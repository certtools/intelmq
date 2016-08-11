# -*- coding: utf-8 -*-
"""
Create RTIR reports for data without, per feed.name

https://github.com/certat/intelmq/issues/53#issuecomment-235338136

evlist = get all open events where report_id IS NULL
foreach distinct feed.names in evlist
   report_data = create a zipped json file (minus raw attribute) with events from current feed.name
   create report with attachment report_data
   set report_id for the used events to newly created report
"""
from __future__ import print_function, unicode_literals

import datetime
import io
import json
import sys
import time
import zipfile
from functools import partial

import psycopg2
import psycopg2.extras

import rt
from intelmq.lib.intelmqcli import *

# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

error = partial(print, file=sys.stderr)
quiet = False
old_print = print


def print(*args, **kwargs):
    if not quiet:
        old_print(*args, **kwargs)


def main():
    config = read_config()
    rtir = rt.Rt(config['rt']['uri'], config['rt']['user'],
                 config['rt']['password'])
    if not rtir.login():
        error('Could not login as {} on {}.'.format(config['rt']['user'],
                                                    config['rt']['uri']))
        exit(2)
    else:
        print('Logged in as {} on {}.'.format(config['rt']['user'],
                                              config['rt']['uri']))
    con, cur = connect_database(config)

    cur.execute(QUERY_OPEN_FEEDNAMES)
    feednames = [x['feed.name'] for x in cur.fetchall()]
    for feedname in feednames:
        print('Handling feedname {!r}.'.format(feedname))
        cur.execute(QUERY_OPEN_EVENTS_BY_FEEDNAME,
                    (feedname, ))
        feeddata = []
        for row in cur:
            """
            First, we ignore None-data
            Second, we ignore raw
            Third, we convert everything to strings, e.g. datetime-objects
            """
            feeddata.append({k: (str(v) if isinstance(v, datetime.datetime) else v)
                             for k, v in row.items() if v is not None and k != 'raw'})

        attachment = io.BytesIO()
        ziphandle = zipfile.ZipFile(attachment, mode='w')
        ziphandle.writestr('events.json', json.dumps(feeddata))
        ziphandle.close()
        attachment.seek(0)
        subject = 'Reports of {} on {}'.format(feedname, time.strftime('%Y-%m-%d'))

        report_id = rtir.create_ticket(Queue='Incident Reports', Subject=subject,
                                       Owner=config['rt']['user'])
        if report_id == -1:
            error('Could not create Incident ({}).'.format(report_id))
            return
        else:
            print('Created Report {}.'.format(report_id))
        comment_id = rtir.comment(report_id,
                                  files=[('events.zip', attachment, 'application/zip')])
        if not comment_id:
            error('Could not correspond with file.')
            return

        cur.executemany("UPDATE events SET rtir_report_id = %s WHERE id = %s",
                        [(report_id, row['id']) for row in feeddata])

if __name__ == '__main__':
    main()
