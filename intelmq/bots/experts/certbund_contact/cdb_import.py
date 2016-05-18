#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO
# - LICENSE
# - Add options and/or agree on defaults: ttl, format_id
# - Handle overlapping manual and automatic IP ranges?

import csv
import psycopg2
import sys
from ipaddr import IPv4Address, IPv6Address, summarize_address_range # python3-ipaddr
import argparse

RIPE_RECORDS = []
DB_RECORDS   = []
ASN_CONTACTS = []

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
        action="store_true")
parser.add_argument("--database", help="Specify the Postgres DB")
parser.add_argument("--network-file", help="Specify the networks CSV file")
parser.add_argument("--asn-file", help="Specify the ASN CSV file")
args = parser.parse_args()

if args.asn_file:
    if args.verbose:
        print("Reading ASN CSV file...")
    with open(args.asn_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            ASN_CONTACTS.append(row)

if args.network_file:
    if args.verbose:
        print("Processing ripencc CSV file...")
    with open(args.network_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if row[0] == '2' or row[5] == 'summary':
                continue
            RIPE_RECORDS.append(row)
    for record in RIPE_RECORDS:
        if record[2] == "ipv4":
            first_ip = IPv4Address(record[3])
            # in network.csv comments ranges go only up to 254, so do '- 2' below?
            last_ip = IPv4Address(first_ip) + ( int(record[4]) - 1 )
            comment_string = "IPv4 " + str(first_ip) + ' - ' + str(last_ip)
            network = summarize_address_range(first_ip, last_ip)
            DB_RECORDS.append((str(network[0]), "false", comment_string))
        elif record[2] == "ipv6":
            first_ip = IPv6Address(record[3])
            ip_prefix = record[4]
            DB_RECORDS.append((str(first_ip) + '/' + ip_prefix, "false", ""))

con = None
try:
    con = psycopg2.connect("dbname='{}'".format(args.database))
    cur = con.cursor()

    if args.network_file:
        if args.verbose:
            print("Processing networks...")
        cur.execute("""
            DELETE FROM network WHERE is_manual = false;
            """)
        for record in DB_RECORDS:
            cur.execute("""
                SELECT count(id) from network
                WHERE address = '{}' AND is_manual = false;
                """.format(record[0]))
            result = cur.fetchone()
            if not result[0]:
                cur.execute("""
                    INSERT INTO network (address, is_manual, comment)
                    VALUES ('{}', {}, '{}');
                    """.format(record[0], record[1], record[2]))
        con.commit()

    if args.asn_file:
        if args.verbose:
            print("Processing contacts and ASN numbers...")
        for record in ASN_CONTACTS:
            # Email contacts
            cur.execute("""
                SELECT count(id) from contact
                WHERE email = $${}$$ AND is_manual = false;
                """.format(record[1]))
            result = cur.fetchone()
            if not result[0]:
                cur.execute("""
                    INSERT INTO contact (email, is_manual, format_id)
                    VALUES ($${}$$, false, 1)
                    RETURNING id;
                    """.format(record[1]))
            else:
                cur.execute("""
                    SELECT id from contact
                    WHERE email = $${}$$;
                    """.format(record[1]))
            result = cur.fetchone()
            contact_id = result[0]
            # ASN
            asn_id = record[0][2:]
            cur.execute("""
                SELECT count(number) from autonomous_system
                WHERE number = $${}$$ AND is_manual = false;
                """.format(asn_id))
            result = cur.fetchone()
            if not result[0]:
                cur.execute("""
                    INSERT INTO autonomous_system (number, is_manual)
                    VALUES ({}, false);
                    """.format(asn_id))
            # contact_to_asn
            cur.execute("""
                SELECT count(asn_id) from contact_to_asn
                WHERE asn_id = {};
                """.format(asn_id))
            result = cur.fetchone()
            if not result[0]:
                # TODO: default 60?
                cur.execute("""
                    INSERT INTO contact_to_asn (contact_id, asn_id, ttl)
                    VALUES ({}, {}, 60);
                    """.format(contact_id, asn_id))
            else:
                cur.execute("""
                    UPDATE contact_to_asn SET contact_id = {}
                    WHERE asn_id = {};
                    """.format(contact_id, asn_id))

    con.commit()
except psycopg2.DatabaseError as e:
    if con:
        con.rollback()
    print("Error {}".format(e))
    sys.exit(1)
finally:
    if con:
        con.close()

# vim: set et
