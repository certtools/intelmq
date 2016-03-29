# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import psycopg2

from intelmq.lib.bot import Bot


SELECT_EMAIL_FROM_IP = """\
WITH
  cidrs (cidr_contact_id, asn)
    AS (SELECT c.cidr_contact_id, c.asn
          FROM cidr c
         WHERE c.cidr >> %(ip)s),
  emails_cidr (email)
    AS (SELECT e.email
          FROM cidrs c
          JOIN nm_email_cidr ec ON ec.cidr_contact_id = c.cidr_contact_id
          JOIN email e ON e.email_id = ec.email_id),
  emails_asn (email)
    AS (SELECT e.email
          FROM cidrs c
          JOIN nm_email_asn ea ON ea.asn = c.asn
          JOIN email e ON e.email_id = ea.email_id)
SELECT email FROM emails_cidr UNION SELECT email from emails_asn;
"""


class CERTBundKontaktExpertBot(Bot):

    def init(self):
        try:
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
                                    sslmode=self.parameters.sslmode)
        self.logger.debug("Connected to PostgreSQL")

    def process(self):
        self.logger.debug("Calling receive_message")
        event = self.receive_message()

        if event is None:
            self.acknowledge_message()
            return

        for section in ["source", "destination"]:
            ip = event.get(section + ".ip")
            self.logger.debug("Calling key %r: %r", section + ".ip", ip)
            contact = self.lookup_ip(ip)
            if contact:
                contact = ",".join(contact)
                key = section + ".abuse_contact"
                if key in event:
                    old_value = event[key]
                    event.update(key, old_value + ',' + contact)
                else:
                    event.add(key, contact)

        self.send_message(event)
        self.acknowledge_message()

    def lookup_ip(self, ip):
        self.logger.debug("Looking up ip: %r", ip)
        cur = self.con.cursor()
        try:
            cur.execute(SELECT_EMAIL_FROM_IP, {"ip": ip})
            return [item[0] for item in cur.fetchall()]
        finally:
            cur.close()


if __name__ == "__main__":
    bot = CERTBundKontaktExpertBot(sys.argv[1])
    bot.start()
