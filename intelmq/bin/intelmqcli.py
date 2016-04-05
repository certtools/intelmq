#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implemented workarounds for old packages:
    BytesIO instead of StringIO on Python 2 for csv module

TODO: "feed.name" ILIKE '%' is slow
"""
from __future__ import print_function, unicode_literals

import argparse
import csv
import datetime
import io
import json
import locale
import os
import pprint
import pkg_resources
import readline  # nopep8, hooks into input()
import subprocess
import sys
import tempfile
import zipfile

import psycopg2
import psycopg2.extras
import psycopg2.extensions
import six
import tabulate
from intelmq.lib.intelmqcli import *
from termstyle import bold, green, inverted, red, reset

import rt
from intelmq.lib import utils


# Use unicode for all input and output
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

myinverted = str(reset) + str(inverted)
if six.PY2:
    input = raw_input

with open('/etc/intelmq/intelmqcli.conf') as conf_handle:
    CONFIG = json.load(conf_handle)
home = os.path.expanduser("~")      # needed for OSX
with open(os.path.expanduser(home + '/.intelmq/intelmqcli.conf')) as conf_handle:
    user_config = json.load(conf_handle)

for key, value in user_config.items():
    if key in CONFIG and type(CONFIG[key]) is dict:
        CONFIG[key].update(value)
    else:
        CONFIG[key] = value


class IntelMQCLIContoller():
    table_mode = False  # for sticky table mode
    rt = rt.Rt(CONFIG['rt']['uri'], CONFIG['rt']['user'],
               CONFIG['rt']['password'])
    dryrun = False
    verbose = False
    compress_csv = False
    boilerplate = None

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog=APPNAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=USAGE,
            description=DESCRIPTION,
            epilog=EPILOG,
        )
        VERSION = pkg_resources.get_distribution("intelmq").version
        parser.add_argument('--version',
                            action='version', version=VERSION)
        parser.add_argument('-l', '--list-feeds', action='store_true',
                            help='List all feeds')
        parser.add_argument('-L', '--list-texts', action='store_true',
                            help='List all existing texts.')
        parser.add_argument('-t', '--text', nargs=1, help='Specify the text to be used.')
        parser.add_argument('-f', '--feed', nargs='?', default='%', const='%',
                            help='Show only incidents reported by given feed.')
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Print verbose messages.')
        parser.add_argument('-c', '--compress-csv', action='store_true',
                            help='Automatically compress/shrink the attached CSV report if fields are empty (default = False).')
        parser.add_argument('-n', '--dry-run', action='store_true',
                            help='Do not store anything or change anything. Just simulate.')
        args = parser.parse_args()

        if args.verbose:
            self.verbose = True
        if args.dry_run:
            self.dryrun = True
        if args.compress_csv:
            self.compress_csv = True
        if args.text:
            self.boilerplate = args.text

        self.connect_database()

        if args.list_feeds:
            self.cur.execute(QUERY_FEED_NAMES)
            for row in self.cur.fetchall():
                if row['feed.name']:
                    print(row['feed.name'])
            exit(0)

        if args.list_texts:
            self.cur.execute(QUERY_TEXT_NAMES)
            for row in self.cur.fetchall():
                if row['key']:
                    print(row['key'])
            exit(0)


        if locale.getpreferredencoding() != 'UTF-8':
            print(red('The preferred encoding of your locale setting is not UTF-8 '
                      'but {}. Exiting.'.format(locale.getpreferredencoding())))
            exit(1)

        if not self.rt.login():
            print(red('Could not login as {} on {}.'.format(CONFIG['rt']['user'],
                                                            CONFIG['rt']['uri'])))
        else:
            print('Logged in as {} on {}.'.format(CONFIG['rt']['user'],
                                                  CONFIG['rt']['uri']))
        try:
            while True:
                asn_count = self.count_by_asn(feed=args.feed)
                if self.verbose:
                    print(sys.stderr, 'asn_count = {}.'.format(asn_count))
                answer = input('{i}detailed view by id, {b}[a]{i}utomatic '
                               'sending, {b}[q]{i}uit?{r} '
                               ''.format(b=bold, i=myinverted, r=reset)).strip()
                try:
                    answer = int(answer)
                except ValueError:
                    pass
                if answer == 'q':
                    break
                elif answer == 'a':
                    for item in asn_count:
                        if item['contacts']:
                            self.query_by_as(item['contacts'], automatic=True,
                                             feed=args.feed)
                        else:
                            if item['asn']:
                                self.query_by_as(int(item['asn']), automatic=True,
                                                 feed=args.feed)
                            else:
                                print(red('Can not query the data of an unknown ASN. Ignoring.'))
                elif type(answer) is int:
                    if asn_count[answer]['contacts']:
                        self.query_by_as(asn_count[answer]['contacts'],
                                         feed=args.feed)
                    else:
                        if asn_count[answer] and asn_count[answer]['asn']:
                            self.query_by_as(int(asn_count[answer]['asn']),
                                                 feed=args.feed)
                        else:
                            print(red('no ASNs known. Ignoring.'))
                else:
                    print(red('Unknown answer {!r}.'.format(answer)))

        except BaseException as exc:
            if isinstance(exc, (SystemExit, KeyboardInterrupt)):
                print()
            else:
                raise
        finally:
            self.rt.logout()

    def connect_database(self):
        self.con = psycopg2.connect(database=CONFIG['database']['database'],
                                    user=CONFIG['database']['user'],
                                    password=CONFIG['database']['password'],
                                    host=CONFIG['database']['host'],
                                    port=CONFIG['database']['port'],
                                    sslmode=CONFIG['database']['sslmode'],
                                    )
        self.cur = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.con.autocommit = True

    def get_text(self, query):
        text = None
        text_id = None
        if self.boilerplate:  # get id from parameter
            text_id = self.boilerplate
        else:  # get id from type (if only one type present)
            types = [row['classification.identifier'] for row in query
                     if 'classification.identifier' in row]
            if len(types) == 1:
                text_id = types[0]
        if text_id:  # get text from db if possible
            self.query_get_text(text_id)
            if self.cur.rowcount:
                text = self.cur.fetchall()[0]['body']
        if not text:  # if all failed, get the default
            self.query_get_text(CONFIG['database']['default_key'])
            if self.cur.rowcount:
                text = self.cur.fetchall()[0]['body']
            else:
                return red('Default text not found!')

        return text

    def shrink_dict(self, d):
        if not self.compress_csv:
            return d
        keys = d[0].keys()
        empty = dict(zip(keys, [True] * len(keys)))
        for line in d:
            for key, value in line.items():
                if value is not None:
                    empty[key] = False
        return [{k: v for k, v in dicti.items() if not empty[k]} for dicti in d]

    def query_by_as(self, contact, requestor=None, automatic=False, feed='%'):
        if type(contact) is int:
            query = self.query_by_asnum(contact, feed)
            if requestor is None:
                requestor = ''
        else:
            query = self.query_by_ascontact(contact, feed)
            if requestor is None:
                requestor = contact
        query = self.shrink_dict(query)
        ids = list(str(row['id']) for row in query)
        asns = set(str(row['source.asn']) for row in query)

        subject = ('{date}: {count} incidents for your AS {asns}'
                   ''.format(count=len(query),
                             date=datetime.datetime.now().strftime('%Y-%m-%d'),
                             asns=', '.join(asns)))
        text = self.get_text(query)
        if six.PY2:
            csvfile = io.BytesIO()
        else:
            csvfile = io.StringIO()
        print(repr(CSV_FIELDS))
        if CSV_FIELDS:
            fieldnames = CSV_FIELDS
        else:
            fieldnames = query[0].keys()    # send all
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        query_unicode = query
        if six.PY2:
            query = [{key: utils.encode(val) if type(val) is six.text_type else val for key, val in row.items()} for row in query]
        writer.writerows(query)
        # note this might contain UTF-8 chars! let's ignore utf-8 errors. sorry.
        attachment_text = utils.decode(csvfile.getvalue(), force=True)
        attachment_lines = attachment_text.splitlines()

        if self.verbose:
            pprint.pprint(text)

        showed_text = '=' * 100 + '''
To: {to}
Subject: {subj}

{text}
    '''.format(to=requestor, subj=subject, text=text)
        showed_text_len = showed_text.count('\n')

        if self.table_mode:
            height = getTerminalHeight() - 3 - showed_text_len
            csvfile.seek(0)
            if len(query) > height:
                with tempfile.NamedTemporaryFile(mode='w+') as handle:
                    handle.write(showed_text + '\n')
                    handle.write(tabulate.tabulate(query_unicode,
                                                   headers='keys',
                                                   tablefmt='psql'))
                    handle.seek(0)
                    subprocess.call(['less', handle.name])
            else:
                print(showed_text,
                      tabulate.tabulate(query_unicode, headers='keys',
                                        tablefmt='psql'), sep='\n')
        else:
            height = getTerminalHeight() - 4
            if 5 + len(query) > height:  # cut query too, 5 is length of text
                print('\n'.join(showed_text.splitlines()[:5]))
                print('...')
                print('\n'.join(attachment_lines[:height - 5]))
                print('...')
            elif showed_text_len + len(query) > height > 5 + len(query):
                print('\n'.join(showed_text.splitlines()[:height - len(query)]))
                print('...')
                print(attachment_text)
            else:
                print(showed_text, attachment_text, sep='\n')
        print('-' * 100)
        if automatic and requestor:
            answer = 's'
        else:
            if automatic:
                print(red('You need to set a valid requestor!'))
            answer = input('{i}{b}[b]{i}ack, {b}[s]{i}end, show {b}[t]{i}able,'
                           ' change {b}[r]{i}equestor or {b}[q]{i}uit?{r} '
                           ''.format(b=bold, i=myinverted, r=reset)).strip()
        if answer == 'q':
            exit(0)
        elif answer == 'b':
            return
        elif answer == 't':
            self.table_mode = bool((self.table_mode + 1) % 2)
            self.query_by_as(contact, requestor=requestor, feed=feed)
            return
        elif answer == ('r'):
            answer = input(inverted('New requestor address:') + ' ').strip()
            if len(answer) == 0:
                if type(contact) is int:
                    requestor = ''
                else:
                    requestor = contact
            else:
                requestor = answer
            self.query_by_as(contact, requestor=requestor, feed=feed)
            return
        elif answer != 's':
            print(red('Unknow command {!r}.'.format(answer)))
            self.query_by_as(contact, requestor=requestor, feed=feed)
            return

        # TODO: Config option for single events (best in ascontacts db)
        if text.startswith(str(red)):
            print(red('I won\'t send with a missing text!'))
            return
        if True:
            self.save_to_rt(ids=ids, subject=subject, requestor=requestor,
                            csvfile=csvfile, body=text)
        else:
            header = attachment_lines[0]
            for id_, attach_line, row in zip(ids, attachment_lines[1:], query):
                if six.PY2:
                    csvfile = io.BytesIO()
                else:
                    csvfile = io.StringIO()
                csvfile.write(header + str('\n'))
                csvfile.write(attach_line)
                subj_date = datetime.datetime.now().strftime('%Y-%m-%d')
                subject = ('{date}: Incident {type} for {target}'
                           ''.format(count=len(query),
                                     date=subj_date,
                                     type=row['classification.type'],
                                     target=target_from_row(row)))
                self.save_to_rt(ids=(id_, ), subject=subject,
                                requestor=requestor, csvfile=csvfile,
                                body=text)

        if requestor != contact and not self.dryrun:
            answer = input(inverted('Save recipient {!r} for ASNs {!s}? [Y/n] '
                                    ''.format(requestor,
                                              ', '.join(asns)))).strip()
            if answer.lower() in ('', 'y', 'j'):
                self.query_update_contact(asns=asns, contact=requestor)
                if self.cur.rowcount == 0:
                    for asn in asns:
                        user = os.environ['USER']
                        time = datetime.datetime.now().strftime('%c')
                        comment = 'Added by {user} @ {time}'.format(user=user,
                                                                    time=time)
                        self.query_insert_contact(asn=int(asn),
                                                  contact=requestor,
                                                  comment=comment)

    def save_to_rt(self, ids, subject, requestor, csvfile, body):
        if self.dryrun:
            print('Not writing to RT, dry-run selected.')
            return

        report_id = self.rt.create_ticket(Queue='Incident Reports',
                                          Subject=subject,
                                          Owner=CONFIG['rt']['user'])
        if report_id == -1:
            print(red('Could not create Incident Report.'))
            return
        print(green('Created Incident Report {}.'.format(report_id)))
        self.query_set_rtirid(events_ids=ids, rtir_id=report_id,
                              rtir_type='report')
        if True:  # TODO: implement zip config
            attachment = csvfile
            attachment.seek(0)
            filename = 'events.csv'
        else:
            attachment = io.BytesIO()
            ziphandle = zipfile.ZipFile(attachment, mode='w')
            ziphandle.writestr('events.csv', csvfile.getvalue())
            ziphandle.close()
            attachment.seek(0)
            filename = 'events.zip'

        incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                            Owner=CONFIG['rt']['user'])
        if incident_id == -1:
            print(red('Could not create Incident.'))
            return
        print(green('Created Incident {}.'.format(incident_id)))
        if not self.rt.edit_link(report_id, 'MemberOf', incident_id):
            print(red('Could not link Incident to Incident Report.'))
            return
        self.query_set_rtirid(events_ids=ids, rtir_id=incident_id,
                              rtir_type='incident')
        investigation_id = self.rt.create_ticket(Queue='Investigations',
                                                 Subject=subject,
                                                 Owner=CONFIG['rt']['user'],
                                                 Requestor=requestor)
        if investigation_id == -1:
            print(red('Could not create Investigation.'))
            return
        print(green('Created Investigation {}.'.format(investigation_id)))
        if not self.rt.edit_link(incident_id, 'HasMember', investigation_id):
            print(red('Could not link Investigation to Incident.'))
            return

        # TODO: CC
        correspond = self.rt.reply(investigation_id, text=body,
                                   files=[(filename, attachment, 'text/csv')])
        if not correspond:
            print(red('Could not correspond with text and file.'))
            return
        print(green('Correspondence added to Investigation.'))

        self.query_set_rtirid(events_ids=ids, rtir_id=investigation_id,
                              rtir_type='investigation')
        if not self.rt.edit_ticket(incident_id, Status='resolved'):
            print(red('Could not close incident {}.'.format(incident_id)))

    def count_by_asn(self, feed='%'):
        # TODO: Existing RT ids!
        asn_count = self.query_count_asn(feed)
        if not asn_count:
            print('No incidents!')
            exit(0)
        headers = map(bold, ['id', 'n°', 'ASNs', 'contacts', 'types', 'feeds'])
        tabledata = []
        for number, row in enumerate(asn_count):
            tabledata.append([number, row['count'], row['asn'],
                              row['contacts'], row['classification'],
                              row['feeds']])
        print(tabulate.tabulate(tabledata, headers=headers, tablefmt='psql'))

        print('{} incidents for {} contacts.'
              ''.format(sum((row['count'] for row in asn_count)),
                             len(asn_count)))
        return asn_count

    def query_by_ascontact(self, contact, feed):
        query = QUERY_BY_ASCONTACT.format(evtab=CONFIG['database']['events_table'],
                                    cc=CONFIG['filter']['cc'],
                                    conttab=CONFIG['database']['contacts_table'])
        self.cur.execute(query, (CONFIG['filter']['fqdn'], contact, feed))
        return self.cur.fetchall()

    def query_by_asnum(self, asn, feed):
        query = QUERY_BY_ASNUM.format(evtab=CONFIG['database']['events_table'],
                                          cc=CONFIG['filter']['cc'],
                                          conttab=CONFIG['database']['contacts_table'])
        self.cur.execute(query, (CONFIG['filter']['fqdn'], asn, feed))
        return self.cur.fetchall()

    def query_count_asn(self, feed):
        query = QUERY_COUNT_ASN.format(evtab=CONFIG['database']['events_table'],
                                       cc=CONFIG['filter']['cc'],
                                       conttab=CONFIG['database']['contacts_table'])
        self.cur.execute(query, (CONFIG['filter']['fqdn'], feed))
        return self.cur.fetchall()

    def query_set_rtirid(self, events_ids, rtir_id, rtir_type):
        query = QUERY_SET_RTIRID.format(evtab=CONFIG['database']['events_table'],
                                        rtirid=rtir_id, type=rtir_type,
                                        ids=','.join(events_ids))
        self.cur.execute(query)

    def query_update_contact(self, contact, asns):
        query = QUERY_UPDATE_CONTACT.format(conttab=CONFIG['database']['contacts_table'],
                                            ids=','.join(asns))
        self.cur.execute(query, (contact, ))

    def query_insert_contact(self, contact, asn, comment):
        query = QUERY_INSERT_CONTACT.format(conttab=CONFIG['database']['contacts_table'])
        self.cur.execute(query, (asn, contact, comment))

    def query_get_text(self, text_id):
        self.cur.execute(QUERY_GET_TEXT.format(texttab=CONFIG['database']['text_table']),
                         (text_id, ))


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
