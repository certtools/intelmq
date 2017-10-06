#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show differences between RIPE data files and database.


Copyright (C) 2016, 2017 by Bundesamt für Sicherheit in der Informationstechnik
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
    Bernhard Herzog <bernhard.herzog@intevation.de>
"""

import sys
import argparse
import ipaddress
from enum import Enum

import psycopg2

import intelmq.bots.experts.certbund_contact.common as common
import intelmq.bots.experts.certbund_contact.ripe_data as ripe_data


SOURCE_NAME = "ripe"


def extract_asn(aut_entry):
    return int(aut_entry['aut-num'][0][2:])


class Organisation:

    def __init__(self, handle, name, asns=(), networks=(), contacts=()):
        self.handle = handle
        self.name = name
        self.asns = list(asns)
        self.networks = list(networks)
        self.contacts = list(contacts)


def build_organisation_objects(asn_list, inetnum_list, inet6num_list,
                               organisation_list, role_list, role_to_org):

    orgs = {entry["organisation"][0]: Organisation(entry["organisation"][0],
                                                   entry['org-name'][0])
            for entry in organisation_list}

    unattached_as = []
    for aut in asn_list:
        org_handle = aut["org"][0]
        org = orgs.get(org_handle)
        if org is not None:
            org.asns.append(extract_asn(aut))
        else:
            unattached_as.append(aut)

    for key, netnums in [("inetnum", inetnum_list),
                         ("inet6num", inet6num_list)]:
        for net in netnums:
            org_handle = net["org"][0]
            org = orgs.get(org_handle)
            if org is not None:
                org.networks.extend(net[key])

    unattached_roles = []
    for role in role_list:
        role_orgs = role_to_org[role['nic-hdl'][0]]
        if not role_orgs:
            unattached_roles.append(role)
        else:
            for org_handle in role_orgs:
                orgs[org_handle].contacts.append(role['abuse-mailbox'][0])

    return orgs, unattached_as, unattached_roles


def build_organisation_objects_from_db(cur):
    cur.execute("""
    SELECT o.ripe_org_hdl, o.name,
           ARRAY(SELECT oa.asn
                   FROM organisation_to_asn_automatic oa
                  WHERE oa.organisation_automatic_id
                        = o.organisation_automatic_id),
           ARRAY(SELECT text(n.address)
                   FROM network_automatic n
                   JOIN organisation_to_network_automatic orgn
                     ON n.network_automatic_id = orgn.network_automatic_id
                  WHERE orgn.organisation_automatic_id
                        = o.organisation_automatic_id),
           ARRAY(SELECT c.email
                   FROM contact_automatic c
                  WHERE c.organisation_automatic_id
                        = o.organisation_automatic_id)
      FROM organisation_automatic o
     WHERE o.import_source = %s;
    """, (SOURCE_NAME,))

    orgs = {}
    while True:
        row = cur.fetchone()
        if row is None:
            break
        org_handle, name, asns, networks, contacts = row
        orgs[org_handle] = Organisation(org_handle, name, asns,
                                        [ipaddress.ip_network(addr)
                                         for addr in networks],
                                        contacts)

    return orgs


def compare_sets(a, b):
    return (a - b, a & b, b - a)


def compare_dicts(a, b):
    return compare_sets(a.keys(), b.keys())


def item_list_changes(plural_name, old, new):
    removed, both, added = compare_sets(set(old), set(new))
    if removed:
        yield plural_name + " removed: " + ", ".join(map(str, removed))
    if added:
        yield plural_name + " added: " + ", ".join(map(str, added))


def organisation_changes(handles, orgs_a, orgs_b):
    for handle in handles:
        a = orgs_a[handle]
        b = orgs_b[handle]

        changes = []
        if a.name != b.name:
            changes.append("Name changed from %r to %r" % (a.name, b.name))
        changes.extend(item_list_changes("ASNs", a.asns, b.asns))
        changes.extend(item_list_changes("networks", a.networks, b.networks))
        changes.extend(item_list_changes("contacts", a.contacts, b.contacts))
        if changes:
            yield handle, changes

# Enumeration to roughly indicate the type of change.
Change = Enum("Change", "removed modified added")


def find_overlaid_manual_entries(cur, org, change):
    formatted = ", ".join(["AS{}".format(asn) for asn in org.asns]
                          + [str(net) for net in org.networks])
    if not formatted:
        return

    if change == Change.removed:
        msg = "        Info: this entry was responsible for {formatted}"
    elif change in (Change.modified, Change.added):
        msg = "        Info: this entry will be responsible for {formatted}"
    else:
        raise ValueError("Unexpeced change value: {!r}".format(change))

    print(msg.format(formatted=formatted))

    for asn in org.asns:
        results = common.lookup_by_manual_asn(cur, asn)
        if results:
            print("        AS{} via manual db entries resolves to:".format(asn))
            for result in results:
                print("            {}".format(result))

    for net in org.networks:
        results = common.lookup_by_manual_network(cur, net)
        if results:
            print("        {} via manual db entries resolves to:".format(net))
            for result in results:
                print("            {}".format(result))


def compare_orgs(cur, old_orgs, new_orgs):
    removed, both, added = compare_dicts(old_orgs, new_orgs)

    if added:
        print("organisations to be added:")
        for handle in added:
            print("    %s: %r" % (handle, new_orgs[handle].name,))
            find_overlaid_manual_entries(cur, new_orgs[handle], Change.added)

    if removed:
        print("organisations to be deleted:")
        for handle in removed:
            print("    %s: %r" % (handle, old_orgs[handle].name,))
            find_overlaid_manual_entries(cur, old_orgs[handle], Change.removed)

    if both:
        all_changes = list(organisation_changes(both, old_orgs, new_orgs))
        if all_changes:
            print("Changed organisations:")
            for handle, changes in all_changes:
                if old_orgs[handle].name == new_orgs[handle].name:
                    print("    %s: %r" % (handle, new_orgs[handle].name,))
                else:
                    print("    %r: %s -> %s" % (handle, old_orgs[handle].name,
                                                new_orgs[handle].name))
                for change in changes:
                    print("        %s" % (change,))
                find_overlaid_manual_entries(cur, new_orgs[handle],
                                             Change.modified)


def compare_unattached(name, old, new):
    removed, both, added = compare_sets(set(old), set(new))
    if removed:
        print("Unattached %s to be removed:" % (name,))
        for item in sorted(removed):
            print("    ", item)
    if added:
        print("Unattached %s to be added:" % (name,))
        for item in sorted(added):
            print("    ", item)


def compare_orgs_with_db(cur, asn_list, inetnum_list, inet6num_list,
                         organisation_list, role_list, abusec_to_org):
    orgs, unattached_as, unattached_roles = \
        build_organisation_objects(asn_list, inetnum_list, inet6num_list,
                                   organisation_list, role_list, abusec_to_org)
    db_orgs = build_organisation_objects_from_db(cur)
    compare_orgs(cur, db_orgs, orgs)


def main():
    parser = argparse.ArgumentParser(
        description=("Show the differences between a set of RIPE DB files"
                     " and the contents of the database."))

    ripe_data.add_db_args(parser)
    ripe_data.add_common_args(parser)

    options = parser.parse_args()

    (asn_list, organisation_list, role_list, abusec_to_org, inetnum_list,
     inet6num_list) = ripe_data.load_ripe_files(options)

    ripe_data.convert_inetnum_to_networks(inetnum_list)
    ripe_data.convert_inet6num_to_networks(inet6num_list)

    con = psycopg2.connect(dsn=options.conninfo)
    try:
        compare_orgs_with_db(con.cursor(), asn_list, inetnum_list,
                             inet6num_list, organisation_list, role_list,
                             abusec_to_org)
    finally:
        con.close()


if __name__ == '__main__':
    main()
