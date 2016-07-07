#!/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of intelMQ RIPE importer.
#
# intelMQ RIPE importer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# intelMQ RIPE importer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import sys
import gzip
import psycopg2
import argparse

parser = argparse.ArgumentParser(description='''This script can be used to import
automatic contact data to the certBUND contact database. It is intended to be
called automatically, e.g. by a cronjob.''')
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity",
                    default=False,
                    action="store_true")
parser.add_argument("--database",
                    default='contactdb',
                    help="Specify the Postgres DB. Default: contactdb")
parser.add_argument("--organisation-file",
                    default='ripe.db.organisation.gz',
                    help="Specify the organisation data file. Default: ripe.db.organisation.gz")
parser.add_argument("--role-file",
                    default='ripe.db.role.gz',
                    help="Specify the contact role data file. Default: ripe.db.role.gz")
parser.add_argument("--asn-file",
                    default='ripe.db.aut-num.gz',
                    help="Specify the AS number data file. Default: ripe.db.aut-num.gz")
parser.add_argument("--notification-format",
                    default='feed_specific',
                    help="Specify the data format the contacts linked with e.g. csv. Default: feed_specific")
parser.add_argument("--notification-interval",
                    default='0',
                    help="Specify the default notification intervall in seconds. Default: 0")
args = parser.parse_args()


def parse_file(filename, fields, index_field=None):
    '''
    Parses a file from the RIPE (split) database set

    ftp://ftp.ripe.net/ripe/dbase/split/
    :param filename: the gziped filename
    :param fields: the field name to read
    :param index_field: a field that occurs only once per dataset.
                        If not provided, the first element of 'fielfs' will be used
    :return: returns a list with the read out values as well as the number of entri
    '''
    if args.verbose:
        print('** Reading file {0}'.format(filename))

    out = []
    tmp = {}
    f = gzip.open(filename, 'rt', encoding='latin1')
    if not index_field:
        index_field = fields[0]

    important_fields = list(fields) + [index_field]
    for line in f:

        # Comments and remarks
        if line.startswith('%') or line.startswith('#') or line.startswith('remarks:'):
            continue

        if ":" in line:
            key, value = [x.strip() for x in line.split(":", 1)]

            # Fields we are interested in, plus the index
            if key not in important_fields:
                continue

            # If we reach the index again, we have reached the next dataset, add
            # the previous data and start again
            if key == index_field:
                out.append(tmp)
                tmp = {}

            for tmp_field in fields:
                if not tmp.get(tmp_field):
                    tmp[tmp_field] = []

            # Only add the fields we are interested in to the result set
            if key in fields:
                tmp[key].append(value)

    f.close()
    if args.verbose:
        print('   -> read {0} entries'.format(len(out)))
    return out


def main():
    if args.verbose:
        print('Parsing RIPE database...')
        print('------------------------')

    asn_list = parse_file(args.asn_file,
                          ('aut-num', 'org'),
                          'aut-num')
    role_list = parse_file(args.role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'),
                           'role')
    organisation_list = parse_file(args.organisation_file,
                                   ('organisation', 'org-name'))

    # Mapping dictionary that holds the database IDs between organisations,
    # contacts and AS numbers. This needs to be done here because we can't
    # use the RIPE org-ids.
    mapping = {}

    con = None
    try:
        con = psycopg2.connect("dbname='{}'".format(args.database))
        cur = con.cursor()

        if args.verbose:
            print('** Looking for %s' % (args.notification_format, ))

        cur.execute("SELECT id FROM format WHERE name = %s",
                    (args.notification_format, ))
        result = cur.fetchall()

        if result:
            notification_fid = result[0]
        else:
            print('The notification format %s could not be determined'
                  % (args.notification_format, ))
            sys.exit(1)

        #
        # AS numbers
        #
        if args.verbose:
            print('** Saving AS data to database...')
        cur.execute("DELETE FROM role_automatic;")
        cur.execute("DELETE FROM organisation_to_template_automatic;")
        cur.execute("DELETE FROM organisation_to_asn_automatic;")
        cur.execute("DELETE FROM autonomous_system_automatic;")
        for entry in asn_list:
            if not entry or not entry.get('aut-num') or not entry.get('org'):
                continue
            as_number = entry['aut-num'][0][2:]
            org_ripe_handle = entry['org'][0]

            cur.execute("""
                INSERT INTO autonomous_system_automatic (number)
                VALUES (%s);
                """, (as_number, ))

            if not mapping.get(org_ripe_handle):
                mapping[org_ripe_handle] = {'org_id': None,
                                            'contact_id': [],
                                            'asn': []}
            mapping[org_ripe_handle]['asn'].append(as_number)

        #
        # Organisation
        #
        if args.verbose:
            print('** Saving organisation data to database...')
        cur.execute("DELETE FROM organisation_automatic;")
        for entry in organisation_list:
            # Not all entries have an organisation associated
            if not entry:
                continue
            org_name = entry['org-name'][0]
            org_ripe_handle = entry['organisation'][0]

            cur.execute("""
                INSERT INTO organisation_automatic (name, ripe_org_hdl)
                VALUES (%s, %s) RETURNING id;
                """, (org_name, org_ripe_handle))
            result = cur.fetchone()
            org_id = result[0]

            if not mapping.get(org_ripe_handle):
                mapping[org_ripe_handle] = {'org_id': None,
                                            'contact_id': [],
                                            'asn': []}
            mapping[org_ripe_handle]['org_id'] = org_id

        # many-to-many table organisation <-> as number
        for org_ripe_handle in mapping:
            org_id = mapping[org_ripe_handle]['org_id']
            asn_ids = mapping[org_ripe_handle]['asn']

            if not org_id:
                continue

            for asn_id in asn_ids:
                cur.execute("""
                INSERT INTO organisation_to_asn_automatic (notification_interval,
                                                           organisation_id,
                                                           asn_id)
                VALUES (%s, %s, %s);
                """, (args.notification_interval, org_id, asn_id))

        #
        # Role
        #
        if args.verbose:
            print('** Saving contacts data to database...')

        cur.execute("DELETE FROM contact_automatic;")

        for entry in role_list:
            # No all entries have email contact
            if not entry or not entry.get('abuse-mailbox'):
                continue
            try:
                org_ripe_handle = entry['org'][0]
            except IndexError:
                org_ripe_handle = None
            email = entry['abuse-mailbox'][0]

            cur.execute("""
                INSERT INTO contact_automatic (format_id, email)
                VALUES (%s, %s)
                RETURNING id;
                """, (notification_fid,email, ))
            result = cur.fetchone()
            contact_id = result[0]

            if org_ripe_handle and mapping.get(org_ripe_handle):
                mapping[org_ripe_handle]['contact_id'].append(contact_id)

        # many-to-many table organisation <-> contact
        cur.execute("DELETE FROM role_automatic;")
        for org_ripe_handle in mapping:
            org_id = mapping[org_ripe_handle]['org_id']
            contact_ids = mapping[org_ripe_handle]['contact_id']

            # Not all contacts from RIPE are connected to an organisation, some
            # for example are only responsible for a network.
            if not org_id:
                continue

            for contact_id in contact_ids:
                cur.execute("""
                INSERT INTO role_automatic (organisation_id, contact_id)
                VALUES (%s, %s);
                """, (org_id, contact_id))

        # Commit all data
        con.commit()
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print("Error {}".format(e))
        sys.exit(1)
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    main()
