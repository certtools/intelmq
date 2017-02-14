#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a SQL command file with commands to create the events table.

Reads the harmonization configuration from
`/opt/intelmq/etc/harmonization.conf` and generates an SQL command from it.
The SQL file is saved in `/tmp/initdb.sql` or a temporary name if the other one
exists.
"""
import json
import os
import sys
import tempfile

from intelmq import HARMONIZATION_CONF_FILE

INDICES = ['classification.identifier', 'classification.taxonomy',
           'classification.type', 'feed.code', 'feed.name',
           'source.abuse_contact', 'source.asn', 'source.ip', 'source.fqdn',
           'time.observation', 'time.source']


def generate(harmonization_file=HARMONIZATION_CONF_FILE):
    FIELDS = dict()

    try:
        print("INFO - Reading %s file" % harmonization_file)
        with open(harmonization_file, 'r') as fp:
            DATA = json.load(fp)['event']
    except IOError:
        print("ERROR - Could not find %s" % harmonization_file)
        print("ERROR - Make sure that you have intelmq installed.")
        sys.exit(2)

    for field in DATA.keys():
        value = DATA[field]

        if value['type'] in ('String', 'Base64', 'URL', 'FQDN',
                             'MalwareName', 'ClassificationType',
                             'LowercaseString', 'UppercaseString', 'Registry'):
            if 'length' in value:
                dbtype = 'varchar({})'.format(value['length'])
            else:
                dbtype = 'text'
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
            raise ValueError('Unknow type %r.' % value['type'])

        FIELDS[field] = dbtype

    initdb = """CREATE TABLE events (
    "id" BIGSERIAL UNIQUE PRIMARY KEY,"""
    for field, field_type in sorted(FIELDS.items()):
        initdb += '\n    "{name}" {type},'.format(name=field, type=field_type)

    initdb = initdb[:-1]  # remove last ','
    initdb += "\n);\n"

    for index in INDICES:
        initdb += 'CREATE INDEX "idx_events_{0}" ON events USING btree ("{0}");\n'.format(index)
    return initdb


def main():
    OUTPUTFILE = "/tmp/initdb.sql"
    fp = None
    try:
        if os.path.exists(OUTPUTFILE):
            print('INFO - File {} exists, generating temporary file.'.format(OUTPUTFILE))
            os_fp, OUTPUTFILE = tempfile.mkstemp(suffix='.initdb.sql',
                                                 text=True)
            fp = os.fdopen(os_fp, 'wt')
        else:
            fp = open(OUTPUTFILE, 'wt')
        psql = generate()
        print("INFO - Writing %s file" % OUTPUTFILE)
        fp.write(psql)
    finally:
        if fp:
            fp.close()


if __name__ == '__main__':  # pragma: no cover
    main()
