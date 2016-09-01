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
parser.add_argument("--asn"
                    default=None,
                    help="Specify the autonomous system number")
parser.add_argument("--ctype",
                    default=None,
                    help="Specify the classification.type")
parser.add_argument("--cidentifier",
                    default=None,
                    help="Specify the classification.identifier")
parser.add_argument("--comment",
                    default=None,
                    help="Specify a comment")

TABLENAME = "inhibition"
CTTABLENAME = "classification_type"
CITABLENAME = "classification_identifier"


def main():
    args = parser.parse_args()
    if args.verbose:
        print('Trying to insert data')
        print('---------------------')

    con = None
    try:
        con = psycopg2.connect(dsn=args.conninfo)
        cur = con.cursor()

        cidentifier_id = None
        ctype_id = None
        asn_id = None
        network_id = None

        # Type
        if args.ctype:
            if args.verbose:
                print('** Determining the ID of the classification type %s'
                      % (args.ctype, ))

            cur.execute("SELECT id FROM %s WHERE name = %s",
                        (CTTABLENAME, args.ctype, ))
            result = cur.fetchall()

            if not result or not result.size() == 1:
                ctype_id = result[0]
                result = None
            else:
                print('The classification type %s could not be determined'
                      % (args.ctype, ))
                if con:
                    con.close()
                sys.exit(1)

        # Identifier
        if args.cidentifier:
            if args.verbose:
                print('** Determining the ID of the classification identifier '
                      '%s' % (args.cidentifier, ))

            cur.execute("SELECT id FROM %s WHERE name = %s",
                        (CITABLENAME, args.cidentifier, ))
            result = cur.fetchall()

            if not result or not result.size() == 1:
                cidentifier_id = result[0]
                result = None
            else:
                print('The classification identifier %s could not be '
                      'determined' % (args.cidentifier, ))
                if con:
                    con.close()
                sys.exit(1)

        # IP / CIDR
        if args.network:
            if args.verbose:
                print('** Determining the ID of the network %s'
                      % (args.network, ))

            # TODO Does this need to order by Network Size??
            cur.execute("SELECT id FROM %s WHERE address <<= %s",
                        ("network", args.network, ))
            result = cur.fetchall()

            if not result:
                network_id = result[0]
                result = None
            else:
                print('The network %s could not be determined'
                      % (args.network, ))
                if con:
                    con.close()
                sys.exit(1)

        # ASN
        if args.asn:
            if args.verbose:
                print('** Determining the ID of the autonomous system %s'
                      % (args.cidentifier, ))

            # TODO is this correct?
            cur.execute("SELECT number FROM %s WHERE ripe_aut_num = %s",
                        ("autonomous_system", args.cidentifier, ))
            result = cur.fetchall()

            if not result or not result.size() == 1:
                asn_id = result[0]
                result = None
            else:
                print('The classification type %s could not be determined'
                      % (args.cidentifier, ))
                if con:
                    con.close()
                sys.exit(1)

        if asn_id or network_id or cidentifier_id or ctype_id:
            if args.verbose:
                print('** All set, we are inserting now...')
            cur.execute("INSERT into %s (asn_id, net_id, "
                        "classification_type_id, classification_identifier_id"
                        ", comment) VALUES (%s, %s, %s, %s, %s)",
                        (TABLENAME, asn_id, network_id, ctype_id,
                        cidentifier_id, comment, ))

        else:
            print('** I don\'t know what I should insert. Exiting.')
            if con:
                con.close()
            sys.exit(1)

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
