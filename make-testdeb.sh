#!/bin/bash

cd $(dirname $0)
TMP=$(mktemp)
TIMESTAMP="$(date +%Y%m%d%H%M%S)"

clean_up () {
  rm $TMP
  exit
}

format_changelog_entry () {
  # Add autobuild tag to version in changelog header
  local HEADER=$(head -1 debian/changelog |
  sed "s/autobuild[0-9]\{14\})/)/; s/)/autobuild${TIMESTAMP})/")
  # Get git revision
  if which git > /dev/null ; then
    local REF=$(git rev-parse HEAD)
  else
    local BRANCH=$(cut -d' ' -f2 .git/HEAD)
    local REF=$(cat .git/${BRANCH})
  fi
  # Format the changelog entry
  cat << EOF
$HEADER

  * Automatic test build of $REF
    by $LOGNAME on $(hostname)

 -- Auto Build <autobuild@intevation.invalid>  $(date -R)

EOF
}

trap clean_up SIGHUP SIGINT SIGTERM

format_changelog_entry > $TMP
cat debian/changelog  >> $TMP

cp $TMP debian/changelog
clean_up
