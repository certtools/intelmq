# -*- coding: utf-8 -*-
"""
Generates a SQL command file with commands to create the events table.

Reads the Data-Harmonization.md document from
`/opt/intelmq/docs/Data-Harmonization.md` and generates an SQL command from it.
The SQL file is saved in `/tmp/initdb.sql`.
"""
from __future__ import print_function, unicode_literals
import re
import sys

FILE = "/opt/intelmq/docs/Data-Harmonization.md"
OUTPUTFILE = "/tmp/initdb.sql"
REGEX_TABLE = r"^\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|$"
REGEX_FIELDS = r"\|[^|]+\|([^|]+)\|([^|]+)\|"
FIELDS = dict()

try:
    with open(FILE, 'r') as fp:
        data = fp.readlines()
    print("INFO - Reading %s file" % FILE)
except IOError:
    print("ERROR - Could not find %s" % FILE)
    print("ERROR - Make sure that you have intelmq installed.")
    sys.exit(-1)

for line in data:
    match = re.search(REGEX_TABLE, line)
    if match:
        if (match.group(0).startswith('|Section') or
           match.group(0).startswith('|:---') or
           match.group(0).startswith('|Name') or
           match.group(0).startswith('|<a name=')):
            continue

        match = re.search(REGEX_FIELDS, line)
        if match.group(1) in FIELDS.keys():
            print('duplicate entry found for {}'.format(match.group(1)))

        # FIXME: repalce workaround, fix in docs
        FIELDS[match.group(1).replace('_', '.', count=1)] = match.group(2)


initdb = "CREATE table events ("
for field, field_type in sorted(FIELDS.items()):
    initdb += '\n\t"{name}" {type},'.format(name=field, type=field_type)

print(initdb[-1])
initdb = initdb[:-1]
initdb += "\n);"

with open(OUTPUTFILE, 'w') as fp:
    print("INFO - Writing %s file" % OUTPUTFILE)
    fp.write(initdb)
