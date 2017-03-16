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
import psycopg2
import argparse
import collections

import intelmq.bots.experts.certbund_contact.ripe_data as ripe_data


SOURCE_NAME = 'ripe'


def remove_old_entries(cur, verbose):
    """Remove the entries imported by previous runs."""
    if verbose:
        print('** Removing old entries from database...')
    cur.execute("DELETE FROM role_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))
    cur.execute("DELETE FROM organisation_to_asn_automatic"
                "      WHERE import_source = %s;", (SOURCE_NAME,))
    cur.execute("DELETE FROM autonomous_system_automatic"
                "      WHERE import_source = %s;", (SOURCE_NAME,))
    cur.execute("DELETE FROM organisation_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))
    cur.execute("DELETE FROM contact_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))
    cur.execute("DELETE FROM role_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))


def insert_new_asn_entries(cur, asn_list, verbose):
    if verbose:
        print('** Saving AS data to database...')
    for entry in asn_list:
        cur.execute("""INSERT INTO autonomous_system_automatic
                                   (number, import_source, import_time)
                            VALUES (%s, %s, CURRENT_TIMESTAMP);""",
                    (entry['aut-num'][0][2:], SOURCE_NAME))


def insert_new_organisations(cur, organisation_list, verbose):
    if verbose:
        print('** Saving organisation data to database...')

    mapping = collections.defaultdict(lambda: {'org_id': None,
                                               'contact_id': []})

    for entry in organisation_list:
        org_ripe_handle = entry['organisation'][0]
        org_name = entry['org-name'][0]

        cur.execute("""INSERT INTO organisation_automatic
                                   (name, ripe_org_hdl, import_source,
                                    import_time)
                            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                         RETURNING id;""",
                    (org_name, org_ripe_handle, SOURCE_NAME))
        org_id = cur.fetchone()[0]
        mapping[org_ripe_handle]['org_id'] = org_id

    return mapping


def insert_new_asn_org_entries(cur, org_to_asn, mapping):
    # many-to-many table organisation <-> as number
    for org_ripe_handle in mapping:
        org_id = mapping[org_ripe_handle]['org_id']

        if org_id is not None:
            for asn_id in org_to_asn[org_ripe_handle]:
                cur.execute("""
                INSERT INTO organisation_to_asn_automatic (
                                                    organisation_id,
                                                    asn_id,
                                                    import_source,
                                                    import_time)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
                """, (org_id, asn_id, SOURCE_NAME))


def insert_new_contact_entries(cur, role_list, abusec_to_org, mapping, verbose):
    if verbose:
        print('** Saving contacts data to database...')


    for entry in role_list:
        # "org" attribute of a role entry is optional,
        # thus we don't use it for now

        nic_hdl = entry['nic-hdl'][0]

        # abuse-mailbox: could be type LIST or occur multiple time
        # TODO: Check if we can handle LIST a@example, b@example
        email = entry['abuse-mailbox'][0]
        # For multiple lines: As not seen in ftp bulk data,
        # we only record if it happens as WARNING for now
        if len(entry['abuse-mailbox']) > 1:
            print('Role with nic-hdl {} has two '
                  'abuse-mailbox lines. Taking the first.'.format(nic_hdl))

        cur.execute("""
            INSERT INTO contact_automatic (email, import_source, import_time)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
            """, (email, SOURCE_NAME))
        contact_id = cur.fetchone()[0]

        for orh in abusec_to_org[nic_hdl]:
            mapping[orh]['contact_id'].append(contact_id)


def insert_new_roles(cur, mapping):
    for org_ripe_handle in mapping:
        org_id = mapping[org_ripe_handle]['org_id']
        contact_ids = mapping[org_ripe_handle]['contact_id']

        if org_id is None:
            continue

        for contact_id in contact_ids:
            cur.execute("""INSERT INTO role_automatic
                                       (organisation_id, contact_id,
                                        import_source, import_time)
                           VALUES (%s, %s, %s, CURRENT_TIMESTAMP);""",
                        (org_id, contact_id, SOURCE_NAME))


def main():
    parser = argparse.ArgumentParser(description='''This script can be used to import
automatic contact data to the certBUND contact database. It is intended to be
called automatically, e.g. by a cronjob.''')

    ripe_data.add_db_args(parser)
    ripe_data.add_common_args(parser)

    args = parser.parse_args()

    if args.verbose:
        print('Parsing RIPE database...')
        print('------------------------')

    (asn_list, organisation_list, role_list,
     org_to_asn, abusec_to_org) = ripe_data.load_ripe_files(args)

    con = None
    try:
        con = psycopg2.connect(dsn=args.conninfo)
        cur = con.cursor()

        remove_old_entries(cur, args.verbose)

        #
        # AS numbers
        #
        insert_new_asn_entries(cur, asn_list, args.verbose)

        #
        # Organisation
        #
        mapping = insert_new_organisations(cur, organisation_list, args.verbose)
        insert_new_asn_org_entries(cur, org_to_asn, mapping)

        #
        # Role
        #
        insert_new_contact_entries(cur, role_list, abusec_to_org, mapping,
                                   args.verbose)
        insert_new_roles(cur, mapping)

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
