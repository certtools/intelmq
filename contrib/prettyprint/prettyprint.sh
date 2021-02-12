#!/bin/sh

while read -r i;
do
  echo "$i" | python -m json.tool ;
done < "$1"
