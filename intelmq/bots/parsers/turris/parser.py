# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from intelmq.lib.bot import ParserBot

PORTS = {
    "ftp": 21,
    "telnet": 23,
    "http": 80
    # smtp uses both 25 and 587, therefore we can't say for certain
}


class TurrisGreylistParserBot(ParserBot):
    """Parse the Turris Greylist feed"""

    parse = ParserBot.parse_csv_dict
    recover_line = ParserBot.recover_line_csv_dict
    _ignore_lines_starting = ["#"]

    def parse_line(self, line, report):

        for tag in line.get("Tags", "").split(","):

            event = self.new_event(report)

            if tag in ["smtp", "http", "ftp", "telnet"]:
                event.add("protocol.transport", "tcp")
                event.add("protocol.application", tag)
                event.add("classification.type", "brute-force")
                event.add("destination.port", PORTS.get(tag))

            elif tag == "port_scan":
                event.add("classification.type", "scanner")

            else:
                # cases such as "haas", "hass_logged" and "hass_not_logged" come from CZ.NIC HaaS Feed (available in IntelMQ)
                # it's better to use that feed for this data (it's data from SSH honeypot)
                continue

            event.add("raw", self.recover_line(line))
            event.add("source.ip", line.get("Address"))
            yield event


BOT = TurrisGreylistParserBot
