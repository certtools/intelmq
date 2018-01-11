#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Example using ripe_data as module to examine the ripe database.

  This file is part of intelMQ RIPE importer.


Copyright (C):
  2016, 2017, 2018 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This program is Free Software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/agpl.html>.

Author(s):
    Bernhard E. Reiter <bernhard.reiter@intevation.de>
"""

import sys

from ripe_data import parse_file


def main():
    asn_file = 'ripe.db.aut-num.gz'
    organisation_file = 'ripe.db.organisation.gz'
    role_file = 'ripe.db.role.gz'

    verbose = True

    asn_list = parse_file(asn_file,
                          ('aut-num', 'org', 'status', 'abuse-c'),
                          verbose=verbose)
    organisation_list = parse_file(organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'),
                                   verbose=verbose)
    role_list = parse_file(role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'), 'role',
                           verbose=verbose)

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

    print("aut-num records without org but with abuse-c attribute:")
    for asn in asn_list:
        if not asn.get("org") and asn.get("abuse-c"):
            print(asn)

if __name__ == '__main__':
    main()
