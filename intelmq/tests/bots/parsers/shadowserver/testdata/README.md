<!--
SPDX-FileCopyrightText: 2017 Gernot Schulz

SPDX-License-Identifier: AGPL-3.0-or-later
-->

Shadowserver test feeds
=======================

This directory contains anonymized Shadowserver feeds that can be used for
testing.

Restrictions:

All csv files here must have a valid name, otherwise test_testdata.py will fail.
To use a file with an invalid filename, it must be named with another extension
such as scan_chargen.short, used in test_scan_chargen.py


clean-shadowserver.awk
----------------------

Also provided is the script that was used to help anonymize the feeds.
clean-shadowserver.awk replaces various information, such as IP addresses,
using regular expressions.

Usage:

    ./clean-shadowserver.awk < FEED.csv

This script is not a complete solution; further manual edits will almost
certainly be necessary to generate files suitable for distribution!

Possible improvements:

* match more types of data
* match and replace more precisely
* randomize more strings (currently only IPv4)
* keep relationships of data within records, e.g., in case of multiple IP
  address fields
