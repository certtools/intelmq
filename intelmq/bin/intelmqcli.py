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
import locale
import os
import readline  # nopep8, hooks into input()
import subprocess
import sys
import tempfile
import time
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
        old_print(*args, **kwargs)


# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

myinverted = str(reset) + str(inverted)
if six.PY2:
    input = raw_input


class IntelMQCLIContoller():
    table_mode = False  # for sticky table mode
    dryrun = False
    verbose = False
    batch = False
    compress_csv = False
    boilerplate = None
    zipme = False

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

        parser.add_argument('-z', '--zip', action='store_true',
                            help='Zip every events.csv attachement to an'
                                 'investigation for RT (defaults to false)')
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
        if args.zip:
            self.zipme = True

        self.config = lib.read_config()
        self.con, self.cur = lib.connect_database(config=self.config)
        self.rt = rt.Rt(self.config['rt']['uri'], self.config['rt']['user'],
                        self.config['rt']['password'])

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
            self.cur.execute(lib.QUERY_OPEN_TAXONOMIES)
            taxonomies = [x['classification.taxonomy'] for x in self.cur.fetchall()]
            print(taxonomies)
            for taxonomy in taxonomies:
                print('Handling taxonomy {!r}.'.format(taxonomy))
                self.cur.execute(lib.QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY, (taxonomy, ))
                report_ids = [x['rtir_report_id'] for x in self.cur.fetchall()]
                self.cur.execute(lib.QUERY_OPEN_EVENT_IDS_BY_TAXONOMY, (taxonomy, ))
                event_ids = [x['id'] for x in self.cur.fetchall()]
                subject = 'Incidents of {} on {}'.format(taxonomy, time.strftime('%Y-%m-%d'))

                incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                                    Owner=self.config['rt']['user'])
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
                self.cur.execute(lib.QUERY_DISTINCT_CONTACTS_BY_INCIDENT, (incident_id, ))
                contacts = [x['contacts'] for x in self.cur.fetchall()]
                for contact in contacts:
                    print('Handling contact ' + contact)
                    self.cur.execute(lib.QUERY_EVENTS_BY_ASCONTACT_INCIDENT,
                                     (incident_id, contact, ))
                    data = self.cur.fetchall()
                    self.send(taxonomy, contact, data, incident_id)

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
        keys = list(d[0].keys())
        empty = dict(zip(keys, [True] * len(keys)))
        for line in d:
            for key, value in line.items():
                if value is not None:
                    empty[key] = False
        return [{k: v for k, v in dicti.items() if not empty[k]} for dicti in d]

    def send(self, taxonomy, contact, query, incident_id, requestor=None):
        if not query:
            print(red('No data!'))
            return
        if not requestor:
            requestor = contact
        query = self.shrink_dict(query)
        ids = list(str(row['id']) for row in query)
        asns = set(str(row['source.asn']) for row in query)

        subject = ('{date}: {count} {tax} incidents for your AS {asns}'
                   ''.format(count=len(query),
                             date=datetime.datetime.now().strftime('%Y-%m-%d'),
                             asns=', '.join(asns),
                             tax=taxonomy))
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
                                quoting=csv.QUOTE_MINIMAL, delimiter=str(";"),
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        query_unicode = query
        if six.PY2:
            query = [{key: utils.encode(val) if isinstance(val, six.text_type) else val for key, val in row.items()} for row in query]
        writer.writerows(query)
        # note this might contain UTF-8 chars! let's ignore utf-8 errors. sorry.
        data = unicode(csvfile.getvalue(), 'utf-8')
        attachment_text = data.encode('ascii', 'ignore')
        attachment_lines = attachment_text.splitlines()

        if self.verbose:
            print(text)

        showed_text = '=' * 100 + '''
To: {to}
Subject: {subj}

{text}
    '''.format(to=requestor, subj=subject, text=text)
        showed_text_len = showed_text.count('\n')

        if self.table_mode and six.PY2:
            print(red('Sorry, no table mode for ancient python versions!'))
        elif self.table_mode and not six.PY2:
            if quiet:
                height = 80     # assume anything for quiet mode
            else:
                height = lib.getTerminalHeight() - 3 - showed_text_len
            csvfile.seek(0)
            if len(query) > height:
                with tempfile.NamedTemporaryFile(mode='w+') as handle:
                    handle.write(showed_text + '\n')
                    handle.write(tabulate.tabulate(query,
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
        automatic = False  # TODO: implement later
        if automatic and requestor:
            answer = 's'
        else:
            answer = 'q'
            if automatic:
                error(red('You need to set a valid requestor!'))
            if not self.batch:
                answer = input('{i}{b}[n]{i}ext, {i}{b}[s]{i}end, show {b}[t]{i}able,'
                               ' change {b}[r]{i}equestor or {b}[q]{i}uit?{r} '
                               ''.format(b=bold, i=myinverted, r=reset)).strip()
        if answer == 'q':
            exit(0)
        elif answer == 'n':
            return
        elif answer == 't':
            self.table_mode = bool((self.table_mode + 1) % 2)
            self.send(taxonomy, contact, query, incident_id, requestor)
            return
        elif answer == 'r':
            answer = input(inverted('New requestor address:') + ' ').strip()
            if len(answer) == 0:
                requestor = contact
            else:
                requestor = answer
            self.send(taxonomy, contact, query, incident_id, requestor)
            return
        elif answer != 's':
            error(red('Unknow command {!r}.'.format(answer)))
            self.send(taxonomy, contact, query, incident_id, requestor)
            return

        if text.startswith(str(red)):
            error(red('I won\'t send with a missing text!'))
            return
        self.save_to_rt(ids=ids, subject=subject, requestor=requestor,
                        body=text, taxonomy=taxonomy,
                        csvfile=csvfile, incident_id=incident_id)

        if requestor != contact and not self.dryrun:
            answer = input(inverted('Save recipient {!r} for ASNs {!s}? [Y/n] '
                                    ''.format(requestor,
                                              ', '.join(asns)))).strip()
            if answer.strip().lower() in ('', 'y', 'j'):
                self.query_update_contact(asns=asns, contact=requestor)
                if self.cur.rowcount == 0:
                    self.query_insert_contact(asns=asns, contact=requestor)

    def save_to_rt(self, ids, subject, requestor, taxonomy, body,
                   csvfile, incident_id):
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

        if self.zipme:
            attachment = io.BytesIO()
            ziphandle = zipfile.ZipFile(attachment, mode='w',
                                        compression=zipfile.ZIP_DEFLATED)
            data = csvfile.getvalue()
            data = unicode(data, 'utf-8')
            ziphandle.writestr('events.csv', data.encode('utf-8'))
            ziphandle.close()
            attachment.seek(0)
            filename = 'events.csv.zip'
            mimetype = 'application/octet-stream'
        else:
            attachment = csvfile
            attachment.seek(0)
            filename = 'events.csv'
            mimetype = 'text/csv'

        # TODO: CC
        correspond = self.rt.reply(investigation_id, text=body,
                                   files=[(filename, attachment, mimetype)])
        if not correspond:
            error(red('Could not correspond with text and file.'))
            return
        print(green('Correspondence added to Investigation.'))

        self.cur.executemany("UPDATE events SET rtir_investigation_id = %s, "
                             "sent_at = LOCALTIMESTAMP WHERE id = %s",
                             [(investigation_id, evid) for evid in ids])
        if not self.rt.edit_ticket(incident_id, Status='resolved'):
            error(red('Could not close incident {}.'.format(incident_id)))

    def query_update_contact(self, contact, asns):
        self.cur.executemany(lib.QUERY_UPDATE_CONTACT,
                             [(contact, asn) for asn in asns])

    def query_insert_contact(self, contact, asns):
        user = os.environ['USER']
        time = datetime.datetime.now().strftime('%c')
        comment = 'Added by {user} @ {time}'.format(user=user, time=time)
        self.cur.executemany(lib.QUERY_INSERT_CONTACT,
                             [(asn, contact, comment) for asn in asns])


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
