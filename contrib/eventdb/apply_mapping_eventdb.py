#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 15:47:07 2018

@author: sebastian
"""

import csv
import io
import re
import sys
from .common import create_parser

try:
    import requests
except ImportError:
    requests = None

try:
    import psycopg2
    from psycopg2.extras import DictCursor
except ImportError:
    psycopg2 = None


def eventdb_apply(malware_name_column, malware_family_column, host, port,
                  database, username, password,
                  table, dry_run, where,
                  filename):
    if not filename:
        if requests is None:
            print("Error: Python module 'requests' is needed to download the mapping, "
                  "but not available.", file=sys.stderr)
            return 2
        data = requests.get('https://raw.githubusercontent.com/certtools/malware_name_mapping/master/mapping.csv').text
        with io.StringIO(data) as handle:
            mapping = [[re.compile(line[0], re.IGNORECASE), line[1]] for line in csv.reader(handle)]
    else:
        with open(filename) as handle:
            mapping = [[re.compile(line[0], re.IGNORECASE), line[1]] for line in csv.reader(handle)]
    families = [x[1] for x in mapping]

    if psycopg2 is None:
        print("Error: Python module 'psycopg2' is needed but not available.", file=sys.stderr)
        return 2
    if password:
        password = input('Password for user %r on %r: ' % (username, host))
    where = 'AND ' + where if where else ''

    db = psycopg2.connect(database=database, user=username, password=password,
                          host=host, port=port)
    db.autocommit = True
    cur = db.cursor(cursor_factory=DictCursor)

    cur.execute('SELECT DISTINCT "classification.identifier", "malware.name" FROM {table} '
                'WHERE "classification.taxonomy" = \'malicious code\' {where}'
                ''.format(table=table, where=where))
    if dry_run:
        execute = lambda x, y: print(cur.mogrify(x, y).decode())  # noqa: E731
    else:
        execute = cur.execute
    for (identifier, malware_name) in cur.fetchall():
        if identifier in families or not malware_name:
            continue
        for rule in mapping:
            if rule[0].match(malware_name):
                if identifier == rule[1]:
                    continue
                if identifier:
                    print('Correcting family for', malware_name, ':', identifier, '->', rule[1])
                else:
                    print('Setting family for', malware_name, ':', rule[1])
                execute('UPDATE {table} SET "classification.identifier" = %s '
                        'WHERE "malware.name" = %s '
                        'AND "classification.identifier" IS DISTINCT FROM %s AND '
                        '"classification.taxonomy" = \'malicious code\' {where}'
                        ''.format(table=table, where=where),
                        (rule[1], malware_name, rule[1]))
                break
        else:
            print('missing mapping for', repr(malware_name))

    return 0


def main():
    parser = create_parser(name='eventdb', description='Apply the mapping to an existing EventDB.')
    parser.add_argument('--filename', '-f',
                        help="Path to mapping file name. Will be downloaded if not given.")
    parser.add_argument('--malware-name-column', '-m', default='malware.name',
                        help='Use this column as malware name, default: '
                             "'malware.name'")
    parser.add_argument('--malware-family-column', '-c',
                        default='classification.identifier',
                        help='Apply the mapping to this column, '
                             "default: 'classification.identifier'")

    args = parser.parse_args()
    return eventdb_apply(**vars(args).copy())


if __name__ == "__main__":
    sys.exit(main())
