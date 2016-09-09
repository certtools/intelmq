#!/bin/bash
# -------------------------------------------------------------------
# Copyright (C) 2016 by Intevation GmbH
# Author(s):
# Sascha Wilde <wilde@intevation.de>

# This program is free software under the GNU GPL (>=v2)
# Read the file COPYING coming with the software for details.
# -------------------------------------------------------------------

ME=`basename "$0"`

usage()
{
  cat <<EOF
$ME INHIBITIONS_FILE

Execute add_inhibition.py to create a inhibition for each line 
in INHIBITIONS_FILE.

The format of INHIBITIONS_FILE is:

  asn;network;ctype;cidentifier;comment

EOF
}

fatal()
{
  echo >&2 "$1"
  exit 23
}

gen_commands()
{
  local optnames=( asn network ctype cidentifier comment )
  while IFS=';' read -a vals ; do
    local cmd="add_inhibition.py"
    for i in `seq 0 4` ; do
      [ "${vals[$i]}" ] && cmd+=" --${optnames[$i]} ${vals[$i]}"
    done
    echo "Executing: $cmd"
    eval $cmd
  done
}

#-----------------------------------------------------------------------
# main

[ $# -eq 1 ] || { usage ; exit 1 ; }
cat "$1" | gen_commands
