import sys

import psycopg2

from intelmq.lib.bot import Bot
import intelmq.bots.experts.certbund_contact.common as common
from intelmq.bots.experts.certbund_contact.eventjson import \
     set_certbund_contacts


class CERTBundKontaktExpertBot(Bot):

    def init(self):
        try:
            self.logger.debug("Trying to connect to database")
            self.connect_to_database()
        except:
            self.logger.exception("Failed to connect to database")
            self.stop()

    def connect_to_database(self):
        self.logger.debug("Connecting to PostgreSQL: database=%r, user=%r, "
                          "host=%r, port=%r, sslmode=%r",
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
        self.logger.debug("Connected to PostgreSQL")

    def process(self):
        self.logger.debug("Calling receive_message")
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for section in ["source", "destination"]:
            ip = event.get(section + ".ip")
            asn = event.get(section + ".asn")
            fqdn = event.get(section + ".fqdn")
            contacts = self.lookup_contact(ip, fqdn, asn)
            if contacts is None:
                # stop processing the message because an error occurred
                # during the database query
                return
            if contacts:
                set_certbund_contacts(event, section, contacts)

        self.send_message(event)
        self.acknowledge_message()


    def lookup_contacts(self, cur, asn, ip, fqdn):
        result = []
        for (automation, suffix) in (("manual", ""),
                                     ("automatic", "_automatic")):
            for row in common.lookup_contacts(cur, suffix, asn, ip, fqdn):
                result.append(row + (automation,))
        return result

    def lookup_contact(self, ip, fqdn, asn):
        self.logger.debug("Looking up ip: %r, fqdn: %r, asn: %r", ip, fqdn, asn)
        try:
            cur = self.con.cursor()
            try:
                raw_result = self.lookup_contacts(cur, asn, ip, fqdn)
            finally:
                cur.close()
        except psycopg2.OperationalError:
            # probably a connection problem. Reconnect and try again, once.
            self.logger.exception("OperationalError. Trying to reconnect.")
            self.init()
            return None

        return [dict(email=email, organisation=organisation, sector=sector,
                     matched_fields=matched,
                     annotations=common.maybe_parse_json(annotations),
                     automation=automation)
                for (email, organisation, sector, matched, annotations,
                     automation)
                in raw_result]


BOT = CERTBundKontaktExpertBot
