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
            classification = event.get("classification.type")
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

    def lookup_manual_and_auto(self, cur, criterion, value, classification):
        assert criterion in ("fqdn", "ip", "asn")
        if not value:
            return []
        cur.execute("SELECT * FROM notifications_for_{}(%s, %s)"
                    .format(criterion), (value, classification))
        result = cur.fetchall()
        if result:
            return result
        cur.execute("SELECT * FROM notifications_for_{}_automatic(%s, %s)"
                    .format(criterion), (value, classification))
        return cur.fetchall()

    def lookup_by_asn_only(self, cur, asn):
        # temporary fallback to lookup contacts by ASN from automatic
        # and manual tables without regard to classification identifier
        # or other criteria.
        for automation in ("", "_automatic"):
            cur.execute("SELECT DISTINCT"
                        "       c.email as email, o.name as organisation,"
                        "       s.name as sector, '' as template_path,"
                        "       'feed_specific' as format_name,"
                        "       oa.notification_interval as notification_interval"
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
                        " WHERE a.number = %s".format(automation), (asn,))
            result = cur.fetchall()
            if result:
                return result
        return []

    def lookup_contact(self, classification, ip, fqdn, asn):
        self.logger.debug("Looking up ip: %r, classification: %r",
                          ip, classification)
        try:
            cur = self.con.cursor()
            try:
                raw_result = self.lookup_manual_and_auto(cur, "fqdn", fqdn,
                                                         classification)

                ip_result = self.lookup_manual_and_auto(cur, "ip", ip,
                                                        classification)
                raw_result.extend(ip_result)
                if not ip_result:
                    asn_notifications = self.lookup_manual_and_auto(
                        cur, "asn", asn, classification)
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


if __name__ == "__main__":
    bot = CERTBundKontaktExpertBot(sys.argv[1])
    bot.start()
