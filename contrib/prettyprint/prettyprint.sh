#!/bin/sh

# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

while read -r i;
do
  echo "$i" | python -m json.tool ;
done < "$1"
