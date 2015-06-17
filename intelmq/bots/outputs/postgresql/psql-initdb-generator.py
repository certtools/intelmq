import re
import sys

FILE = "/usr/share/doc/intelmq/DataHarmonization.md"
OUTPUTFILE = "/tmp/initdb.sql"
REGEX_TABLE = "^\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|$"
REGEX_FIELDS = "\|[^|]+\|([^|]+)\|([^|]+)\|"
FIELDS = dict()

try:
    with open(FILE, 'r') as fp:
        data = fp.read()
    print "[INFO] Reading %s file" % FILE
except IOError:
    print "[ERROR] Could not find %s" % FILE
    print "[ERROR] Make sure that you have intelmq installed."
    sys.exit(-1)

for line in data.split('\n'):
    match = re.search(REGEX_TABLE, line)
    if match:

        if match.group(0).startswith('|Section') or match.group(0).startswith('|:---'):
            continue

        match = re.search(REGEX_FIELDS, line)
        if match.group(1) in FIELDS.keys():
            print match.group(1)

        FIELDS[match.group(1)] = match.group(2)


initdb = "CREATE table events ("
for field, field_type in sorted(FIELDS.iteritems()):
    initdb += '\n\t"%s" %s,' % (field, field_type)

initdb = initdb[:-1]
initdb += "\n);"


with open(OUTPUTFILE, 'w') as fp:
    print "[INFO] Writing %s file" % OUTPUTFILE
    fp.write(initdb)
