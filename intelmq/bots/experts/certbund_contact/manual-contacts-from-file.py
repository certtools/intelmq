#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
# Software engineering by Intevation GmbH
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/agpl.html>.
#
# Author(s):
#   Gernot Schulz <gernot.schulz@intevation.de>

import sys
import psycopg2
import csv
import argparse

NOTIFICATION_INTERVAL = 300
FORMAT_ID = 2

def get_automatic_org_name(cur, asn):
    # Get existing Org ID & name from _automatic tables
    cur.execute("""
            SELECT organisation_id from
            organisation_to_asn_automatic WHERE asn_id = %s;
            """,
        (asn,))
    result = cur.fetchall()
    org_id = result[0][0]
    cur.execute("SELECT name from organisation_automatic WHERE id = %s;",
            (org_id,))
    result = cur.fetchall()
    org_name = result[0][0]
    return cur, org_id, org_name

def add_contact(cur, asn, email, org_name=None):
    # Add AS number to manual table if necessary
    cur.execute("""
        SELECT EXISTS(SELECT number from autonomous_system WHERE number = %s);
        """,
            (asn,))
    result = cur.fetchall()
    exists = result[0][0]
    if not exists:
        # Insert AS into manual AS table
        cur.execute("INSERT INTO autonomous_system (number) VALUES (%s);",
                (asn,))

    # If no organization name was supplied, try to find it in the imported RIPE
    # data
    if not org_name:
        cur, org_id, org_name = get_automatic_org_name(cur, asn)
    print(org_name)

    # Check if a *manual* organization with the provided name exists, and use
    # it if possible; else add new manual organization
    cur.execute("SELECT id FROM organisation WHERE name = %s;", (org_name,))
    result = cur.fetchall()
    if result:
        org_id = result[0][0]
    else:
        cur.execute(
                "INSERT INTO organisation (name) VALUES (%s) RETURNING id;",
                (org_name,))
        result = cur.fetchall()
        org_id = result[0][0]

    # Check if a *manual* contact with the provided name exists, and use it if
    # possible; else add new manual contact
    cur.execute("SELECT id FROM contact WHERE email = %s;", (email,))
    result = cur.fetchall()
    if result:
        contact_id = result[0][0]
    else:
        cur.execute("""
            INSERT INTO contact (email,format_id) VALUES (%s,%s) RETURNING id;
            """, (email, FORMAT_ID))
        result = cur.fetchall()
        contact_id = result[0][0]

    # Add relations
    cur.execute("""
        SELECT EXISTS( SELECT (organisation_id,asn_id)
        FROM organisation_to_asn WHERE organisation_id = %s AND asn_id = %s);
        """, (org_id, asn))
    result = cur.fetchall()
    exists = result[0][0]
    if not exists:
        cur.execute("""
                INSERT INTO organisation_to_asn
                (organisation_id,asn_id,notification_interval)
                VALUES (%s, %s, %s);
                """, (org_id, asn, NOTIFICATION_INTERVAL))

    cur.execute("""
            SELECT EXISTS( SELECT (organisation_id,contact_id)
            FROM role WHERE organisation_id = %s AND contact_id = %s);
            """, (org_id, contact_id))
    result = cur.fetchall()
    exists = result[0][0]
    if not exists:
        cur.execute(
            "INSERT INTO role (organisation_id,contact_id) VALUES (%s, %s);",
            (org_id, contact_id))
    return cur

def parse_file(reader):
    list = []
    # AS|Email|Organisation name
    for row in reader:
        # E-Mail addresses may be comma-separated list
        for email in row[1].split(','):
            if len(row) == 3:
                list.append((row[0], email, row[2]))
            else:
                list.append((row[0], email, None))
    return list

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--conninfo",
                        default='dbname=contactdb',
                        help="Libpg connection string. E.g. 'host=localhost"
                            " port=5432 user=intelmq dbname=connectdb'"
                            " Default: 'dbname=contactdb'")
    parser.add_argument("--input", "-i",
                        help="Specify the input CSV file")
    args = parser.parse_args()

    with open(args.input) as f:
        reader = csv.reader(f, delimiter='|')
        parsed_list = parse_file(reader)

    con = None
    try:
        con = psycopg2.connect(dsn=args.conninfo)
        cur = con.cursor()

        for asn, email, org_name in parsed_list:
            cur = add_contact(cur, asn, email, org_name)

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
