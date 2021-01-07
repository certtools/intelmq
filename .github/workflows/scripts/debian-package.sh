#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2020 Birger Schacht
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Bash script for a github action to build a Debian
# package in a user-defined Debian container


set -x
set -e

# A list of known Debian releases
knowncodenames=("stretch" "buster" "bullseye" "stable" "testing")

# We want exactly one argument: the name of the release
if (( $# != 1 ))
then
	>&2 echo "Illegal number of parameters"
	exit 1
fi

codename=$1

# check if the releasename is in the list of known Debian distributions
validcodename=false
for value in "${knowncodenames[@]}"
do
	[[ "$codename" = "$value" ]] && validcodename=true
done

# If the release name is not valid, simply exit
unknowncodename () {
	>&2 echo "Debian distribution not known. Valid arguments are: ${knowncodenames[*]}"
	exit 1
}

# Build the package in the container
build () {
	codename=$1
	echo "Building on ${codename}"
	# run installation in buildah

	ARTIFACTEXTENSIONS=("deb" "xz" "dsc" "buildinfo" "changes")
	PARENT=$(dirname "${GITHUB_WORKSPACE}")
	echo "Building on ${codename} in ${GITHUB_WORKSPACE}"

	# fetch and configure the container
	CONTAINER=$(buildah from docker.io/debian:"${codename}"-slim)
	buildah config --workingdir "${GITHUB_WORKSPACE}" "${CONTAINER}"

	# install build dependencies in the container
	BR="buildah run -v ${PARENT}:${PARENT}"
	${BR} "${CONTAINER}" apt-get update -qq
	${BR} "${CONTAINER}" apt-get install dpkg-dev lintian -y
	${BR} "${CONTAINER}" apt-get build-dep -y .

	# this is a hack because intelmq does
	# not like to be run as root :( :
	${BR} "${CONTAINER}" chown -R nobody:nogroup "${PARENT}"
	${BR} --user nobody:nogroup "${CONTAINER}" /bin/sh -c 'dpkg-buildpackage -us -uc -b'

	# create a directory for the artifacts
	# and copy the relevant files there
	mkdir -p "${HOME}/artifacts"
	for extension in "${ARTIFACTEXTENSIONS[@]}"
	do
		find "${PARENT}" -type f -name "*.${extension}" -exec cp '{}' "${HOME}/artifacts/" \;
	done
}

# check if release name is valid; build if it is, exit if it isn't
if [ "$validcodename" = true ]
then
	build "$codename"
else
	unknowncodename
fi
