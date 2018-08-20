#!/bin/sh
set -e

if [ "$1" = "remove" ] ; then
    if getent passwd intelmq >/dev/null 2>&1; then
        userdel intelmq
    fi
    if getent group intelmq >/dev/null 2>&1; then
        groupdel intelmq
    fi
fi

#DEBHELPER#
