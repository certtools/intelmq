import sys
import json

import psycopg2

from intelmq.lib.bot import Bot
import intelmq.bots.experts.certbund_contact.common as common


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
            class_type = event.get("classification.type")
            class_identifier = event.get("classification.identifier")
            notifications = self.lookup_contact(class_type, class_identifier,
                                                ip, fqdn, asn)
            if notifications is None:
                # stop processing the message because an error occurred
                # during the database query
                return
            if notifications:
                self.set_certbund_field(event, "notify_" + section,
                                        notifications)
            elif notifications is False:
                self.set_certbund_field(event, section + "_inhibited", [])

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

    def lookup_manual_and_auto(self, cur, criterion, value, class_type):
        assert criterion in ("fqdn", "ip", "asn")
        if not value:
            return []
        cur.execute("SELECT * FROM notifications_for_{}(%s, %s)"
                    .format(criterion), (value, class_type))
        result = cur.fetchall()
        if result:
            return result
        cur.execute("SELECT * FROM notifications_for_{}_automatic(%s, %s)"
                    .format(criterion), (value, class_type))
        return cur.fetchall()

    def lookup_by_asn_only(self, cur, asn):
        # temporary fallback to lookup contacts by ASN from automatic
        # and manual tables without regard to classification identifier
        # or other criteria.
        for automation in ("", "_automatic"):
            result = common.lookup_by_asn_only(cur, automation, asn)
            if result:
                return result
        return []

    def notification_inhibited(self, cur, class_type, class_identifier,
                               ip, fqdn, asn):
        cur.execute("SELECT notifications_inhibited(%s, %s, %s, %s);",
                    (asn, ip, class_type, class_identifier))
        return cur.fetchone()[0]

    def lookup_contact(self, class_type, class_identifier, ip, fqdn, asn):
        self.logger.debug("Looking up ip: %r, classification.type: %r,"
                          " classification.identifier: %r, ",
                          ip, class_type)
        try:
            cur = self.con.cursor()
            try:
                if self.notification_inhibited(cur, class_type,
                                               class_identifier, ip, fqdn, asn):
                    return False

                raw_result = self.lookup_manual_and_auto(cur, "fqdn", fqdn,
                                                         class_type)

                ip_result = self.lookup_manual_and_auto(cur, "ip", ip,
                                                        class_type)
                raw_result.extend(ip_result)
                if not ip_result:
                    asn_notifications = self.lookup_manual_and_auto(
                        cur, "asn", asn, class_type)
                    if not asn_notifications and asn:
                        asn_notifications = self.lookup_by_asn_only(cur, asn)
                    raw_result.extend(asn_notifications)
            finally:
                cur.close()
        except psycopg2.OperationalError:
            # probably a connection problem. Reconnect and try again, once.
            self.logger.exception("OperationalError. Trying to reconnect.")
            self.init()
            return None

        return [dict(email=email, organisation=organisation, sector=sector,
                     template_path=template_path, format=format, ttl=ttl)
                for (email, organisation, sector, template_path, format, ttl)
                in raw_result]


BOT = CERTBundKontaktExpertBot
