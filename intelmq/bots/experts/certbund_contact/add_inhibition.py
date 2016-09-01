#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of IntelMQ
# It is used to insert rules into the inhibition table
# of the certbund-contactdb expert
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

parser = argparse.ArgumentParser(description='''This script can be used to
insert rules into the inhibition table of the certBUND contact database.
It is not intended to be called automatically, e.g. by a cronjob.''')
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity",
                    default=False,
                    action="store_true")
parser.add_argument("--conninfo",
                    default='dbname=contactdb',
                    help="Libpg connection string. E.g. 'host=localhost"
                         " port=5432 user=intelmq dbname=connectdb'"
                         " Default: 'dbname=contactdb'")
parser.add_argument("--network",
                    default=None,
                    help="Specify the network as CIDR or IP-Address")
parser.add_argument("--asn",
                    default=None,
                    help="Specify the autonomous system number")
parser.add_argument("--ctype",
                    default=None,
                    help="Specify the classification.type")
parser.add_argument("--cidentifier",
                    default=None,
                    help="Specify the classification.identifier")
parser.add_argument("--comment",
                    default="",
                    help="Specify a comment")


def lookup_classification(cur, kind, value):
    if value is not None:
        cur.execute("SELECT id FROM classification_{} WHERE name = %s;"
                    .format(kind), (value,))
        result = cur.fetchall()
        if result:
            return result[0]
    return None


def lookup_or_create_as(cur, asn):
    if asn is not None:
        cur.execute("SELECT true FROM autonomous_system WHERE number = %s;",
                    (asn,))
        if bool(cur.fetchall()):
            return asn
        cur.execute("INSERT INTO autonomous_system (number, comment)"
                    " VALUES (%s, %s);",
                    (asn, "Created by add_inhibition.py"))
        return asn
    return None


def lookup_or_create_network(cur, network):
    if network is not None:
        cur.execute("SELECT id FROM network WHERE address = %s;", (network,))
        result = cur.fetchall()
        if result:
            return result[0]
        cur.execute("INSERT INTO network (address, comment) VALUES (%s, %s)"
                    " RETURNING id;",
                    (network, "Created by add_inhibition.py"))
        return cur.fetchall()[0]
    return None


def add_inhibition(cur, asn, network, ctype, cidentifier, comment):
    ctype_id = lookup_classification(cur, "type", ctype)
    cidentifier_id = lookup_classification(cur, "identifier", cidentifier)

    classification_ok = True
    if ctype is not None and ctype_id is None:
        classification_ok = False
        print("Could not find classification.type %r" % ctype, file=sys.stderr)
    if cidentifier is not None and cidentifier_id is None:
        classification_ok = False
        print("Could not find classification.identifier %r" % cidentifier,
              file=sys.stderr)
    if not classification_ok:
        sys.exit(1)

    asn_id = lookup_or_create_as(cur, asn)
    network_id = lookup_or_create_network(cur, network)

    cur.execute("INSERT INTO inhibition"
                " (asn_id, net_id, classification_type_id,"
                "  classification_identifier_id, comment)"
                " VALUES (%s, %s, %s, %s, %s);",
                (asn_id, network_id, ctype_id, cidentifier_id, comment))


def main():
    args = parser.parse_args()

    if args.asn is None and args.network is None:
        print("At least one of --asn and --network must be specified",
              file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print('Trying to insert data')
        print('---------------------')

    con = psycopg2.connect(dsn=args.conninfo)
    try:
        add_inhibition(con.cursor(), args.asn, args.network, args.ctype,
                       args.cidentifier, args.comment)
        con.commit()
    finally:
        con.close()


if __name__ == '__main__':
    main()
