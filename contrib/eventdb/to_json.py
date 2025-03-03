#!/usr/bin/python3

# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from argparse import ArgumentParser
from datetime import datetime
import json
from sys import exit, stderr
from pprint import pprint

from psycopg2 import connect
from psycopg2.extras import RealDictCursor

parser = ArgumentParser(
                    prog='EventDB to JSON',
                    description='Extract data from the IntelMQ EventDB')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-i', '--id', help='Get events by ID')
parser.add_argument('-p', '--pretty', action='store_true', help='Pretty print JSON output')
parser.add_argument('--dsn', help='A complete libpg conninfo string. If not given, it will be loaded from /etc/intelmq/eventdb-serve.conf')
args = parser.parse_args()

if args.dsn:
    conninfo = args.dsn
else:
    try:
        with open('/etc/intelmq/eventdb-serve.conf') as fody_config:
            conninfo = json.load(fody_config)['libpg conninfo']
    except FileNotFoundError as exc:
        print(f'Could not load database configuration. {exc}', file=stderr)
        exit(2)

if args.verbose:
    print(f'Using DSN {conninfo!r}.')
db = connect(dsn=conninfo)
cur = db.cursor(cursor_factory=RealDictCursor)
cur.execute ('SELECT * FROM events WHERE id = %s', (args.id, ))

for row in cur.fetchall():
    del row['id']
    for key in list(row.keys()):
        if isinstance(row[key], datetime):
            # data from the database has TZ information already included
            row[key] = row[key].isoformat()
        elif row[key] is None:
            del row[key]
    if args.pretty:
        print(json.dumps(row, indent=2))
    else:
        print(json.dumps(row))
