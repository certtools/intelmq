# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 17:23:52 2018

@author: sebastian
"""
import psycopg2
import sys
from psycopg2.extras import DictCursor
from publicsuffixlist import PublicSuffixList
from .common import create_parser


def eventdb_apply(host, port,
                  database, username, password,
                  table, dry_run, where,
                  filename):
    if password:
        password = input('Password for user %r on %r: ' % (username, host))
    where = 'AND ' + where if where else ''

    con1 = psycopg2.connect(user=username,
                            password=password,
                            database=database,
                            host=host, port=port)
    cur1 = con1.cursor(cursor_factory=DictCursor)
    con2 = psycopg2.connect(user=username,
                            password=password,
                            database=database,
                            host=host, port=port)
    con2.autocommit = True
    cur2 = con2.cursor(cursor_factory=DictCursor)
    cur1.execute('''
                 SELECT id, "source.fqdn", "destination.fqdn"
                 FROM {table}
                 WHERE
                 ("source.fqdn" IS NOT NULL OR "destination.fqdn" IS NOT NULL)
                 {where}
                 '''.format(table=table, where=where))

    psl = PublicSuffixList(only_icann=True)

    counter = 0
    for row in cur1:
        counter += 1
        if row['source.fqdn']:
            cur2.execute('update events set "source.domain_suffix" = %s where id = %s', (psl.publicsuffix(row['source.fqdn'].encode('idna').decode()), row['id']))

        if row['destination.fqdn']:
            cur2.execute('update events set "destination.domain_suffix" = %s where id = %s', (psl.publicsuffix(row['destination.fqdn'].encode('idna').decode()), row['id']))
    con2.commit()
    print("Changed %d rows" % counter)


def main():
    parser = create_parser(name='eventdb',
                           description='Apply the mapping to an existing EventDB.')
    args = parser.parse_args()
    return eventdb_apply(**vars(args).copy())


if __name__ == "__main__":
    sys.exit(main())
