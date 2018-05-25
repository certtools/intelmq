#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide common functions to handle ripe data.


Copyright (C) 2016-2018 by Bundesamt für Sicherheit in der Informationstechnik
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

import collections
import itertools
import gzip
import ipaddress


def add_db_args(parser):
    parser.add_argument("--conninfo",
                        default='dbname=contactdb',
                        help="Libpg connection string. E.g. 'host=localhost"
                             " port=5432 user=intelmq dbname=contactdb'")


def add_common_args(parser):
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        default=False, action="store_true")
    parser.add_argument("--organisation-file",
                        default='ripe.db.organisation.gz',
                        help=("Specify the organisation data file."))
    parser.add_argument("--role-file",
                        default='ripe.db.role.gz',
                        help=("Specify the contact role data file."))
    parser.add_argument("--asn-file",
                        default='ripe.db.aut-num.gz',
                        help=("Specify the AS number data file."))
    parser.add_argument("--inetnum-file",
                        default='ripe.db.inetnum.gz',
                        help=("Specify the inetnum data file."))
    parser.add_argument("--inet6num-file",
                        default='ripe.db.inet6num.gz',
                        help=("Specify the inet6num data file."))
    parser.add_argument("--ripe-delegated-file",
                        default='delegated-ripencc-latest',
                        help=("Name of the delegated-ripencc-latest file to"
                              " read. Only needed for --restrict-to-country."
                              " In that case this file is"
                              " read and only the ASNs given in the file"
                              " that match the country code from"
                              " --restrict-to-country are imported."
                              " If --asn-whitelist-file is also given it"
                              " takes precedence"))
    parser.add_argument("--asn-whitelist-file",
                        default='',
                        help=("A file name with a whitelist of ASNs."
                              " If this option is not set,"
                              " all ASNs are imported"))
    parser.add_argument("--restrict-to-country",
                        metavar="COUNTRY_CODE",
                        help=("A country code, e.g. DE, to restrict which"
                              " information is actually read from the files."))


def load_ripe_files(options) -> tuple:
    """Read ripe files as given in the command line options.

    Returns:
        tuple of (asn_list, organisation_list, role_list, abusec_to_org,
                  inetnum_list, inet6num_list)
    """

    # Step 1: read all files
    asn_whitelist = None
    if options.asn_whitelist_file:
        asn_whitelist = read_asn_whitelist(options.asn_whitelist_file,
                                           verbose=options.verbose)
    elif options.ripe_delegated_file:
        if not options.restrict_to_country:
            print("** --ripe-delegated-file ignored because no country was"
                  " specified with --restrict-to-country")
        else:
            asn_whitelist = read_delegated_file(options.ripe_delegated_file,
                                                options.restrict_to_country,
                                                verbose=options.verbose)

    def restrict_country(record):
        country = options.restrict_to_country
        return (not country) or record["country"][0] == country

    asn_list = parse_file(options.asn_file,
                          ('aut-num', 'org', 'status', 'abuse-c'),
                          verbose=options.verbose)
    inetnum_list = parse_file(options.inetnum_file,
                              ('inetnum', 'org', 'country', 'abuse-c'),
                              restriction=restrict_country,
                              verbose=options.verbose)
    inet6num_list = parse_file(options.inet6num_file,
                               ('inet6num', 'org', 'country', 'abuse-c'),
                               restriction=restrict_country,
                               verbose=options.verbose)

    organisation_list = parse_file(options.organisation_file,
                                   ('organisation', 'org-name', 'abuse-c'),
                                   restriction=lambda org: org["abuse-c"],
                                   verbose=options.verbose)
    organisation_index = build_index(organisation_list, 'organisation')

    role_list = parse_file(options.role_file,
                           ('role', 'nic-hdl', 'abuse-mailbox', 'org'),
                           verbose=options.verbose)
    role_index = build_index(role_list, 'nic-hdl')

    # Step 2: Prepare new data for insertion

    (asn_list_o, asn_list_a,
        organisation_list, organisation_index) = sanitize_split_and_modify(
            asn_list, 'aut-num', asn_whitelist,
            organisation_list, organisation_index, role_index,
            verbose=options.verbose)

    (inetnum_list_o, inetnum_list_a,
        organisation_list, organisation_index) = sanitize_split_and_modify(
            inetnum_list, 'inetnum', None,
            organisation_list, organisation_index, role_index,
            verbose=options.verbose)

    (inet6num_list_o, inet6num_list_a,
        organisation_list, organisation_index) = sanitize_split_and_modify(
            inet6num_list, 'inet6num', None,
            organisation_list, organisation_index, role_index,
            verbose=options.verbose)

    known_organisations = referenced_organisations(
        asn_list_o + asn_list_a,
        inetnum_list_o + inetnum_list_a,
        inet6num_list_o + inet6num_list_a)

    organisation_list = sanitize_organisation_list(organisation_list,
                                                   known_organisations)
    if options.verbose:
        print('** Found {} orgs to be relevant.'.format(len(organisation_list)))

    abusec_to_org = role_to_org_mapping(organisation_list)

    role_list = sanitize_role_list(role_list, abusec_to_org)

    if options.verbose:
        print('** Found {} contacts to be relevant.'.format(len(role_list)))

    return (
        asn_list_o + asn_list_a,
        organisation_list, role_list, abusec_to_org,
        inetnum_list_o + inetnum_list_a,
        inet6num_list_o + inet6num_list_a)


def read_delegated_file(filename, country, verbose=False):
    """Read the ASN entries from the delegated file for the given country."""
    asns = []
    with open(filename) as f:
        for line in f:
            parts = line.split("|")
            if parts[2] == "asn" and parts[1] == country:
                asns.append("AS" + parts[3])
    print('** Loaded {} entries from delegated file {}'
          .format(len(asns), filename))
    return asns


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


def parse_file(filename, fields, index_field=None, restriction=lambda x: True,
               verbose=False):
    """Parses a file from the RIPE (split) database set.

    ftp://ftp.ripe.net/ripe/dbase/split/

    Args:
        filename (str): name of the gzipped file
        fields (list of str): names of the fields to read
        index_field (str): the field that marks the beginning of a dataset.
            If not provided, the first element of ``fields`` will be used
        restriction (optional function): This function is called once
            for every record read from the file. The record is only
            included if this function returns true. It defaults to a
            function that returns True for every record.

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
                # keep previous record if any (tmp will be false before
                # the first record has been read) and if we want to keep
                # it
                if tmp and restriction(tmp):
                    out.append(tmp)

                tmp = collections.defaultdict(list)

            # Only add the fields we are interested in to the result set
            if key in fields:
                tmp[key].append(value)

    f.close()

    if verbose:
        print('   -> read {0} entries'.format(len(out)))

    return out


def build_index(obj_list, index_attribute):
    """Return a dict with the index_attribute as key to the ripe objects.

    The first value of the index attribute will be upper cased and
    used as key for the dict entry.
    """
    return {obj.get(index_attribute)[0].upper(): obj for obj in obj_list}


def uppercase_org_handle(entry):
    """Return a copy of the entry with the 'org' value in upper-case.
    The input entry must already have an org attribute.
    """
    entry = entry.copy()
    entry["org"] = [handle.upper() for handle in entry["org"]]
    return entry


def split_list(obj_list, attribute, whitelist=None):
    """Return three lists split and sanitized from a ripe RESOURCE list.

    If the whitelist parameter is given and not None, the first of the
    attribute values must be in whitelist.

    The returned lists are:
    * entries with `org` but no `abuse-c`
    * entries with both
    * entries with 'abuse-c' but no 'org'
    """
    o = []
    oa = []
    a = []
    for entry in obj_list:
        if not entry.get(attribute):
            continue
        if whitelist and entry[attribute][0] not in whitelist:
            continue

        if entry.get('org') and entry.get('abuse-c'):
            oa.append(uppercase_org_handle(entry))
        elif entry.get('org'):
            o.append(uppercase_org_handle(entry))
        elif entry.get('abuse-c'):
            a.append(entry.copy())

    return (o, oa, a)


def points_to_same_abuse_mailbox(obj, organisation_index, role_index):
    """Return true of the obj's abuse-c points to org->abuse-c's abuse-mailbox.

    Parameter obj must have both `abuse-c` and `org` attributes.
    """
    abuse_c_1 = obj['abuse-c'][0].upper()
    abuse_c_2 = organisation_index[obj['org'][0]].get('abuse-c')[0].upper()
    return abuse_c_1 == abuse_c_2 or (
        role_index[abuse_c_1].get('abuse-mailbox') ==
        role_index[abuse_c_2].get('abuse-mailbox'))


def modify_for_abusec(obj_list_a,
                      organisation_list, organisation_index, role_index,
                      verbose=False):
    """Modifies lists and index to add a virtual org using direct abuse-c.

    We are using the `role` attribute of the abuse-c role as
    org-name and `abuse-c` as organisation's id.
    As regular `organisation` values have ORG- prepended we do not expect
    a conflict here.

    If it does not exist yet, we add it to the organisation_list and update
    the index. Then we let the `org` attribute of obj point to it.

    If `role` is one of a list of known unspecific strings we add the abuse-c
    string.

    Parameters:
        obj_list_a must have an `abuse-c` attribute, we use the first one.

    Returns:
        an obj_list with `org` changed or added to point to the virtual org
        an updated org list
        and updated org index
    """
    added_counter = 0
    for obj in obj_list_a:
        abuse_c = obj['abuse-c'][0].upper()
        role = role_index[abuse_c]

        new_org_id = abuse_c  # for clarity of following code
        new_org_name = role.get('role')[0]
        if new_org_name in ["Abuse", "Abuse-C Role",
                            "Abuse contact role object"]:
            new_org_name += " " + abuse_c

        if new_org_id not in organisation_index:
            new_org = collections.defaultdict(list)
            new_org['organisation'].append(new_org_id)
            new_org['org-name'].append(new_org_name)
            new_org['abuse-c'].append(abuse_c)

            added_counter += 1
            if verbose and added_counter < 7:
                print("    e.g. adding {}".format(new_org))
            organisation_list.append(new_org)
            organisation_index[new_org_id] = new_org

        if obj.get('org'):
            obj['org'][0] = new_org_id
        else:
            obj['org'].append(new_org_id)

    return obj_list_a, organisation_list, organisation_index


def sanitize_split_and_modify(obj_list, index, whitelist,
                              organisation_list, organisation_index,
                              role_index, verbose):
    """Sanitize, split and modify a ripe RESOURCE list for direct abuse-c.

    Handles obj_list where some have direct `abuse-c` attributes.
    Decides which abuse-mailbox to use in case both `org` and `abuse-c`
    are given and modifies organisation_list and organisation_index
    accordingly.

    Returns:
        obj_list: where the original `org` is used for the abuse-mailbox
        obj_list: where direct `abuse-c` is used with extra org for
                  abuse-mailbox
        organisation_list: an updated organisation list (modified in plac)
        organisation_index: an updated index (modified in place)
    """

    obj_list_o, obj_list_oa, obj_list_a = split_list(obj_list, index, whitelist)
    if verbose:
        print("** {}s {} (`org` only)".format(index, len(obj_list_o)))
        print("** {}s {} (`abuse-c` only)".format(index, len(obj_list_a)))
        print("** {}s {} (`org` and `abuse-c`)".format(index, len(obj_list_oa)))
        print("** Distributing entries with (`org` and `abuse-c`)")

    for obj in obj_list_oa:
        if points_to_same_abuse_mailbox(obj, organisation_index, role_index):
            obj_list_o.append(obj)
        else:
            obj_list_a.append(obj)

    # Remove entries from obj_list_o that do not refer to a known
    # organisation. This can happen when e.g. organisations without
    # contact information are ignored and therefore not in
    # organisation_index.
    num_obj_o = len(obj_list_o)
    obj_list_o = [obj for obj in obj_list_o
                  if obj["org"][0] in organisation_index]

    if verbose:
        print("   -> for {} {} we use `org`".format(len(obj_list_o), index))
        print("      ({} referenced unknown organisations)"
              .format(num_obj_o - len(obj_list_o)))
        print("   -> for {} {} we use `abuse-c'".format(len(obj_list_a), index))

    obj_list_a, organisation_list, organisation_index = modify_for_abusec(
        obj_list_a, organisation_list, organisation_index, role_index, verbose)

    return (obj_list_o, obj_list_a, organisation_list, organisation_index)


def convert_inetnum_to_networks(inetnum_list):
    """Replace inetnum ranges with lists of network objects in place.
    """
    for entry in inetnum_list:
        first, last = [ipaddress.ip_address(s.strip())
                       for s in entry["inetnum"][0].split("-", 1)]
        entry["inetnum"] = ipaddress.summarize_address_range(first, last)


def convert_inet6num_to_networks(inet6num_list):
    """Replace inet6num CIDRs with lists of network objects in place.
    """
    for entry in inet6num_list:
        entry["inet6num"] = [ipaddress.ip_network(entry["inet6num"][0])]


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


def sanitize_organisation_list(organisation_list, known_organisations=None):
    """Return a sanitized copy of the organisation list read from a RIPE file.
    The entries in the returned list have been sanitized with
    sanitize_organisation_entry.

    If known_organisations is given it should be a set. Only entries
    from organisation_list whose handle is in that set are returned.
    """
    new_list = [sanitize_organisation_entry(entry)
                for entry in organisation_list]

    if known_organisations is not None:
        new_list = [org for org in new_list
                    if org['organisation'][0] in known_organisations]

    return new_list


def referenced_organisations(*org_referencing_lists):
    """Return the set of all org handles referenced by the entries in the lists.
    """
    return {entry['org'][0]
            for entry in itertools.chain.from_iterable(org_referencing_lists)}


def role_to_org_mapping(organisation_list):
    """Return a dictionary mapping RIPE role handles to their organisations.
    """
    mapping = collections.defaultdict(list)
    for entry in organisation_list:
        abuse_c = entry['abuse-c'][0] if entry['abuse-c'] else None
        if abuse_c:
            mapping[abuse_c].append(entry['organisation'][0])
    return mapping
