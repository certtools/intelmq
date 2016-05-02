#!/bin/bash
# Update tor nodes data
PATH=/bin:/usr/bin

set -e
trap cleanup EXIT

DEST_FILE=/opt/intelmq/var/lib/bots/tor_nodes/tor_nodes.dat
TMP_DIR=`mktemp -d`
dest_dir=`dirname "$DEST_FILE"`

cleanup()
{
  [ -e "$TMP_DIR/latest.bz2" ] && rm "$TMP_DIR/latest.bz2"
  rmdir "$TMP_DIR"
}


[ -d "$dest_dir" ] || mkdir -p "$dest_dir"

cd "$TMP_DIR"
curl -O https://internet2.us/static/latest.bz2
bunzip2 -c latest.bz2 >tor_nodes.dat
mv tor_nodes.dat "$DEST_FILE"
