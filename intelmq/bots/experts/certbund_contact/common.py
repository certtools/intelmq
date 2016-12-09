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
                "       c.email as email, o.name as organisation,"
                "       s.name as sector"
                "  FROM contact{0} AS c"
                "  JOIN role{0} AS r ON r.contact_id = c.id"
                "  JOIN organisation_to_asn{0} AS oa"
                "    ON oa.organisation_id = r.organisation_id"
                "  JOIN organisation{0} o"
                "    ON o.id = r.organisation_id"
                "  LEFT OUTER JOIN sector AS s"
                "    ON s.id = o.sector_id"
                "  JOIN autonomous_system{0} AS a"
                "    ON a.number = oa.asn_id"
                " WHERE a.number = %s".format(table_extension), (asn,))
    return cur.fetchall()


def lookup_contacts(cur, table_extension, asn, ip, fqdn):
    cur.execute("""
    WITH matched_asn (organisation_id, reason)
             AS (SELECT oa.organisation_id, ('asn' :: TEXT)
                   FROM autonomous_system{0} AS a
                   JOIN organisation_to_asn{0} AS oa
                     ON a.number = oa.asn_id
                  WHERE a.number = %(asn)s),
         matched_ip (organisation_id, reason)
             AS (SELECT "on".organisation_id, ('ip' :: TEXT)
                   FROM network{0} AS n
                   JOIN organisation_to_network{0} AS "on"
                     ON n.id = "on".net_id
                  WHERE inet(host(network(n.address))) <= %(ip)s
                    AND %(ip)s <= inet(host(broadcast(n.address)))),
         matched_fqdn (organisation_id, reason)
             AS (SELECT of.organisation_id, ('fqdn' :: TEXT)
                   FROM fqdn{0} AS f
                   JOIN organisation_to_fqdn{0} AS of
                     ON f.id = of.fqdn_id
                  WHERE f.fqdn = %(fqdn)s),
         grouped_matches (organisation_id, reasons)
             AS (SELECT u.organisation_id, array_agg(u.reason)
                   FROM (SELECT organisation_id, reason FROM matched_asn
                         UNION
                         SELECT organisation_id, reason FROM matched_ip
                         UNION
                         SELECT organisation_id, reason FROM matched_fqdn) u
               GROUP BY u.organisation_id)

    -- we explicitly check the DISTINCT in the main SELECT statement
    -- only on c.email and o.id because all other fields are functional
    -- dependencies of these:
    --
    --  c.email      obviously
    --  o.name       o.id is a key of the organisation table
    --  s.name       ditto + sector.id is a key of sector
    --  m.reasons    grouped_matches is grouped by organisation id alone,
    --               so it#s a key in grouped_matches

    SELECT DISTINCT ON (c.email, o.id)
           c.email as email, o.name as organisation, s.name as sector,
           m.reasons as reasons,
           CASE WHEN %(extension)s = ''
                THEN (SELECT json_agg(annotation)
                        FROM organisation_annotation ann
                       WHERE ann.organisation_id = o.id)
                ELSE ('[]' :: JSON)
           END AS annotations
      FROM grouped_matches as m
      JOIN organisation{0} o ON o.id = m.organisation_id
      JOIN role{0} AS r ON r.organisation_id = o.id
      JOIN contact{0} AS c ON c.id = r.contact_id
      LEFT OUTER JOIN sector AS s ON s.id = o.sector_id
      """.format(table_extension),
                {"asn": asn, "ip": ip, "fqdn": fqdn,
                 "extension": table_extension})
    return cur.fetchall()
