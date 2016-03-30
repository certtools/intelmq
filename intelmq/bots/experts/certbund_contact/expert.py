# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import json

import psycopg2

from intelmq.lib.bot import Bot


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
            classification = event.get("event.classification.identifier")
            notifications = self.lookup_ip(ip, classification)
            if notifications is None:
                # stop processing the message because an error occurred
                # during the database query
                return
            if notifications:
                self.set_certbund_field(event, "notify_" + section,
                                        notifications)


        self.send_message(event)
        self.acknowledge_message()

    def set_certbund_field(self, event, key, value):
        if "extra" in event:
            extra = json.loads(event["extra"])
        else:
            extra = {}
        certbund = extra.setdefault("certbund", {})
        certbund[key] = value
        event.add("extra", extra, force=True)

    def lookup_ip(self, ip, classification):
        self.logger.debug("Looking up ip: %r, classification: %r",
                          ip, classification)
        try:
            cur = self.con.cursor()
            try:
                cur.execute("SELECT * FROM notifications_for_ip(%s, %s);",
                            (ip, classification))
                raw_result = cur.fetchall()
            finally:
                cur.close()
        except psycopg2.OperationalError:
            # probably a connection problem. Reconnect and try again, once.
            self.logger.exception("OperationalError. Trying to reconnect.")
            self.init()
            return None

        return [dict(email=email, organisation=organisation,
                     template_path=template_path, format=format, ttl=ttl)
                for (email, organisation, template_path, format, ttl)
                in raw_result]



if __name__ == "__main__":
    bot = CERTBundKontaktExpertBot(sys.argv[1])
    bot.start()
