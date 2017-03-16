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

import collections
import gzip


def add_db_args(parser):
    parser.add_argument("--conninfo",
                        default='dbname=contactdb',
                        help="Libpg connection string. E.g. 'host=localhost"
                             " port=5432 user=intelmq dbname=connectdb'"
                             " Default: 'dbname=contactdb'")


def add_common_args(parser):
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        default=False, action="store_true")
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
    parser.add_argument("--asn-whitelist-file",
                        default='',
                        help=("A file name with a whitelist of ASNs."
                              " If this option is not set,"
                              " all ASNs are imported"))


def load_ripe_files(options) -> tuple:
    """Read ripe files as given in the command line options.

    Returns:
        tuple of (asn_list, org_list, role_list, org_to_asn, abusec_to_org)
    """

    # Step 1: read all files
    asn_whitelist = read_asn_whitelist(options.asn_whitelist_file,
                                       verbose=options.verbose)

    asn_list = parse_file(options.asn_file,
                          ('aut-num', 'org', 'status'),
                          verbose=options.verbose)
    organisation_list = parse_file(options.organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'),
                                   verbose=options.verbose)
    role_list = parse_file(options.role_file,
                           ('nic-hdl', 'abuse-mailbox', 'org'), 'role',
                           verbose=options.verbose)

    # Step 2: Prepare new data for insertion
    asn_list = sanitize_asn_list(asn_list, asn_whitelist)

    org_to_asn = org_to_asn_mapping(asn_list)

    organisation_list = sanitize_organisation_list(organisation_list,
                                                   org_to_asn)
    if options.verbose:
        print('** Found {} orgs to be relevant.'.format(len(organisation_list)))

    abusec_to_org = role_to_org_mapping(organisation_list)

    role_list = sanitize_role_list(role_list, abusec_to_org)

    if options.verbose:
        print('** Found {} contacts to be relevant.'.format(len(role_list)))

    return (asn_list, organisation_list, role_list, org_to_asn, abusec_to_org)


def read_asn_whitelist(filename, verbose=False):
    """Read a list of ASNs from file.

    Each line of the file being one ASN in the format "ASnnnnnn".

    Returns:
        list of ASN strings (maybe empty) or None
    """
    if filename:
        out = []
        with open(filename) as f:
            out = [line.strip() for line in f]

        if verbose and out:
            print('** Loaded {} entries from '
                  'ASN whitelist {}'.format(len(out), filename))
        return out
    else:
        return None


def parse_file(filename, fields, index_field=None, verbose=False):
    """Parses a file from the RIPE (split) database set.

    ftp://ftp.ripe.net/ripe/dbase/split/

    Args:
        filename (str): name of the gzipped file
        fields (list of str): names of the fields to read
        index_field (str): the field that marks the beginning of a dataset.
            If not provided, the first element of ``fields`` will be used

    Returns:
        list of dictionaries: The entries read from the file. Each value
        in the dictionaries is a list.

    Note:
        Does **not** handle "continuation lines" (see rfc2622 section 2).

    Note:
        Preserves the contents of the fields like lower and upper case
        characters, though the RPSL is case insensitive and ASCII only.
        Thus for some fields it makes sense to upper() them (before
        comparing).
    """
    if verbose:
        print('** Reading file {0}'.format(filename))

    if not index_field:
        index_field = fields[0]

    important_fields = set(fields)
    important_fields.add(index_field)

    out = []
    tmp = None

    f = gzip.open(filename, 'rt', encoding='latin1')
    for line in f:
        # Comments and remarks
        if (line.startswith('%') or line.startswith('#') or
                line.startswith('remarks:')):
            continue

        if ":" in line:
            key, value = [x.strip() for x in line.split(":", 1)]

            # Fields we are interested in, plus the index
            if key not in important_fields:
                continue

            # If we reach the index again, we have reached the next dataset, add
            # the previous data and start again
            if key == index_field:
                if tmp:  # template is filled, except on the first record
                    out.append(tmp)

                tmp = collections.defaultdict(list)

            # Only add the fields we are interested in to the result set
            if key in fields:
                tmp[key].append(value)

    f.close()

    if verbose:
        print('   -> read {0} entries'.format(len(out)))

    return out


def sanitize_asn_entry(entry):
    """Return a sanitized version of an ASN entry.
    The sanitized version always has an upper case org handle.
    The input entry must already have an org attribute.
    """
    entry = entry.copy()
    entry["org"] = [handle.upper() for handle in entry["org"]]
    return entry


def sanitize_asn_list(asn_list, whitelist=None):
    """Return a sanitized copy of the AS list read from a RIPE aut-num file.
    The returned list retains only those entries which have the
    attributes 'aut-num' and 'org'. Also, if the whitelist parameter is
    given and not None, the first of the aut-num values must be in
    whitelist.
    """
    return [sanitize_asn_entry(entry) for entry in asn_list

            # keep only entries for which we have the minimal
            # necessary attributes
            if entry.get('aut-num') and entry.get('org')

            # when using a white-list, keep only AS in the whitelist:
            if whitelist is None or entry['aut-num'][0] in whitelist]


def sanitize_role_entry(entry):
    """Return a sanitized version of a role entry.
    The sanitized version always has upper case nic-hdl values.
    The input entry must already have a nic-hdl attribute.
    """
    entry = entry.copy()
    entry["nic-hdl"] = [handle.upper() for handle in entry["nic-hdl"]]
    return entry


def sanitize_role_list(role_list, abuse_c_to_org=None):
    """Return a sanitized copy of the role list read from a RIPE role file.
    The returned list retains only those entries which have an
    'abuse-mailbox' attribute.

    If abuse_c_to_org dict is given, only entries that are keys are returned.
    """
    new_list = [sanitize_role_entry(entry) for entry in role_list
                # abuse-mailbox is mandatory for a role used in abuse-c
                if entry.get('abuse-mailbox')]

    if abuse_c_to_org is not None:
        new_list = [entry for entry in new_list
                    if entry['nic-hdl'][0] in abuse_c_to_org]

    return new_list


def sanitize_organisation_entry(entry):
    """Return a sanitized version of a organisation entry.
    The sanitized version always has upper case values for organisation
    and abuse-c. The input entry must already have a organisation
    and abuse-c attributes.
    """
    entry = entry.copy()
    entry["organisation"] = [handle.upper() for handle in entry["organisation"]]
    entry["abuse-c"] = [handle.upper() for handle in entry["abuse-c"]]
    return entry


def sanitize_organisation_list(organisation_list, org_to_asn=None):
    """Return a sanitized copy of the organisation list read from a RIPE file.
    The entries in the returned list have been sanitized with
    sanitize_organisation_entry.

    If org_to_asn dict is given, only entries that are keys are returned.
    """
    new_list = [sanitize_organisation_entry(entry)
                for entry in organisation_list]

    if org_to_asn is not None:
        new_list = [org for org in new_list
                    if org['organisation'][0] in org_to_asn]

    return new_list


def org_to_asn_mapping(asn_list):
    """Return a dictionary mapping RIPE org handles to the corresponding ASNs.
    The parameter is an AS list as read by parse_file and is assumed to
    have been sanitized by sanitize_asn_list which makes sure that the
    relevant information is present in all entries in the list.
    """
    org_to_asn = collections.defaultdict(list)
    for entry in asn_list:
        org_to_asn[entry['org'][0]].append(entry['aut-num'][0][2:])
    return org_to_asn


def role_to_org_mapping(organisation_list):
    """Return a dictionary mapping RIPE role handles to their organisations.
    """
    mapping = collections.defaultdict(list)
    for entry in organisation_list:
        abuse_c = entry['abuse-c'][0] if entry['abuse-c'] else None
        if abuse_c:
            mapping[abuse_c].append(entry['organisation'][0])
    return mapping
