#!/bin/bash
# Update tor nodes data
# The target file must be given as only argument on the commandline.
PATH=/bin:/usr/bin
set -e
trap cleanup EXIT

fail()
{
  echo >&2 "$@"
  exit 23
}

setup()
{
  [ "$#" -eq 1 ] || fail "Exactly one argument DESTINATION-FILE must be given."
  DEST_FILE="$1"
  TMP_DIR=`mktemp -d`
  dest_dir=`dirname "$DEST_FILE"`
  [ -d "$dest_dir" ] || mkdir -p "$dest_dir"
}

cleanup()
{
  [ -d "$dest_dir" ] && rm -rf "$TMP_DIR"
}

fetch_and_install()
{
  cd "$TMP_DIR"
  curl -s -O https://internet2.us/static/latest.bz2
  bunzip2 -c latest.bz2 >tor_nodes.dat
  mv tor_nodes.dat "$DEST_FILE"
}

setup "$@"
fetch_and_install
