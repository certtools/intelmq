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


def lookup_by_ipaddress_only(cur, table_extension, ipaddress):
    cur.execute("SELECT DISTINCT"
                "       c.email as email, o.name as organisation,"
                "       s.name as sector"
                "  FROM contact{0} AS c"
                "  JOIN role{0} AS r ON r.contact_id = c.id"
                "  JOIN organisation{0} o"
                "    ON o.id = r.organisation_id"
                "  LEFT OUTER JOIN sector AS s"
                "    ON s.id = o.sector_id"
                "  JOIN organisation_to_network{0} AS orgn"
                "    ON orgn.organisation_id = r.organisation_id"
                "  JOIN network{0} AS n ON n.id = orgn.net_id"
                " WHERE inet(host(network(n.address))) <= %s"
                "   AND %s <= inet(host(broadcast(n.address)))"
                .format(table_extension), (ipaddress, ipaddress))
    return cur.fetchall()


def lookup_by_fqdn_only(cur, table_extension, fqdn):
    cur.execute("SELECT DISTINCT"
                "       c.email as email, o.name as organisation,"
                "       s.name as sector"
                "  FROM contact{0} AS c"
                "  JOIN role{0} AS r ON r.contact_id = c.id"
                "  JOIN organisation{0} o"
                "    ON o.id = r.organisation_id"
                "  LEFT OUTER JOIN sector AS s"
                "    ON s.id = o.sector_id"
                "  JOIN organisation_to_fqdn{0} AS orgf"
                "    ON orgf.organisation_id = r.organisation_id"
                "  JOIN fqdn{0} AS f ON f.id = orgf.fqdn_id"
                " WHERE f.fqdn = %s"
                .format(table_extension), (fqdn,))
    return cur.fetchall()
