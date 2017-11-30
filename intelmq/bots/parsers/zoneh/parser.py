# -*- coding: utf-8 -*-
"""
ZoneH CSV defacement report parser
"""
from urllib.parse import urlparse

from intelmq.lib.bot import ParserBot


class ZoneHParserBot(ParserBot):
    recover_line = ParserBot.recover_line
    parse = ParserBot.parse_csv_dict

    def parse_line(self, row, report):
        event = self.new_event(report)
        parsed_url = urlparse(row["domain"])

        event.add('classification.identifier', "compromised-website")
        event.add('classification.type', 'compromised')
        event.add('event_description.text', 'defacement')
        event.add('time.source', row["add_date"] + ' UTC')
        event.add('raw', self.recover_line(self.current_line))
        event.add('source.ip', row["ip_address"], raise_failure=False)
        event.add('source.fqdn', parsed_url.netloc, raise_failure=False)
        event.add('source.geolocation.cc', row["country_code"],
                  raise_failure=False)
        event.add('protocol.application', parsed_url.scheme)
        # yes, the URL field is called 'domain'
        event.add('source.url', row["domain"], raise_failure=False)
        if row.get("accept_date"):
            event.add("extra.accepted_date", row["accept_date"])
        event.add("extra.actor", row["attacker"])
        event.add("extra.http_target", row["web_server"])
        event.add("extra.os.name", row["system"])
        event.add("extra.compromise_method", row["hackmode"])
        event.add("extra.zoneh_report_id", row["defacement_id"])
        yield event


BOT = ZoneHParserBot
