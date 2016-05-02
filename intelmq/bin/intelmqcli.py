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


# wrapper around print()
def quietprint(*args, **kwargs):
    if not quiet:
        print(*args, **kwargs)


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
    filter_asns = []

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

        self.read_config()
        self.connect_database()

        if args.list_feeds:
            self.cur.execute(lib.QUERY_FEED_NAMES)
            for row in self.cur.fetchall():
                if row['feed.name']:
                    quietprint(row['feed.name'])
            exit(0)

        if args.list_texts:
            self.cur.execute(lib.QUERY_TEXT_NAMES)
            for row in self.cur.fetchall():
                if row['key']:
                    quietprint(row['key'])
            exit(0)

        if args.list_identifiers:
            self.cur.execute(lib.QUERY_IDENTIFIER_NAMES)
            for row in self.cur.fetchall():
                if row['classification.identifier']:
                    quietprint(row['classification.identifier'])
            exit(0)

        if args.list_taxonomies:
            self.cur.execute(lib.QUERY_TAXONOMY_NAMES)
            for row in self.cur.fetchall():
                if row['classification.taxonomy']:
                    quietprint(row['classification.taxonomy'])
            exit(0)

        if args.list_types:
            self.cur.execute(lib.QUERY_TYPE_NAMES)
            for row in self.cur.fetchall():
                if row['classification.type']:
                    quietprint(row['classification.type'])
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
            quietprint('Logged in as {} on {}.'.format(self.config['rt']['user'],
                                                       self.config['rt']['uri']))
        try:
            answer = 'init'
            while answer != 'q':
                asn_count = self.count_by_asn(feed=args.feed,
                                              taxonomy=args.taxonomy)
                if self.verbose:
                    error('asn_count = {}.'.format(asn_count))
                if self.batch and answer != 'q':
                    answer = 'a'
                else:
                    answer = input('{i}detailed view by id, {b}[a]{i}utomatic '
                                   'sending, {b}[q]{i}uit?{r} '
                                   ''.format(b=bold, i=myinverted,
                                             r=reset)).strip()
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
                                             feed=args.feed,
                                             taxonomy=args.taxonomy)
                        else:
                            if item['asn']:
                                self.query_by_as(int(item['asn']), automatic=True,
                                                 feed=args.feed,
                                                 taxonomy=args.taxonomy)
                            else:
                                error(red('Can not query the data of an unknown ASN. Ignoring.'))
                    answer = 'q'
                elif not self.batch and isinstance(answer, int):
                    if asn_count[answer]['contacts']:
                        self.query_by_as(asn_count[answer]['contacts'],
                                         feed=args.feed,
                                         taxonomy=args.taxonomy)
                    else:
                        if asn_count[answer] and asn_count[answer]['asn']:
                            self.query_by_as(int(asn_count[answer]['asn']),
                                             feed=args.feed,
                                             taxonomy=args.taxonomy)
                        else:
                            error(red('no ASNs known. Ignoring.'))
                else:
                    error(red('Unknown answer {!r}.'.format(answer)))

        except BaseException as exc:
            if isinstance(exc, (SystemExit, KeyboardInterrupt)):
                pass
            else:
                raise
        finally:
            self.rt.logout()

    def read_config(self):
        with open('/etc/intelmq/intelmqcli.conf') as conf_handle:
            self.config = json.load(conf_handle)
        home = os.path.expanduser("~")      # needed for OSX
        with open(os.path.expanduser(home + '/.intelmq/intelmqcli.conf')) as conf_handle:
            user_config = json.load(conf_handle)

        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value

        self.rt = rt.Rt(self.config['rt']['uri'], self.config['rt']['user'],
                        self.config['rt']['password'])

    def connect_database(self):
        self.con = psycopg2.connect(database=self.config['database']['database'],
                                    user=self.config['database']['user'],
                                    password=self.config['database']['password'],
                                    host=self.config['database']['host'],
                                    port=self.config['database']['port'],
                                    sslmode=self.config['database']['sslmode'],
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

    def query_by_as(self, contact, requestor=None, automatic=False, feed='%',
                    taxonomy='%'):
        if isinstance(contact, int):
            query = self.query_by_asnum(contact, feed, taxonomy)
            if requestor is None:
                requestor = ''
        else:
            query = self.query_by_ascontact(contact, feed, taxonomy)
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
        quietprint(repr(lib.CSV_FIELDS))
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
            quietprint(text)

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
                quietprint(showed_text,
                           tabulate.tabulate(query_unicode, headers='keys',
                                             tablefmt='psql'), sep='\n')
        else:
            if quiet:
                height = 80
            else:
                height = lib.getTerminalHeight() - 4
            if 5 + len(query) > height:  # cut query too, 5 is length of text
                quietprint('\n'.join(showed_text.splitlines()[:5]))
                quietprint('...')
                quietprint('\n'.join(attachment_lines[:height - 5]))
                quietprint('...')
            elif showed_text_len + len(query) > height > 5 + len(query):
                quietprint('\n'.join(showed_text.splitlines()[:height - len(query)]))
                quietprint('...')
                quietprint(attachment_text)
            else:
                quietprint(showed_text, attachment_text, sep='\n')
        quietprint('-' * 100)
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
        if True:
            self.save_to_rt(ids=ids, subject=subject, requestor=requestor,
                            csvfile=csvfile, body=text, feed=feed, taxonomy=taxonomy)
        else:  # TODO: Config option for single events (best in ascontacts db)
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
                           ''.format(date=subj_date,
                                     type=row['classification.type'],
                                     target=lib.target_from_row(row)))
                self.save_to_rt(ids=(id_, ), subject=subject,
                                requestor=requestor, feed=feed, taxonomy=taxonomy, csvfile=csvfile,
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

    def save_to_rt(self, ids, subject, requestor, feed, taxonomy, csvfile, body):
        if self.dryrun:
            quietprint('Not writing to RT, dry-run selected.')
            return

        if taxonomy == '%':
            taxonomy='Unknown'

        report_id = self.rt.create_ticket(Queue='Incident Reports',
                                          Subject=subject,
                                          Owner=self.config['rt']['user'])
        if report_id == -1:
            error(red('Could not create Incident Report.'))
            return
        quietprint(green('Created Incident Report {}.'.format(report_id)))
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

        if self.verbose:
            error("save_to_rt: feed = {}".format(feed))
            error("save_to_rt: taxonomy = {}".format(taxonomy))
        incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                            Owner=self.config['rt']['user'])
        if incident_id == -1:
            error(red('Could not create Incident ({}).'.format(incident_id)))
            return
        # XXX TODO: distinguish between national and other constituencies
        self.rt.edit_ticket(incident_id, CF__RTIR_Classification=taxonomy,
                            CF__RTIR_Constituency='national',
                            CF__RTIR_Function='IncidentCoord')
        quietprint(green('Created Incident {}.'.format(incident_id)))
        if not self.rt.edit_link(report_id, 'MemberOf', incident_id):
            error(red('Could not link Incident to Incident Report: ({} -> {}).'.format(incident_id, report_id)))
            return
        self.query_set_rtirid(events_ids=ids, rtir_id=incident_id,
                              rtir_type='incident')
        investigation_id = self.rt.create_ticket(Queue='Investigations',
                                                 Subject=subject,
                                                 Owner=self.config['rt']['user'],
                                                 Requestor=requestor)

        if investigation_id == -1:
            error(red('Could not create Investigation.'))
            return
        quietprint(green('Created Investigation {}.'.format(investigation_id)))
        if not self.rt.edit_link(incident_id, 'HasMember', investigation_id):
            error(red('Could not link Investigation to Incident.'))
            return

        # TODO: CC
        correspond = self.rt.reply(investigation_id, text=body,
                                   files=[(filename, attachment, 'text/csv')])
        if not correspond:
            error(red('Could not correspond with text and file.'))
            return
        quietprint(green('Correspondence added to Investigation.'))

        self.query_set_rtirid(events_ids=ids, rtir_id=investigation_id,
                              rtir_type='investigation')
        if not self.rt.edit_ticket(incident_id, Status='resolved'):
            error(red('Could not close incident {}.'.format(incident_id)))

    def count_by_asn(self, feed='%', taxonomy='%'):
        # TODO: Existing RT ids!
        asn_count = self.query_count_asn(feed, taxonomy)
        if not asn_count:
            quietprint('No incidents!')
            exit(0)
        headers = map(bold, ['id', 'n°', 'ASNs', 'contacts', 'types', 'feeds'])
        tabledata = []
        for number, row in enumerate(asn_count):
            tabledata.append([number, row['count'], row['asn'],
                              row['contacts'], row['classification'],
                              row['feeds']])
        quietprint(tabulate.tabulate(tabledata, headers=headers, tablefmt='psql'))

        quietprint('{} incidents for {} contacts.'
                   ''.format(sum((row['count'] for row in asn_count)),
                             len(asn_count)))
        return asn_count

    def query_by_ascontact(self, contact, feed='%', taxonomy='%'):
        query = lib.QUERY_BY_ASCONTACT.format(evtab=self.config['database']['events_table'],
                                              cc=self.config['filter']['cc'],
                                              conttab=self.config['database']['contacts_table'])
        self.cur.execute(query, (self.config['filter']['fqdn'], contact, feed,
                                 taxonomy))
        return self.cur.fetchall()

    def query_by_asnum(self, asn, feed, taxonomy='%'):
        query = lib.QUERY_BY_ASNUM.format(evtab=self.config['database']['events_table'],
                                          cc=self.config['filter']['cc'],
                                          conttab=self.config['database']['contacts_table'])
        self.cur.execute(query, (self.config['filter']['fqdn'], asn, feed,
                                 taxonomy))
        return self.cur.fetchall()

    def query_count_asn(self, feed, taxonomy='%'):
        query = lib.QUERY_COUNT_ASN.format(evtab=self.config['database']['events_table'],
                                           cc=self.config['filter']['cc'],
                                           conttab=self.config['database']['contacts_table'])
        quietprint("query = '%r'" %query)
        self.cur.execute(query, (self.config['filter']['fqdn'], feed, taxonomy))
        return self.cur.fetchall()

    def query_set_rtirid(self, events_ids, rtir_id, rtir_type):
        query = lib.QUERY_SET_RTIRID.format(evtab=self.config['database']['events_table'],
                                            rtirid=rtir_id, type=rtir_type,
                                            ids=','.join(events_ids))
        self.cur.execute(query)

    def query_update_contact(self, contact, asns):
        query = lib.QUERY_UPDATE_CONTACT.format(conttab=self.config['database']['contacts_table'],
                                                ids=','.join(asns))
        self.cur.execute(query, (contact, ))

    def query_insert_contact(self, contact, asn, comment):
        query = lib.QUERY_INSERT_CONTACT.format(conttab=self.config['database']['contacts_table'])
        self.cur.execute(query, (asn, contact, comment))

    def query_get_text(self, text_id):
        self.cur.execute(lib.QUERY_GET_TEXT.format(texttab=self.config['database']['text_table']),
                         (text_id, ))


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
