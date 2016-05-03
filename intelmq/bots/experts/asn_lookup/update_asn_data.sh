#!/bin/bash
# Update asn data
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
  # FIXME: we have to use http as the data is not available via httpd,
  # so this is not a secure connection... :-(
  curl -k -s -O http://data.ris.ripe.net/rrc12/latest-bview.gz
  gunzip -c <latest-bview.gz | bzip2 -c >latest-bview.bz2 
  pyasn_util_convert.py --single --no-progress latest-bview.bz2 ipasn.dat
  mv ipasn.dat "$DEST_FILE"
}

setup "$@"
fetch_and_install
