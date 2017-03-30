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
    cur.execute("DELETE FROM organisation_to_asn_automatic"
                "      WHERE import_source = %s;", (SOURCE_NAME,))
    cur.execute("DELETE FROM organisation_to_network_automatic"
                "      WHERE import_source = %s;", (SOURCE_NAME,))
    cur.execute("DELETE FROM network_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))
    cur.execute("DELETE FROM contact_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))
    cur.execute("DELETE FROM organisation_automatic WHERE import_source = %s;",
                (SOURCE_NAME,))


def insert_new_network_entries(cur, network_list, key, verbose):
    """Insert the networks from network_list into the database.

    In some cases a single entry read from the RIPE data file may have
    to be stored as several entries in the network_automatic table
    because the address range can only be expressed by the union of
    severa network addresses in CIDR notation. This also means that some
    entries in the RIPE data for different ranges may need the same CIDR
    value as part of their network_automatic entries. This function will
    only create one entry in network_automatic in such cases.

    The return value contains maps organisation handles to the IDs of
    the network_automatic entries created by these functions, allowing
    to connect the network_automatic entries to the
    organisation_automatic entries.

    Args:
        network_list (list of dict): The list of dictionaries for the
            networks as returned by e.g. ripe_data.load_ripe_files.

        key (str): the key to use to lookup the network address in the
            dicts in network_list. Usually either 'inetnum' or
            'inet6num'.

        verbose (bool): If true, print some information about the data

    Return:
        A dictionary mapping organisation handles to lists of database
        IDs for the networks associated with the organisation
    """
    if verbose:
        print('** Saving {} data to database...'.format(key))
    net_org_map = collections.defaultdict(set)
    for entry in network_list:
        for addr in entry[key]:
            net_org_map[addr.compressed].add(entry["org"][0])

    org_net_map = collections.defaultdict(list)
    for addr, orgs in net_org_map.items():
        cur.execute("""INSERT INTO network_automatic
                                   (address, import_source, import_time)
                            VALUES (%s, %s, CURRENT_TIMESTAMP)
                       RETURNING network_automatic_id;""",
                    (addr, SOURCE_NAME))
        network_id = cur.fetchone()[0]
        for org in orgs:
            org_net_map[org].append(network_id)
    return org_net_map


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
                         RETURNING organisation_automatic_id;""",
                    (org_name, org_ripe_handle, SOURCE_NAME))
        org_id = cur.fetchone()[0]
        mapping[org_ripe_handle]['org_id'] = org_id

    return mapping


def insert_new_asn_org_entries(cur, asn_list, mapping):
    # many-to-many table organisation <-> as number
    for entry in asn_list:
        org_id = mapping[entry["org"][0]].get("org_id")
        if org_id is None:
            print("org_id None for AS organisation handle {!r}"
                  .format(entry["org"][0]))
            continue

        cur.execute("""INSERT INTO organisation_to_asn_automatic
                                   (organisation_automatic_id, asn,
                                    import_source, import_time)
                       VALUES (%s, %s, %s, CURRENT_TIMESTAMP);""",
                    (org_id, entry['aut-num'][0][2:], SOURCE_NAME))


def insert_new_network_org_entries(cur, org_net_mapping, mapping):
    # many-to-many table organisation <-> network number
    for org, networks in org_net_mapping.items():
        org_id = mapping[org].get("org_id")
        if org_id is None:
            print("org_id None for network entry {!r}".format((org, networks)))
            continue

        for network_id in networks:
            cur.execute("""INSERT INTO organisation_to_network_automatic
                                       (organisation_automatic_id,
                                        network_automatic_id,
                                        import_source, import_time)
                            VALUES (%s, %s, %s, CURRENT_TIMESTAMP);""",
                        (org_id, network_id, SOURCE_NAME))


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

        for orh in abusec_to_org[nic_hdl]:
            cur.execute("""INSERT INTO contact_automatic
                                       (email, organisation_automatic_id,
                                        import_source, import_time)
                           VALUES (%s, %s, %s, CURRENT_TIMESTAMP)""",
                        (email, mapping[orh]['org_id'], SOURCE_NAME))


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

    (asn_list, organisation_list, role_list, abusec_to_org, inetnum_list,
     inet6num_list) = ripe_data.load_ripe_files(args)

    ripe_data.convert_inetnum_to_networks(inetnum_list)
    ripe_data.convert_inet6num_to_networks(inet6num_list)

    con = None
    try:
        con = psycopg2.connect(dsn=args.conninfo)
        cur = con.cursor()

        remove_old_entries(cur, args.verbose)

        # network addresses
        org_inet6_mapping = insert_new_network_entries(
            cur, inet6num_list, "inet6num", args.verbose)
        org_inet_mapping = insert_new_network_entries(
            cur, inetnum_list, "inetnum", args.verbose)

        #
        # Organisation
        #
        mapping = insert_new_organisations(cur, organisation_list, args.verbose)

        # relate organisations to AS, networks, etc.
        insert_new_asn_org_entries(cur, asn_list, mapping)
        insert_new_network_org_entries(cur, org_inet6_mapping, mapping)
        insert_new_network_org_entries(cur, org_inet_mapping, mapping)

        #
        # Role
        #
        insert_new_contact_entries(cur, role_list, abusec_to_org, mapping,
                                   args.verbose)

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
