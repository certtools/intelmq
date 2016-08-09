#!/usr/bin/env python3
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
parser.add_argument("--conninfo",
                    default='dbname=contactdb',
                    help="Libpg connection string. E.g. 'host=localhost"
                         " port=5432 user=intelmq dbname=connectdb'"
                         " Default: 'dbname=contactdb'")
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
parser.add_argument("--asn-whitelist-file",
                    default='',
                    help="A file name with a whitelist of ASNs. If this option is not set, all ASNs are imported")

#TODO: move parsing of arguments into the main() block to avoid while being
# executed during import
args = parser.parse_args()

SOURCE_NAME = 'ripe'


def read_asn_whitelist():
    out = []
    if args.asn_whitelist_file:
        with open(args.asn_whitelist_file) as f:
            out = [line.strip() for line in f]

            if args.verbose and out:
                print('** Loaded {} entries from ASN whitelist {}'.format(len(out),
                                                                          args.asn_whitelist_file))
    return out


def parse_file(filename, fields, index_field=None):
    '''Parses a file from the RIPE (split) database set.

    ftp://ftp.ripe.net/ripe/dbase/split/
    :param filename: the gziped filename
    :param fields: the field names to read
    :param index_field: the field that marks the beginning of a dataset.
        If not provided, the first element of 'fields' will be used
    :return: returns a list of lists with the read out values

    NOTE: Does **not** handle "continuation lines" (see rfc2622 section 2).

    NOTE: Preserves the contents of the fields like lower and upper case
          characters, though the RPSL is case insensitive and ASCII only.
          Thus for some fields it makes sense to upper() them (before
          comparing).
    '''
    if args.verbose:
        print('** Reading file {0}'.format(filename))

    out = []
    tmp = None

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
                if tmp: # template is filled, except on the first record
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

    # Load ASN whitelist
    asn_whitelist = read_asn_whitelist()

    asn_list = parse_file(args.asn_file, ('aut-num', 'org'), 'aut-num')
    organisation_list = parse_file(args.organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'))
    role_list = parse_file(args.role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'), 'role')

    # Mapping dictionary that holds the database IDs between organisations,
    # contacts and AS numbers. This needs to be done here because we can't
    # use the RIPE org-ids.
    mapping = {}

    # Mapping from abuse-c to organisation
    abuse_c_organisation = {}


    con = None
    try:
        con = psycopg2.connect(dsn=args.conninfo)
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
        cur.execute("DELETE FROM role_automatic WHERE import_source = %s;", (SOURCE_NAME,))
        cur.execute("DELETE FROM organisation_to_template_automatic WHERE import_source = %s;", (SOURCE_NAME,))
        cur.execute("DELETE FROM organisation_to_asn_automatic WHERE import_source = %s;", (SOURCE_NAME,))
        cur.execute("DELETE FROM autonomous_system_automatic WHERE import_source = %s;", (SOURCE_NAME,))

        for entry in asn_list:
            if not entry or not entry.get('aut-num') or not entry.get('org'):
                continue

            # Only
            if args.asn_whitelist_file and entry['aut-num'][0] not in asn_whitelist:
                continue

            as_number = entry['aut-num'][0][2:]
            org_ripe_handle = entry['org'][0].upper()

            cur.execute("""
                INSERT INTO autonomous_system_automatic (number, import_source, import_time)
                VALUES (%s, %s, CURRENT_TIMESTAMP);
                """, (as_number, SOURCE_NAME ))

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
        cur.execute("DELETE FROM organisation_automatic WHERE import_source = %s;", (SOURCE_NAME,))
        for entry in organisation_list:
            org_ripe_handle = entry['organisation'][0].upper()
            org_name = entry['org-name'][0]
            abuse_c = entry['abuse-c'][0].upper() if entry['abuse-c'] else None

            cur.execute("""
                INSERT INTO organisation_automatic (name, ripe_org_hdl, import_source, import_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP) RETURNING id;
                """, (org_name, org_ripe_handle, SOURCE_NAME))
            result = cur.fetchone()
            org_id = result[0]

            if abuse_c:
                abuse_c_organisation.setdefault(abuse_c,
                                                []).append(org_ripe_handle)

            if not mapping.get(org_ripe_handle):
                mapping[org_ripe_handle] = {'org_id': None,
                                            'contact_id': [],
                                            'asn': []}
            mapping[org_ripe_handle]['org_id'] = org_id

        # many-to-many table organisation <-> as number
        for org_ripe_handle in mapping:
            org_id = mapping[org_ripe_handle]['org_id']
            asn_ids = mapping[org_ripe_handle]['asn']

            if org_id is not None:
                for asn_id in asn_ids:
                    cur.execute("""
                    INSERT INTO organisation_to_asn_automatic (
                                                        notification_interval,
                                                        organisation_id,
                                                        asn_id,
                                                        import_source,
                                                        import_time)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
                    """, (args.notification_interval, org_id,
                          asn_id, SOURCE_NAME))

        #
        # Role
        #
        if args.verbose:
            print('** Saving contacts data to database...')

        cur.execute("DELETE FROM contact_automatic WHERE import_source = %s;", (SOURCE_NAME,))

        for entry in role_list:
            # Sanity check.
            # abuse-mailbox is mandatory for a role used in abuse-c.
            if not entry.get('abuse-mailbox'):
                continue

            # "org" attribute of a role entry is optional,
            # thus we don't use it for now

            nic_hdl = entry['nic-hdl'][0].upper()

            # abuse-mailbox: could be type LIST or occur multiple time
            # TODO: Check if we can handle LIST a@example, b@example
            email = entry['abuse-mailbox'][0]
            # For multiple lines: As not seen in ftp bulk data, 
            # we only record if it happens as WARNING for now
            if len(entry['abuse-mailbox'])>1:
                print('Role with nic-hdl {} has two '
                      'abuse-mailbox lines. Taking the first.'.format(nic_hdl))

            cur.execute("""
                INSERT INTO contact_automatic (format_id, email, import_source, import_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id;
                """, (notification_fid, email, SOURCE_NAME))
            result = cur.fetchone()
            contact_id = result[0]

            for orh in abuse_c_organisation.get(nic_hdl, []):
                mapping[orh]['contact_id'].append(contact_id)


        # many-to-many table organisation <-> contact
        cur.execute("DELETE FROM role_automatic WHERE import_source = %s;", (SOURCE_NAME,))

        for org_ripe_handle in mapping:
            org_id = mapping[org_ripe_handle]['org_id']
            contact_ids = mapping[org_ripe_handle]['contact_id']

            if org_id is None:
                continue

            for contact_id in contact_ids:
                cur.execute("""
                INSERT INTO role_automatic (organisation_id, contact_id, import_source, import_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
                """, (org_id, contact_id, SOURCE_NAME))

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
