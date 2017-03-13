#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Example using ripe_data as module use to examine the ripe database.

  This file is part of intelMQ RIPE importer, see the license there.
"""

import sys

from ripe_data import parse_file


def main():
    asn_file = 'ripe.db.aut-num.gz'
    organisation_file = 'ripe.db.organisation.gz'
    role_file = 'ripe.db.role.gz'

    verbose = True

    asn_list = parse_file(asn_file,
                          ('aut-num', 'org', 'status'), 'aut-num', verbose)
    organisation_list = parse_file(organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'),
                                   verbose=verbose)
    role_list = parse_file(role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'), 'role', verbose)

    a = 'x.txt'
    asfilename = a
    print("Checking AS numbers from {}..".format(asfilename))

    as2org = {}

    with open(asfilename, 'rt') as f:
        for line in f:
            asn = int(line.strip())
            asns = "AS{}".format(asn)

            for a in asn_list:
                if a["aut-num"][0] == "AS{}".format(asn):
                    as2org[asn] = a["org"][0].upper()
                    print(a)

    for asn in as2org:
        for o in organisation_list:
            if o["organisation"][0] == as2org[asn]:
                print(o)

if __name__ == '__main__':
    main()
