"""Look up the certbund-contact database.


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
    Bernhard Herzog <bernhard.herzog@intevation.de>
"""
import sys

import psycopg2

from intelmq.lib.bot import Bot
import intelmq.bots.experts.certbund_contact.common as common
from intelmq.bots.experts.certbund_contact.eventjson \
    import set_certbund_contacts


class CERTBundKontaktExpertBot(Bot):

    def init(self):
        try:
            self.logger.debug("Trying to connect to database.")
            self.connect_to_database()
        except:
            self.logger.exception("Failed to connect to database!")
            self.stop()

    def connect_to_database(self):
        self.logger.debug("Connecting to PostgreSQL: database=%r, user=%r, "
                          "host=%r, port=%r, sslmode=%r.",
                          self.parameters.database, self.parameters.user,
                          self.parameters.host, self.parameters.port,
                          self.parameters.sslmode)
        self.con = psycopg2.connect(database=self.parameters.database,
                                    user=self.parameters.user,
                                    host=self.parameters.host,
                                    port=self.parameters.port,
                                    password=self.parameters.password,
                                    sslmode=self.parameters.sslmode)
        self.con.autocommit = True
        self.logger.debug("Connected to PostgreSQL.")

    def process(self):
        self.logger.debug("Calling receive_message.")
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for section in ["source", "destination"]:
            ip = event.get(section + ".ip")
            asn = event.get(section + ".asn")
            fqdn = event.get(section + ".fqdn")
            country_code = event.get(section + ".geolocation.cc")
            contacts = self.lookup_contact(ip, fqdn, asn, country_code)
            if contacts is None:
                # stop processing the message because an error occurred
                # during the database query
                return
            if contacts:
                set_certbund_contacts(event, section, contacts)

        self.send_message(event)
        self.acknowledge_message()

    def lookup_contacts(self, cur, asn, ip, fqdn, country_code):
        automatic = common.lookup_contacts(cur, common.Managed.automatic, asn,
                                           ip, fqdn, country_code)
        self.renumber_organisations_in_place(automatic)
        manual = common.lookup_contacts(cur, common.Managed.manual, asn, ip,
                                        fqdn, country_code)
        self.renumber_organisations_in_place(manual,
                                             len(automatic["organisations"]))
        return {key: automatic[key] + manual[key] for key in automatic}

    def renumber_organisations_in_place(self, matches, start=0):
        idmap = {}
        for new_id, org in enumerate(matches["organisations"], start):
            idmap[org["id"]] = new_id
            org["id"] = new_id

        for match in matches["matches"]:
            match["organisations"] = [idmap[i] for i in match["organisations"]]

    def lookup_contact(self, ip, fqdn, asn, country_code):
        self.logger.debug("Looking up ip: %r, fqdn: %r, asn: %r.", ip, fqdn, asn)
        try:
            cur = self.con.cursor()
            try:
                return self.lookup_contacts(cur, asn, ip, fqdn, country_code)
            finally:
                cur.close()
        except psycopg2.OperationalError:
            # probably a connection problem. Reconnect and try again, once.
            self.logger.exception("OperationalError. Trying to reconnect.")
            self.init()
            return None


BOT = CERTBundKontaktExpertBot
