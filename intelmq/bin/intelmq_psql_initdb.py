#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a SQL command file with commands to create the events table.

Reads the Data-Harmonization.md document from
`/opt/intelmq/docs/Data-Harmonization.md` and generates an SQL command from it.
The SQL file is saved in `/tmp/initdb.sql`.
"""
import json
import sys

from intelmq import HARMONIZATION_CONF_FILE


def main():
    OUTPUTFILE = "/tmp/initdb.sql"
    FIELDS = dict()

    try:
        print("INFO - Reading %s file" % HARMONIZATION_CONF_FILE)
        with open(HARMONIZATION_CONF_FILE, 'r') as fp:
            DATA = json.load(fp)['event']
    except IOError:
        print("ERROR - Could not find %s" % HARMONIZATION_CONF_FILE)
        print("ERROR - Make sure that you have intelmq installed.")
        sys.exit(-1)

    for field in DATA.keys():
        value = DATA[field]

        if value['type'] in ('String', 'Base64', 'URL', 'FQDN',
                             'MalwareName', 'ClassificationType'):
            dbtype = 'varchar({})'.format(value.get('length', 2000))
        elif value['type'] in ('IPAddress', 'IPNetwork'):
            dbtype = 'inet'
        elif value['type'] == 'DateTime':
            dbtype = 'timestamp with time zone'
        elif value['type'] == 'Boolean':
            dbtype = 'boolean'
        elif value['type'] == 'Integer':
            dbtype = 'integer'
        elif value['type'] in ('Float', 'Accuracy'):
            dbtype = 'real'
        elif value['type'] == 'UUID':
            dbtype = 'UUID'
        elif value['type'] == 'JSON':
            dbtype = 'json'
        else:
            print('Unknow type {!r}, assuming varchar(2000) by default'
                  ''.format(value['type']))
            dbtype = 'varchar(2000)'

        FIELDS[field] = dbtype

    initdb = """CREATE table events (
        "id" BIGSERIAL UNIQUE PRIMARY KEY,"""
    for field, field_type in sorted(FIELDS.items()):
        initdb += '\n    "{name}" {type},'.format(name=field, type=field_type)

    initdb = initdb[:-1]  # remove last ','
    initdb += "\n);"

    with open(OUTPUTFILE, 'w') as fp:
        print("INFO - Writing %s file" % OUTPUTFILE)
        fp.write(initdb)

if __name__ == '__main__':
    main()
