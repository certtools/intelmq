#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implemented workarounds for old packages:
    BytesIO instead of StringIO on Python 2 for csv module
"""
from __future__ import print_function, unicode_literals

import csv
import datetime
import io
import locale
import os
import readline  # nopep8, hooks into input()
import subprocess
import tempfile
import zipfile

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import six
import tabulate
from termstyle import bold, inverted, reset

import intelmq.lib.intelmqcli as lib
from intelmq.lib import utils

# Use unicode for all input and output, needed for Py2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


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
                                 help='Automatically compress/shrink the attached CSV report if'
                                      ' fields are empty (default = False).')
        self.parser.add_argument('-z', '--zip', action='store_true',
                                 help='Zip every events.csv attachement to an '
                                      'investigation for RT (defaults to false)')
        self.setup()

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
                    self.logger.info(row['feed.name'])
            exit(0)

        if self.args.list_texts:
            self.execute(lib.QUERY_TEXT_NAMES)
            for row in self.cur.fetchall():
                if row['key']:
                    self.logger.info(row['key'])
            exit(0)

        if self.args.list_identifiers:
            self.execute(lib.QUERY_IDENTIFIER_NAMES)
            for row in self.cur.fetchall():
                if row['classification.identifier']:
                    self.logger.info(row['classification.identifier'])
            exit(0)

        if self.args.list_taxonomies:
            self.execute(lib.QUERY_TAXONOMY_NAMES)
            for row in self.cur.fetchall():
                if row['classification.taxonomy']:
                    self.logger.info(row['classification.taxonomy'])
            exit(0)

        if self.args.list_types:
            self.execute(lib.QUERY_TYPE_NAMES)
            for row in self.cur.fetchall():
                if row['classification.type']:
                    self.logger.info(row['classification.type'])
            exit(0)

        if locale.getpreferredencoding() != 'UTF-8':
            self.logger.error('The preferred encoding of your locale setting is not UTF-8 '
                              'but {}. Exiting.'.format(locale.getpreferredencoding()))
            exit(1)

        if not self.rt.login():
            self.logger.error('Could not login as {} on {}.'.format(self.config['rt']['user'],
                                                                    self.config['rt']['uri']))
            exit(2)
        else:
            self.logger.info('Logged in as {} on {}.'.format(self.config['rt']['user'],
                                                             self.config['rt']['uri']))
        try:
            self.execute(lib.QUERY_OPEN_TAXONOMIES)
            taxonomies = [x['classification.taxonomy'] for x in self.cur.fetchall()]
            self.logger.info("All taxonomies: " + ",".join(taxonomies))
            for taxonomy in taxonomies:
                self.logger.info('Handling taxonomy {!r}.'.format(taxonomy))
                if taxonomy not in lib.SUBJECT or lib.SUBJECT[taxonomy] is None:
                    self.logger.error('No subject defined for %r.' % taxonomy)
                    continue
                self.execute(lib.QUERY_OPEN_EVENT_REPORTS_BY_TAXONOMY, (taxonomy, ))
                report_ids = [x['rtir_report_id'] for x in self.cur.fetchall()]
                self.execute(lib.QUERY_OPEN_EVENT_IDS_BY_TAXONOMY, (taxonomy, ))
                event_ids = [x['id'] for x in self.cur.fetchall()]
                subject = ('%s %s incidents on %s'
                           '' % (len(event_ids), lib.SUBJECT[taxonomy],
                                 datetime.datetime.now().strftime('%Y-%m-%d')))

                if self.dryrun:
                    self.logger.info('Simulate creation of incident.')
                    incident_id = -1
                else:
                    incident_id = self.rt.create_ticket(Queue='Incidents', Subject=subject,
                                                        Owner=self.config['rt']['user'])
                    if incident_id == -1:
                        self.logger.error('Could not create Incident ({}).'.format(incident_id))
                        continue

                    self.logger.info('Created Incident %s.' % incident_id)
                    # XXX TODO: distinguish between national and other constituencies
                    self.rt.edit_ticket(incident_id, CF__RTIR_Classification=taxonomy,
                                        CF__RTIR_Constituency='national',
                                        CF__RTIR_Function='IncidentCoord')

                for report_id in report_ids:
                    if not self.dryrun and not self.rt.edit_link(report_id, 'MemberOf', incident_id):
                        self.logger.error('Could not link Incident to Incident Report: ({} -> {}).'
                                          ''.format(incident_id, report_id))
                        continue

                self.executemany("UPDATE events SET rtir_incident_id = %s WHERE id = %s",
                                 [(incident_id, event_id) for event_id in event_ids])
                self.con.commit()
                self.logger.info('Linked events to incident.')

                if not self.dryrun:
                    self.execute(lib.QUERY_DISTINCT_CONTACTS_BY_INCIDENT, (incident_id, ))
                else:
                    self.execute(lib.DRY_QUERY_DISTINCT_CONTACTS_BY_TAXONOMY, (taxonomy, ))

                contacts = [x['source.abuse_contact'] for x in self.cur.fetchall()]
                inv_results = []

                for contact in contacts:
                    self.logger.info('Handling contact ' + contact)
                    if not self.dryrun:
                        self.execute(lib.QUERY_EVENTS_BY_ASCONTACT_INCIDENT,
                                     (incident_id, contact, ))
                    else:
                        self.execute(lib.DRY_QUERY_EVENTS_BY_ASCONTACT_TAXONOMY,
                                     (taxonomy, contact, ))
                    data = self.cur.fetchall()
                    inv_results.append(self.send(taxonomy, contact, data, incident_id))

                if all(inv_results):
                    try:
                        if not self.dryrun and not self.rt.edit_ticket(incident_id,
                                                                       Status='resolved'):
                            self.logger.error('Could not close incident {}.'.format(incident_id))
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
                self.logger.error('Default text not found!')
                return None

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
            self.logger.error('No data!')
            return False
        if not requestor:
            requestor = contact

        # PREPARATION
        query = self.shrink_dict(query)
        ids = list(str(row['id']) for row in query)

        subject = ('{count} {tax} in your network: {date}'
                   ''.format(count=len(query),
                             date=datetime.datetime.now().strftime('%Y-%m-%d'),
                             tax=lib.SUBJECT[taxonomy]))
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
            query = [{key: utils.encode(val) if isinstance(val, six.text_type) else val for key, val in row.items()}
                     for row in query]
        writer.writerows(query)
        # note this might contain UTF-8 chars! let's ignore utf-8 errors. sorry.
        if six.PY2:
            data = unicode(csvfile.getvalue(), 'utf-8')
        else:
            data = csvfile.getvalue()
        attachment_text = data.encode('ascii', 'ignore')
        attachment_lines = attachment_text.splitlines()

        if self.verbose:
            self.logger.info(text)

        showed_text = '=' * 100 + '''
To: {to}
Subject: {subj}

{text}
    '''.format(to=requestor, subj=subject, text=text)
        showed_text_len = showed_text.count('\n')

        # SHOW DATA
        if self.table_mode and six.PY2:
            self.logger.error('Sorry, no table mode for ancient python versions!')
        elif self.table_mode and not six.PY2:
            if self.quiet:
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
                self.logger.info(showed_text)
                self.logger.info(tabulate.tabulate(query_unicode, headers='keys',
                                                   tablefmt='psql'))
        else:
            if self.quiet:
                height = 80
            else:
                height = lib.getTerminalHeight() - 4
            if 5 + len(query) > height:  # cut query too, 5 is length of text
                self.logger.info('\n'.join(showed_text.splitlines()[:5]))
                self.logger.info('...')
                self.logger.info('\n'.join(attachment_lines[:height - 5]))
                self.logger.info('...')
            elif showed_text_len + len(query) > height > 5 + len(query):
                self.logger.info('\n'.join(showed_text.splitlines()[:height - len(query)]))
                self.logger.info('...')
                self.logger.info(attachment_text)
            else:
                self.logger.info(showed_text)
                self.logger.info(attachment_text)
        self.logger.info('-' * 100)

        # MENU
        if self.batch and requestor:
            answer = 's'
        else:
            answer = 'q'
            if self.batch:
                self.logger.error('You need to set a valid requestor!')
            else:
                answer = input('{i}{b}[a]{i}utomatic, {b}[n]{i}ext, {i}{b}[s]{i}end, show '
                               '{b}[t]{i}able, change {b}[r]{i}equestor or {b}[q]{i}uit?{r} '
                               ''.format(b=bold, i=myinverted, r=reset)).strip()
        if answer == 'q':
            exit(0)
        elif answer == 'n':
            return False
        elif answer == 'a':
            self.batch = True
        elif answer == 't':
            self.table_mode = bool((self.table_mode + 1) % 2)
            return self.send(taxonomy, contact, query, incident_id, requestor)
        elif answer == 'r':
            answer = input(inverted('New requestor address:') + ' ').strip()
            if len(answer) == 0:
                requestor = contact
            else:
                requestor = answer
            return self.send(taxonomy, contact, query, incident_id, requestor)
        elif answer != 's':
            self.logger.error('Unknow command {!r}.'.format(answer))
            return self.send(taxonomy, contact, query, incident_id, requestor)

        if text is None:
            self.logger.error('I won\'t send with a missing text!')
            return False

        # INVESTIGATION
        if self.dryrun:
            self.logger.info('Simulate creation of investigation.')
            investigation_id = -1
        else:
            investigation_id = self.rt.create_ticket(Queue='Investigations',
                                                     Subject=subject,
                                                     Owner=self.config['rt']['user'],
                                                     Requestor=requestor)

            if investigation_id == -1:
                self.logger.error('Could not create Investigation.')
                return False

            self.logger.info('Created Investigation {}.'.format(investigation_id))
            if not self.rt.edit_link(incident_id, 'HasMember', investigation_id):
                self.logger.error('Could not link Investigation to Incident.')
                return False

        # CORRESPOND
        filename = '%s-%s.csv' % (datetime.datetime.now().strftime('%Y-%m-%d'), taxonomy)
        if self.zipme or len(query) > self.config['rt']['zip_threshold']:
            attachment = io.BytesIO()
            ziphandle = zipfile.ZipFile(attachment, mode='w',
                                        compression=zipfile.ZIP_DEFLATED)
            data = csvfile.getvalue()
            if six.PY2:
                data = unicode(data, 'utf-8')
            ziphandle.writestr('events.csv', data.encode('utf-8'))
            ziphandle.close()
            attachment.seek(0)
            filename += '.zip'
            mimetype = 'application/octet-stream'
        else:
            attachment = csvfile
            attachment.seek(0)
            mimetype = 'text/csv'

        try:
            # TODO: CC
            if self.dryrun:
                self.logger.info('Simulate creation of correspondence.')
            else:
                correspond = self.rt.reply(investigation_id, text=text,
                                           files=[(filename, attachment, mimetype)])
                if not correspond:
                    self.logger.error('Could not correspond with text and file.')
                    return False
                self.logger.info('Correspondence added to Investigation.')

            self.executemany("UPDATE events SET rtir_investigation_id = %s, "
                             "sent_at = LOCALTIMESTAMP WHERE id = %s",
                             [(investigation_id, evid) for evid in ids])
            self.logger.info('Linked events to investigation.')
        except:
            self.con.rollback()
            raise
        else:
            self.con.commit()

            # RESOLVE
            try:
                if not self.dryrun and not self.rt.edit_ticket(investigation_id,
                                                               Status='resolved'):
                    self.logger.error('Could not close investigation {}.'.format(incident_id))
            except IndexError:
                # Bug in RT/python-rt
                pass

        if requestor != contact:
            asns = set(str(row['source.asn']) for row in query)
            answer = input(inverted('Save recipient {!r} for ASNs {!s}? [Y/n] '
                                    ''.format(requestor,
                                              ', '.join(asns)))).strip()
            if answer.strip().lower() in ('', 'y', 'j'):
                self.executemany(lib.QUERY_UPDATE_CONTACT,
                                 [(requestor, asn) for asn in asns])
                self.con.commit()
                if self.cur.rowcount == 0:
                    self.query_insert_contact(asns=asns, contact=requestor)

        return True

    def query_insert_contact(self, contact, asns):
        user = os.environ['USER']
        time = datetime.datetime.now().strftime('%c')
        comment = 'Added by {user} @ {time}'.format(user=user, time=time)
        self.executemany(lib.QUERY_INSERT_CONTACT,
                         [(asn, contact, comment) for asn in asns])
        self.con.commit()


def main():
    IntelMQCLIContoller()

if __name__ == '__main__':
    main()
