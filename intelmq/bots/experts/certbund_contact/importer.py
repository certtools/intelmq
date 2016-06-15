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
import urllib

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity",
                    action="store_true")
parser.add_argument("--no-download",
                    help="Don't download files from RIPE, use local copy",
                    action="store_true")
parser.add_argument("--database",
                    help="Specify the Postgres DB")
parser.add_argument("--organisation-file",
                    default='ripe.db.organisation.gz',
                    help="Specify the ASN Set CSV file. Default: ripe.db.organisation.gz")
parser.add_argument("--role-file",
                    default='ripe.db.role.gz',
                    help="Specify the ASN Set CSV file. Default: ripe.db.role.gz")
parser.add_argument("--asn-file",
                    default='ripe.db.aut-num.gz',
                    help="Specify the ASN CSV file. Default: ripe.db.aut-num.gz")
args = parser.parse_args()


def download_file(filename):
    '''
    Downloads the given filename from RIPE and saves to disc
    :param filename: the filename to use, consult ftp://ftp.ripe.net/ripe/dbase/split/
                     for other possible names.
    '''
    ripe = urllib.URLopener()
    ripe.retrieve("ftp://ftp.ripe.net/ripe/dbase/split/{}".format(filename), filename)
    print('** Downloaded {0} '.format(filename))


def parse_file(filename, fields, index_field=None):
    '''
    Parses a (split) file from the RIPE database set

    ftp://ftp.ripe.net/ripe/dbase/split/
    :param filename: the gziped filename
    :param fields: the field name to read
    :param index_field: a field that occurs only once per dataset.
                        If not provided, the first element of 'fielfs' will be used
    :return: returns a list with the read out values as well as the number of entri
    '''
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
                # if tmp_field not in tmp.keys():
                if not tmp.get(tmp_field):
                    tmp[tmp_field] = []

            # Only add the fields we are interested in to the result set
            if key in fields:
                tmp[key].append(value)

    f.close()
    print('   -> read {0} entries'.format(len(out)))
    return out

def main():
    if not args.no_download:
        print('Downloading files...')
        download_file(args.role_file)
        download_file(args.organisation_file)
        download_file(args.asn_file)
    else:
        print('Not downloading files, using local copy...')
    print('')

    print('Parsing RIPE database...')
    print('------------------------')

    asn_list = parse_file(args.asn_file,
                          ('aut-num', 'org'),
                          'aut-num')
    role_list = parse_file(args.role_file,
                           ('nic-hdl', 'abuse-mailbox',),
                           'role')
    organisation_list = parse_file(args.organisation_file,
                                   ('organisation', 'org-name'))

    # Mapping dictionary that holds the database IDs between organisations,
    # contacts ans AS numbers
    mapping = {}

    con = None
    try:
        con = psycopg2.connect("dbname='{}'".format(args.database))
        cur = con.cursor()

        #
        # AS numbers
        #
        print('** Saving AS data to database...')
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

        cur.execute("DELETE FROM organisation_to_asn_automatic;")
        for org_ripe_handle in mapping:
            org_id = mapping[org_ripe_handle]['org_id']
            asn_ids = mapping[org_ripe_handle]['asn']

            if not org_id:
                continue

            # TODO: what should be the default for notification_interval?
            for asn_id in asn_ids:
                # print(org_id)
                cur.execute("""
                INSERT INTO organisation_to_asn_automatic (notification_interval, organisation_id, asn_id)
                VALUES (180, %s, %s);
                """, (org_id, asn_id))

        #
        # Role
        #
        print('** Saving contacts data to database...')
        cur.execute("DELETE FROM contact_automatic;")
        for entry in role_list:
            # No all entries have email contact
            if not entry or not entry.get('abuse-mailbox'):
                continue
            email = entry['abuse-mailbox'][0]
            org_ripe_handle = entry['nic-hdl'][0]

            cur.execute("""
                INSERT INTO contact_automatic (format_id, email)
                VALUES (1, %s)
                RETURNING id;
                """, (email, ))
            result = cur.fetchone()
            contact_id = result[0]


            if org_ripe_handle and mapping.get(org_ripe_handle):
                mapping[org_ripe_handle]['contact_id'] = contact_id
            else:
                pass
                # print('count not find org handle {0}'.format(org_ripe_handle))

            #
            # mapping['contacts'][ripe_org_handle] = contact_id

        # many-to-many table organisation <-> contact
        cur.execute("DELETE FROM role_automatic;")
        # for entry in mapping['orgs']:
        #     print(orgs)
        #     # cur.execute("""
        #     #     INSERT INTO role_automatic (organisation_id, contact_id)
        #     #     VALUES (%s, %s);
        #     #     """, (email, ))

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
