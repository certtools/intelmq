#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide common functions to query the contactdb.

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
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

from enum import Enum
import json


def maybe_parse_json(string_or_json):
    if isinstance(string_or_json, str):
        return json.loads(string_or_json)
    return string_or_json


def lookup_by_asn_only(cur, table_extension, asn):
    """Find email addresses for ASN from either manual or auto tables.

    This is a simple version that does not consider some other criteria
    in the database.

    :return: list of returned db rows
    """
    cur.execute("SELECT DISTINCT"
                "       c.email AS email, o.name AS organisation,"
                "       s.name AS sector"
                "  FROM contact{0} AS c"
                "  JOIN role{0} AS r ON r.contact_id = c.id"
                "  JOIN organisation_to_asn{0} AS oa"
                "    ON oa.organisation_id = r.organisation_id"
                "  JOIN organisation{0} AS o"
                "    ON o.id = r.organisation_id"
                "  LEFT OUTER JOIN sector AS s"
                "    ON s.id = o.sector_id"
                "  JOIN autonomous_system{0} AS a"
                "    ON a.number = oa.asn_id"
                " WHERE a.number = %s".format(table_extension), (asn,))
    return cur.fetchall()


# Enum type for the "managed" parameter of lookup_contacts.
Managed = Enum("Managed", "manual automatic")


def lookup_contacts(cur, managed, asn, ip, fqdn):
    if managed is Managed.manual:
        table_extension = ""
    elif managed is Managed.automatic:
        table_extension = "_automatic"
    else:
        raise ValueError("The 'managed' parameter must be one of the values"
                         " of the Managed enum, not %r" % (managed,))

    cur.execute("""
    WITH
         -- all organisations related to the ASN
         matched_asn (organisation_id)
             AS (SELECT oa.organisation_id
                   FROM autonomous_system{0} AS a
                   JOIN organisation_to_asn{0} AS oa
                     ON a.number = oa.asn_id
                  WHERE a.number = %(asn)s),
         -- the ASN matches in a form useful for conversion to JSON
         asn_json_rows (field, organisations, annotations, managed)
             AS (SELECT 'asn' AS field,
                        ARRAY(SELECT * FROM matched_asn) AS organisations,
                        coalesce(CASE WHEN %(extension)s = ''
                                      THEN (SELECT json_agg(annotation)
                                              FROM autonomous_system_annotation
                                                   ann
                                             WHERE ann.asn_id = %(asn)s)
                                 END,
                                 ('[]' :: JSON)) AS annotations,
                        %(managed)s AS managed),

         -- The FADN IDs for the given FQDN
         matched_fqdn_ids (fqdn_id)
             AS (SELECT f.id AS fqdn_id
                   FROM fqdn{0} AS f
                  WHERE f.fqdn = %(fqdn)s),
         -- all organisations related to the matched_fqdn_ids
         matched_fqdn (organisation_id)
             AS (SELECT of.organisation_id AS organisation_id
                   FROM matched_fqdn_ids AS f
                   JOIN organisation_to_fqdn{0} AS of
                     ON f.fqdn_id = of.fqdn_id),
         -- the FQDN matches in a form useful for conversion to JSON
         fqdn_json_rows (field, organisations, annotations, managed)
             AS (SELECT 'fqdn' AS field,
                        ARRAY(SELECT * FROM matched_fqdn) AS organisations,
                        coalesce(CASE WHEN %(extension)s = ''
                                      THEN (SELECT json_agg(annotation)
                                              FROM fqdn_annotation ann
                                             WHERE ann.fqdn_id
                                                   IN (SELECT *
                                                       FROM matched_fqdn_ids))
                                 END,
                                 ('[]' :: JSON)) AS annotations,
                        %(managed)s AS managed),

         -- all matched networks including their cidr addresses
         matched_networks (network_id, address)
             AS (SELECT n.id AS network_id, n.address AS address
                   FROM network{0} AS n
                  WHERE inet(host(network(n.address))) <= %(ip)s
                    AND %(ip)s <= inet(host(broadcast(n.address)))),

         -- all matched networks in a form useful for conversion to JSON
         network_json_rows (field, address, organisations, annotations, managed)
             AS (SELECT 'ip' AS field,
                        mn.address AS address,
                        ARRAY(SELECT orgn.organisation_id
                                FROM organisation_to_network{0} orgn
                               WHERE mn.network_id = orgn.net_id)
                        AS organisations,
                        coalesce(CASE WHEN %(extension)s = ''
                                      THEN (SELECT json_agg(annotation)
                                              FROM network_annotation ann
                                             WHERE ann.network_id
                                                   = mn.network_id)
                                 END,
                                 ('[]' :: JSON)) AS annotations,
                        %(managed)s AS managed
                   FROM matched_networks mn),

         -- The IDs of all matched organisations
         grouped_matches (organisation_id)
             AS (SELECT u.organisation_id
                   FROM (SELECT organisation_id FROM matched_asn
                         UNION
                         SELECT orgn.organisation_id
                           FROM matched_networks mn
                           JOIN organisation_to_network{0} orgn
                             ON mn.network_id = orgn.net_id
                         UNION
                         SELECT organisation_id FROM matched_fqdn) u),

         -- map organisation IDs to that organisation's contacts in JSON
         -- form
         org_contacts (org_id, contacts)
             AS (SELECT r.organisation_id,
                        ARRAY(SELECT row_to_json(sub)
                              FROM (SELECT r2.role_type as role,
                                           c.email as email,
                                           r2.is_primary_contact
                                              AS is_primary_contact,
                                           %(managed)s AS managed
                                     FROM role{0} r2
                                     JOIN contact{0} c ON c.id = r2.contact_id
                                    WHERE r2.organisation_id
                                              = r.organisation_id) sub)
                 FROM role{0} r
                 GROUP BY r.organisation_id),

         -- All matched organisations as rows that can be easily
         -- converted to JSON
         org_json_rows (id, name, sector, contacts, annotations, managed)
             AS (SELECT o.id as id, o.name as name, sector.name as sector,
                        coalesce((SELECT oc.contacts
                                  FROM org_contacts oc
                                  WHERE oc.org_id = o.id),
                                 ARRAY[] :: JSON[])
                        AS contacts,
                        coalesce(CASE WHEN %(extension)s = ''
                                      THEN (SELECT json_agg(annotation)
                                              FROM organisation_annotation ann
                                             WHERE ann.organisation_id = o.id)
                                 END,
                                 ('[]' :: JSON))
                        AS annotations,
                        %(managed)s AS managed
                  FROM organisation{0} o
                  LEFT OUTER JOIN sector ON sector.id = o.sector_id
                 WHERE o.id IN (select * FROM grouped_matches))

      SELECT coalesce((SELECT json_agg(row_to_json(org_json_rows))
                       FROM org_json_rows),
                       '[]' :: JSON)
             AS organisations,

             coalesce((SELECT json_agg(row_to_json(asn_json_rows))
                       FROM asn_json_rows),
                       '[]' :: JSON)
             AS asn_matches,

             coalesce((SELECT json_agg(row_to_json(fqdn_json_rows))
                      FROM fqdn_json_rows),
                      '[]' :: JSON)
             AS fqdn_matches,

             coalesce((SELECT json_agg(row_to_json(network_json_rows))
                       FROM network_json_rows),
                       '[]' :: JSON)
             AS network_matches
      """.format(table_extension),
                {"asn": asn, "fqdn": fqdn, "ip": ip,
                 "managed": managed.name, "extension": table_extension})

    org_result = cur.fetchone()
    return {"organisations": maybe_parse_json(org_result[0]),
            "matches": (maybe_parse_json(org_result[1])
                        + maybe_parse_json(org_result[2])
                        + maybe_parse_json(org_result[3]))}
