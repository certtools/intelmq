import sys
import json

import psycopg2

from intelmq.lib.bot import Bot


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
            classification = event.get("event.classification.identifier")
            notifications = self.lookup_contact(classification, ip, fqdn, asn)
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

    def lookup_contact(self, classification, ip, fqdn, asn):
        self.logger.debug("Looking up ip: %r, classification: %r",
                          ip, classification)
        try:
            cur = self.con.cursor()
            try:
                #
                # s1)  Event has FQDN:
                #
                if fqdn:
                    # Yes -> Go to m1
                    cur.execute("SELECT * FROM notifications_for_fqdn(%s, %s);",
                                (fqdn, classification))

                #
                # s2)  Event has IP:
                #
                elif ip:
                    # Yes -> Go to m2
                    cur.execute("SELECT * FROM notifications_for_ip(%s, %s);",
                                (ip, classification))

                #
                # s3) Event has ASN:
                #
                elif asn:
                    # Yes -> Go to m3
                    cur.execute("SELECT * FROM notifications_for_asn(%s, %s);",
                                (asn, classification))
                else:
                    # No -> No information available (not implemented)
                    pass
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
