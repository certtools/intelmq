#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse

import psycopg2

from intelmq.bots.experts.certbund_contact.ripe_data import parse_file, \
     sanitize_asn_list, sanitize_role_list, sanitize_organisation_list, \
     org_to_asn_mapping, role_to_org_mapping


SOURCE_NAME = "ripe"


def load_ripe_files(options):
    asn_list = parse_file(options.asn_file,
                          ('aut-num', 'org', 'status'),
                          verbose=options.verbose)
    organisation_list = parse_file(options.organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'),
                                   verbose=options.verbose)
    role_list = parse_file(options.role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'), 'role',
                           verbose=options.verbose)

    return (sanitize_asn_list(asn_list),
            sanitize_organisation_list(organisation_list),
            sanitize_role_list(role_list))


def extract_asn(aut_entry):
    return int(aut_entry['aut-num'][0][2:])


class Organisation:

    def __init__(self, handle, name, asns=(), contacts=()):
        self.handle = handle
        self.name = name
        self.asns = list(asns)
        self.contacts = list(contacts)


def build_organisation_objects(asn_list, organisation_list, role_list):
    role_to_org = role_to_org_mapping(organisation_list)

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
           ARRAY(SELECT oa.asn_id
                   FROM organisation_to_asn_automatic oa
                  WHERE oa.organisation_id = o.id),
           ARRAY(SELECT c.email
                   FROM contact_automatic c
                   JOIN role_automatic r ON r.contact_id = c.id
                  WHERE r.organisation_id = o.id)
      FROM organisation_automatic o
     WHERE o.import_source = %s;
    """, (SOURCE_NAME,))

    orgs = {}
    while True:
        row = cur.fetchone()
        if row is None:
            break
        org_handle, name, asns, contacts = row
        orgs[org_handle] = Organisation(org_handle, name, asns, contacts)

    return orgs


def get_unattached_asns_from_db(cur):
    cur.execute("""
    SELECT a.number
      FROM autonomous_system_automatic a
     WHERE a.import_source = %s
       AND NOT EXISTS (SELECT * FROM organisation_to_asn_automatic oa
                        WHERE oa.asn_id = a.number);
    """, (SOURCE_NAME,))
    return [row[0] for row in cur.fetchall()]


def get_unattached_contacts_from_db(cur):
    cur.execute("""
    SELECT c.email
      FROM contact_automatic c
     WHERE c.import_source = %s
       AND NOT EXISTS (SELECT * FROM role_automatic r
                        WHERE r.contact_id = c.id);
    """, (SOURCE_NAME,))
    return [row[0] for row in cur.fetchall()]


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
        changes.extend(item_list_changes("contacts", a.contacts, b.contacts))
        if changes:
            yield handle, changes


def compare_orgs(old_orgs, new_orgs):
    removed, both, added = compare_dicts(old_orgs, new_orgs)

    if added:
        print("organisations to be added:")
        for handle in added:
            print("    %s: %r" % (handle, new_orgs[handle].name,))
    if removed:
        print("organisations to be deleted:")
        for handle in removed:
            print("    %r" % (old_orgs[handle],))

    if both:
        all_changes = list(organisation_changes(both, old_orgs, new_orgs))
        if all_changes:
            print("Changed organisations:")
            for handle, changes in all_changes:
                print("    %r:" % (handle,))
                for change in changes:
                    print("        %s" % (change,))


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


def compare_orgs_with_db(cur, asn_list, organisation_list, role_list):
    orgs, unattached_as, unattached_roles = \
          build_organisation_objects(asn_list, organisation_list, role_list)

    db_orgs = build_organisation_objects_from_db(cur)
    db_unattached_as = get_unattached_asns_from_db(cur)
    db_unattached_roles = get_unattached_contacts_from_db(cur)

    compare_orgs(orgs, db_orgs)

    compare_unattached("AS", db_unattached_as,
                       [extract_asn(a) for a in unattached_as])
    compare_unattached("roles", db_unattached_roles,
                       [r['abuse-mailbox'][0] for r in unattached_roles])



parser = argparse.ArgumentParser(
    description=("Show the differences between a set of RIPE DB files"
                 " and the contents of the database."))
parser.add_argument("-v", "--verbose",
                    help="increase output verbosity",
                    default=False,
                    action="store_true")
parser.add_argument("--conninfo",
                    default='dbname=contactdb',
                    help=("Libpg connection string. E.g. 'host=localhost"
                          " port=5432 user=intelmq dbname=connectdb'"
                          " Default: 'dbname=contactdb'"))
parser.add_argument("--organisation-file",
                    default='ripe.db.organisation.gz',
                    help=("Specify the organisation data file."
                          " Default: ripe.db.organisation.gz"))
parser.add_argument("--role-file",
                    default='ripe.db.role.gz',
                    help=("Specify the contact role data file."
                          " Default: ripe.db.role.gz"))
parser.add_argument("--asn-file",
                    default='ripe.db.aut-num.gz',
                    help=("Specify the AS number data file."
                          " Default: ripe.db.aut-num.gz"))


def main():
    options = parser.parse_args()

    (asn_list, organisation_list, role_list) = load_ripe_files(options)

    con = psycopg2.connect(dsn=options.conninfo)
    try:
        compare_orgs_with_db(con.cursor(), asn_list, organisation_list,
                             role_list)
    finally:
        con.close()


if __name__ == '__main__':
    main()
