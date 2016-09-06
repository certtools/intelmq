#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implemented workarounds for old packages:
    BytesIO instead of StringIO on Python 2 for csv module

TODO: Implement automatic mode
"""
from __future__ import print_function, unicode_literals

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

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import six
import tabulate
from termstyle import bold, green, inverted, red, reset

import intelmq.lib.intelmqcli as lib
from intelmq.lib import utils

# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

error = partial(print, file=sys.stderr)
quiet = False
old_print = print


def print(*args, **kwargs):
    if not quiet:
        old_print(*args, **kwargs)


myinverted = str(reset) + str(inverted)
if six.PY2:
    input = raw_input


class IntelMQCLIContoller(lib.IntelMQCLIContollerTemplate):
    appname = 'intelmqcli'
    usage = lib.USAGE
    epilog = lib.EPILOG
    table_mode = False  # for sticky table mode
    dryrun = False
    verbose = False
    batch = False
    compress_csv = False
    boilerplate = None
    zipme = False

    def init(self):
        self.parser.add_argument('-l', '--list-feeds', action='store_true',
                                 help='List all feeds')
        self.parser.add_argument('-i', '--list-identifiers', action='store_true',
                                 help='List all identifiers')
        self.parser.add_argument('-L', '--list-texts', action='store_true',
                                 help='List all existing texts.')
        self.parser.add_argument('-t', '--text', nargs=1, help='Specify the text to be used.')
        self.parser.add_argument('-T', '--list-taxonomies', action='store_true',
                                 help='List all taxonomies')
        self.parser.add_argument('-y', '--list-types', action='store_true',
                                 help='List all types')

        self.parser.add_argument('-c', '--compress-csv', action='store_true',
                                 help='Automatically compress/shrink the attached CSV report if fields are empty (default = False).')

        self.parser.add_argument('-z', '--zip', action='store_true',
                                 help='Zip every events.csv attachement to an '
                                      'investigation for RT (defaults to false)')
        self.setup()

        if self.args.quiet:
            global quiet
            quiet = True
        if self.args.compress_csv:
            self.compress_csv = True
        if self.args.text:
            self.boilerplate = self.args.text
        if self.args.zip:
            self.zipme = True

        self.connect_database()

        if self.args.list_feeds:
            self.execute(lib.QUERY_FEED_NAMES)
            for row in self.cur.fetchall():
                if row['feed.name']:
                    print(row['feed.name'])
            exit(0)

        if self.args.list_texts:
            self.execute(lib.QUERY_TEXT_NAMES)
            for row in self.cur.fetchall():
                if row['key']:
                    print(row['key'])
            exit(0)

        if self.args.list_identifiers:
            self.execute(lib.QUERY_IDENTIFIER_NAMES)
            for row in self.cur.fetchall():
                if row['classification.identifier']:
                    print(row['classification.identifier'])
            exit(0)

        if self.args.list_taxonomies:
            self.execute(lib.QUERY_TAXONOMY_NAMES)
            for row in self.cur.fetchall():
                if row['classification.taxonomy']:
                    print(row['classification.taxonomy'])
            exit(0)

        if self.args.list_types:
            self.execute(lib.QUERY_TYPE_NAMES)
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
            self.execute(lib.QUERY_OPEN_TAXONOMIES)
            taxonomies = [x['classification.taxonomy'] for x in self.cur.fetchall()]
            print("All taxonomies: " + ",".join(taxonomies))
            for taxonomy in taxonomies:
                print('Handling taxonomy {!r}.'.format(taxonomy))
                self.execute(lib.QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY, (taxonomy, ))
                report_ids = [x['rtir_report_id'] for x in self.cur.fetchall()]
                self.execute(lib.QUERY_OPEN_EVENT_IDS_BY_TAXONOMY, (taxonomy, ))
                event_ids = [x['id'] for x in self.cur.fetchall()]
                subject = ('%s %s incidents of %s'
                           '' % (len(event_ids), taxonomy, time.strftime('%Y-%m-%d')))

                if self.dryrun:
                    print('Dry run: Skipping creation of incident.')
                    continue

                incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                                    Owner=self.config['rt']['user'])
                if incident_id == -1:
                    error('Could not create Incident ({}).'.format(incident_id))
                    continue
                else:
                    print(green('Created Incident %s.' % incident_id))
                # XXX TODO: distinguish between national and other constituencies
                self.rt.edit_ticket(incident_id, CF__RTIR_Classification=taxonomy,
                                    CF__RTIR_Constituency='national',
                                    CF__RTIR_Function='IncidentCoord')

                for report_id in report_ids:
                    if not self.rt.edit_link(report_id, 'MemberOf', incident_id):
                        error(red('Could not link Incident to Incident Report: ({} -> {}).'.format(incident_id, report_id)))
                        continue
                self.executemany("UPDATE events SET rtir_incident_id = %s WHERE id = %s",
                                 [(incident_id, event_id) for event_id in event_ids])
                print(green('Linked events to incident.'))

                self.execute(lib.QUERY_DISTINCT_CONTACTS_BY_INCIDENT, (incident_id, ))
                contacts = [x['source.abuse_contact'] for x in self.cur.fetchall()]
                for contact in contacts:
                    print('Handling contact ' + contact)
                    self.execute(lib.QUERY_EVENTS_BY_ASCONTACT_INCIDENT,
                                 (incident_id, contact, ))
                    data = self.cur.fetchall()
                    try:
                        self.send(taxonomy, contact, data, incident_id)
                    except IndexError:
                        # Bug in RT/python-rt
                        pass

        finally:
            self.rt.logout()

    def query_get_text(self, text_id):
        self.execute(lib.QUERY_GET_TEXT.format(texttab=self.config['database']['text_table']),
                     (text_id, ),
                     extend=False)

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

        ### PREPARATION
        query = self.shrink_dict(query)
        ids = list(str(row['id']) for row in query)

        subject = ('{date}: {count} {tax} incidents for your network'
                   ''.format(count=len(query),
                             date=datetime.datetime.now().strftime('%Y-%m-%d'),
                             tax=taxonomy))
        text = self.get_text(taxonomy)
        if six.PY2:
            csvfile = io.BytesIO()
        else:
            csvfile = io.StringIO()
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
        data = unicode(csvfile.getvalue(), 'utf-8')  # TODO: PY2 only
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

        ### SHOW DATA
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

        ### MENU
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

        ### INVESTIGATION
        subject = ('%s %s incidents in your network: %s'
                   ''% (len(query), taxonomy, time.strftime('%Y-%m-%d')))
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

        ### CORRESPOND
        filename = '%s-%s.csv' % (time.strftime('%Y-%m-%d'), taxonomy)
        if self.zipme or len(query) > self.config['rt']['zip_threshold']:
            attachment = io.BytesIO()
            ziphandle = zipfile.ZipFile(attachment, mode='w',
                                        compression=zipfile.ZIP_DEFLATED)
            data = csvfile.getvalue()
            data = unicode(data, 'utf-8')  # TODO: PY2 only
            ziphandle.writestr('events.csv', data.encode('utf-8'))
            ziphandle.close()
            attachment.seek(0)
            filename += '.zip'
            mimetype = 'application/octet-stream'
        else:
            attachment = csvfile
            attachment.seek(0)
            mimetype = 'text/csv'

        # TODO: CC
        correspond = self.rt.reply(investigation_id, text=text,
                                   files=[(filename, attachment, mimetype)])
        if not correspond:
            error(red('Could not correspond with text and file.'))
            return
        print(green('Correspondence added to Investigation.'))

        self.executemany("UPDATE events SET rtir_investigation_id = %s, "
                         "sent_at = LOCALTIMESTAMP WHERE id = %s",
                         [(investigation_id, evid) for evid in ids])
        print(green('Linked events to investigation.'))

        ### RESOLVE
        if not self.rt.edit_ticket(incident_id, Status='resolved'):
            error(red('Could not close incident {}.'.format(incident_id)))
        if requestor != contact and not self.dryrun:
            asns = set(str(row['source.asn']) for row in query)
            answer = input(inverted('Save recipient {!r} for ASNs {!s}? [Y/n] '
                                    ''.format(requestor,
                                              ', '.join(asns)))).strip()
            if answer.strip().lower() in ('', 'y', 'j'):
                self.executemany(lib.QUERY_UPDATE_CONTACT,
                                 [(requestor, asn) for asn in asns])
                if self.cur.rowcount == 0:
                    self.query_insert_contact(asns=asns, contact=requestor)

    def query_insert_contact(self, contact, asns):
        user = os.environ['USER']
        time = datetime.datetime.now().strftime('%c')
        comment = 'Added by {user} @ {time}'.format(user=user, time=time)
        self.executemany(lib.QUERY_INSERT_CONTACT,
                         [(asn, contact, comment) for asn in asns])


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
