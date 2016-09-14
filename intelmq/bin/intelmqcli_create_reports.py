# -*- coding: utf-8 -*-
"""
Create RTIR reports for data without, per feed.name

https://github.com/certat/intelmq/issues/53#issuecomment-235338136

evlist = get all open events where report_id IS NULL
foreach distinct feed.names in evlist
   report_data = create a zipped json file (minus raw attribute) with events from current feed.name
   create report with attachment report_data
   set report_id for the used events to newly created report

TODO: Non-batch mode
"""
from __future__ import print_function, unicode_literals

import datetime
import io
import json
import time
import zipfile

import psycopg2
import psycopg2.extras

import intelmq.lib.intelmqcli as lib

# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


class IntelMQCLIContoller(lib.IntelMQCLIContollerTemplate):
    appname = 'intelmqcli_create_reports'

    def init(self):
        self.parser.add_argument('-l', '--list-feeds', action='store_true',
                                 help='List all open feeds')

        self.setup()
        self.connect_database()

        if self.args.list_feeds:
            self.execute(lib.QUERY_OPEN_FEEDNAMES)
            for row in self.cur.fetchall():
                if row['feed.name']:
                    self.logger.info(row['feed.name'])
            exit(0)

        if not self.rt.login():
            self.logger.error('Could not login as {} on {}.'.format(self.config['rt']['user'],
                                                                    self.config['rt']['uri']))
            exit(2)
        else:
            self.logger.info('Logged in as {} on {}.'.format(self.config['rt']['user'],
                                                             self.config['rt']['uri']))

        self.execute(lib.QUERY_OPEN_FEEDNAMES)
        feednames = [x['feed.name'] for x in self.cur.fetchall()]
        if feednames:
            self.logger.info("All feeds: " + ", ".join(['%r']*len(feednames))%tuple(feednames))
        else:
            self.logger.info('Nothing to do.')
        for feedname in feednames:
            self.logger.info('Handling feedname {!r}.'.format(feedname))
            self.execute(lib.QUERY_OPEN_EVENTS_BY_FEEDNAME,
                         (feedname, ))
            feeddata = []
            self.logger.info('Found %s events.' % self.cur.rowcount)
            for row in self.cur:
                """
                First, we ignore None-data
                Second, we ignore raw
                Third, we convert everything to strings, e.g. datetime-objects
                """
                feeddata.append({k: (str(v) if isinstance(v, datetime.datetime) else v)
                                 for k, v in row.items() if v is not None and k != 'raw'})

            attachment = io.BytesIO()
            ziphandle = zipfile.ZipFile(attachment, mode='w',
                                        compression=zipfile.ZIP_DEFLATED)
            ziphandle.writestr('events.json', json.dumps(feeddata))
            ziphandle.close()
            attachment.seek(0)
            subject = 'Reports of {} on {}'.format(feedname, time.strftime('%Y-%m-%d'))

            if self.dryrun:
                self.logger.info('Dry run: Skipping creation of report.')
            else:
                report_id = self.rt.create_ticket(Queue='Incident Reports', Subject=subject,
                                                  Owner=self.config['rt']['user'])
                if report_id == -1:
                    self.logger.error('Could not create Incident ({}).'.format(report_id))
                    return
                else:
                    self.logger.info('Created Report {}.'.format(report_id))

            if self.dryrun:
                self.logger.info('Dry run: Skipping creation of attachment.')
            else:
                comment_id = self.rt.comment(report_id,
                                             files=[('events.zip', attachment, 'application/zip')])
                if not comment_id:
                    self.logger.error('Could not correspond with file.')
                    return

            self.executemany("UPDATE events SET rtir_report_id = %s WHERE id = %s",
                             [(report_id, row['id']) for row in feeddata])
            self.con.commit()
            self.logger.info('Linked events to report.')


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
