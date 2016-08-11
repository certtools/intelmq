#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implemented workarounds for old packages:
    BytesIO instead of StringIO on Python 2 for csv module

"""
from __future__ import print_function, unicode_literals

import argparse
import csv
import datetime
import io
import json
import locale
import os
import readline  # nopep8, hooks into input()
import subprocess
import sys
import tempfile
import zipfile
from functools import partial

import pkg_resources
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import six
import tabulate
from termstyle import bold, green, inverted, red, reset

import intelmq.lib.intelmqcli as lib
import rt
from intelmq.lib import utils

error = partial(print, file=sys.stderr)
quiet = False
old_print = print


def print(*args, **kwargs):
    if not quiet:
        print(*args, **kwargs)


# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

myinverted = str(reset) + str(inverted)
if six.PY2:
    input = raw_input


class IntelMQCLIContoller():
    verbose = False
    compress_csv = False
    boilerplate = None

    def __init__(self):
        global quiet
        parser = argparse.ArgumentParser(
            prog=lib.APPNAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=lib.USAGE,
            description=lib.DESCRIPTION,
            epilog=lib.EPILOG,
        )
        VERSION = pkg_resources.get_distribution("intelmq").version
        parser.add_argument('--version',
                            action='version', version=VERSION)

        parser.add_argument('-l', '--list-feeds', action='store_true',
                            help='List all feeds')
        parser.add_argument('-f', '--feed', nargs='?', default='%', const='%',
                            help='Show only incidents reported by given feed.')

        parser.add_argument('-i', '--list-identifiers', action='store_true',
                            help='List all identifiers')

        parser.add_argument('-L', '--list-texts', action='store_true',
                            help='List all existing texts.')
        parser.add_argument('-t', '--text', nargs=1, help='Specify the text to be used.')

        parser.add_argument('-T', '--list-taxonomies', action='store_true',
                            help='List all taxonomies')
        parser.add_argument('--taxonomy', nargs='?', default='%', const='%',
                            help='Select only events with given taxonomy.')

        parser.add_argument('-y', '--list-types', action='store_true',
                            help='List all types')

        parser.add_argument('-a', '--asn', type=int, nargs='+',
                            help='Specify one or more AS numbers (integers) to process.')

        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Print verbose messages.')

        parser.add_argument('-c', '--compress-csv', action='store_true',
                            help='Automatically compress/shrink the attached CSV report if fields are empty (default = False).')

        parser.add_argument('-b', '--batch', action='store_true',
                            help='Run in batch mode (defaults to "yes" to all).')
        parser.add_argument('-q', '--quiet', action='store_true',
                            help='Do not output anything, except for error messages. Useful in combination with --batch.')
        parser.add_argument('-n', '--dry-run', action='store_true',
                            help='Do not store anything or change anything. Just simulate.')
        args = parser.parse_args()

        if args.quiet:
            quiet = True
        if args.verbose:
            self.verbose = True
        if args.dry_run:
            self.dryrun = True
        if args.batch:
            self.batch = True
        if args.compress_csv:
            self.compress_csv = True
        if args.asn:
            self.filter_asns = args.asn
        if args.text:
            self.boilerplate = args.text

        self.config = read_config()
        self.con, self.cur = connect_database()

        if args.list_feeds:
            self.cur.execute(lib.QUERY_FEED_NAMES)
            for row in self.cur.fetchall():
                if row['feed.name']:
                    print(row['feed.name'])
            exit(0)

        if args.list_texts:
            self.cur.execute(lib.QUERY_TEXT_NAMES)
            for row in self.cur.fetchall():
                if row['key']:
                    print(row['key'])
            exit(0)

        if args.list_identifiers:
            self.cur.execute(lib.QUERY_IDENTIFIER_NAMES)
            for row in self.cur.fetchall():
                if row['classification.identifier']:
                    print(row['classification.identifier'])
            exit(0)

        if args.list_taxonomies:
            self.cur.execute(lib.QUERY_TAXONOMY_NAMES)
            for row in self.cur.fetchall():
                if row['classification.taxonomy']:
                    print(row['classification.taxonomy'])
            exit(0)

        if args.list_types:
            self.cur.execute(lib.QUERY_TYPE_NAMES)
            for row in self.cur.fetchall():
                if row['classification.type']:
                    print(row['classification.type'])
            exit(0)

        if locale.getpreferredencoding() != 'UTF-8':
            error(red('The preferred encoding of your locale setting is not UTF-8 '
                      'but {}. Exiting.'.format(locale.getpreferredencoding())))
            exit(1)

        if not self.rt.login():
            error(red('Could not login as {} on {}.'.format(self.config['rt']['user'],
                                                            self.config['rt']['uri'])))
            exit(2)
        else:
            print('Logged in as {} on {}.'.format(self.config['rt']['user'],
                                                  self.config['rt']['uri']))
        try:
            self.cur.execute(QUERY_OPEN_TAXONOMIES)
            taxonomies = [x['classification.taxonomy'] for x in self.cur.fetchall()]
            for taxonomy in taxonomies:
                print('Handling taxonomy {!r}.'.format(taxonomy))
                self.cur.execute(QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY, (taxonomy, ))
                report_ids = [x[0] for x in self.cur.fetchall()]
                self.cur.execute(QUERY_OPEN_EVENT_IDS_BY_TAXONOMY, (taxonomy, ))
                event_ids = [x[0] for x in self.cur.fetchall()]
                print(report_ids)
                print(event_ids)
                subject = 'Incidents of {} on {}'.format(taxonomy, time.strftime('%Y-%m-%d'))

                incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                                 Owner=config['rt']['user'])
                if incident_id == -1:
                    error('Could not create Incident ({}).'.format(incident_id))
                    continue
                # XXX TODO: distinguish between national and other constituencies
                self.rt.edit_ticket(incident_id)#, CF__RTIR_Classification=taxonomy,
#                                 CF__RTIR_Constituency='national',
#                                 CF__RTIR_Function='IncidentCoord')

                for report_id in report_ids:
                    if not self.rt.edit_link(report_id, 'MemberOf', incident_id):
                        error(red('Could not link Incident to Incident Report: ({} -> {}).'.format(incident_id, report_id)))
                        continue
                self.cur.executemany("UPDATE events SET rtir_incident_id = %s WHERE id = %s",
                                     [(incident_id, event_id) for event_id in event_ids])
                self.send(None)  # Continue here
        finally:
            self.rt.logout()

    def query_get_text(self, text_id):
        self.cur.execute(lib.QUERY_GET_TEXT.format(texttab=self.config['database']['text_table']),
                                                   (text_id, ))

    def get_text(self, text_id):
        text = None
        if self.boilerplate:  # get id from parameter
            text_id = self.boilerplate
        else:  # get id from type (if only one type present)
        if text_id:  # get text from db if possible
            self.query_get_text(text_id)
            if self.cur.rowcount:
                text = self.cur.fetchall()[0]['body']
        if not text:  # if all failed, get the default
            self.query_get_text(self.config['database']['default_key'])
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

    def send(self, contact):
        query = self.query_by_ascontact(contact, feed, taxonomy)
        requestor = contact
        query = self.shrink_dict(query)
        ids = list(str(row['id']) for row in query)
        asns = set(str(row['source.asn']) for row in query)

        subject = ('{date}: {count} {tax} incidents for your AS {asns}'
                   ''.format(count=len(query),
                             date=datetime.datetime.now().strftime('%Y-%m-%d'),
                             asns=', '.join(asns)))
        text = self.get_text(taxonomy)
        if six.PY2:
            csvfile = io.BytesIO()
        else:
            csvfile = io.StringIO()
        print(repr(lib.CSV_FIELDS))
        if lib.CSV_FIELDS:
            fieldnames = lib.CSV_FIELDS
        else:
            fieldnames = query[0].keys()    # send all
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        query_unicode = query
        if six.PY2:
            query = [{key: utils.encode(val) if isinstance(val, six.text_type) else val for key, val in row.items()} for row in query]
        writer.writerows(query)
        # note this might contain UTF-8 chars! let's ignore utf-8 errors. sorry.
        attachment_text = utils.decode(csvfile.getvalue(), force=True)
        attachment_lines = attachment_text.splitlines()

        if self.verbose:
            print(text)

        showed_text = '=' * 100 + '''
To: {to}
Subject: {subj}

{text}
    '''.format(to=requestor, subj=subject, text=text)
        showed_text_len = showed_text.count('\n')

        if self.table_mode:
            if quiet:
                height = 80     # assume anything for quiet mode
            else:
                height = lib.getTerminalHeight() - 3 - showed_text_len
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
            if quiet:
                height = 80
            else:
                height = lib.getTerminalHeight() - 4
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
            answer = 'q'
            if automatic:
                error(red('You need to set a valid requestor!'))
            if not self.batch:
                answer = input('{i}{b}[b]{i}ack, {b}[s]{i}end, show {b}[t]{i}able,'
                               ' change {b}[r]{i}equestor or {b}[q]{i}uit?{r} '
                               ''.format(b=bold, i=myinverted, r=reset)).strip()
        if answer == 'q':
            exit(0)
        elif answer == 'b':
            return
        elif answer == 't':
            self.table_mode = bool((self.table_mode + 1) % 2)
            self.query_by_as(contact, requestor=requestor, feed=feed,
                             taxonomy=taxonomy)
            return
        elif answer == ('r'):
            answer = input(inverted('New requestor address:') + ' ').strip()
            if len(answer) == 0:
                if isinstance(contact, int):
                    requestor = ''
                else:
                    requestor = contact
            else:
                requestor = answer
            self.query_by_as(contact, requestor=requestor, feed=feed,
                             taxonomy=taxonomy)
            return
        elif answer != 's':
            error(red('Unknow command {!r}.'.format(answer)))
            self.query_by_as(contact, requestor=requestor, feed=feed,
                             taxonomy=taxonomy)
            return

        if text.startswith(str(red)):
            error(red('I won\'t send with a missing text!'))
            return
        self.save_to_rt(ids=ids, subject=subject, requestor=requestor,
                        csvfile=csvfile, body=text, feed=feed, taxonomy=taxonomy,
                        query=query)

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

    def save_to_rt(self, ids, subject, requestor, feed, taxonomy, csvfile, body, query):
        investigation_id = self.rt.create_ticket(Queue='Investigations',
                                                 Subject=subject,
                                                 Owner=self.config['rt']['user'],
                                                 Requestor=requestor)

        if investigation_id == -1:
            error(red('Could not create Investigation.'))
            return
        print(green('Created Investigation {}.'.format(investigation_id)))
        if not self.rt.edit_link(incident_id, 'HasMember', investigation_id):
            error(red('Could not link Investigation to Incident.'))
            return

        # TODO: CC
        correspond = self.rt.reply(investigation_id, text=body,
                                   files=[(filename, attachment, 'text/csv')])
        if not correspond:
            error(red('Could not correspond with text and file.'))
            return
        print(green('Correspondence added to Investigation.'))

        self.query_set_rtirid(events_ids=ids, rtir_id=investigation_id,
                              rtir_type='investigation')
        if not self.rt.edit_ticket(incident_id, Status='resolved'):
            error(red('Could not close incident {}.'.format(incident_id)))


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
