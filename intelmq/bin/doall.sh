#!/bin/sh

export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8

#IFS=$'\n'
IFS=""

while read -r f ; do 
	./intelmqcli --feed="$f" --batch --quiet
done



