#!/bin/bash

export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

#IFS=$'\n'
IFS=""

while read -r t ; do 
	./intelmqcli --taxonomy="$t" --batch  --quiet
done



