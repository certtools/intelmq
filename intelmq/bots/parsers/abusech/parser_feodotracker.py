# SPDX-FileCopyrightText: 2022 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import dateutil.parser

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime


class AbusechFeodoTrackerParserBot(ParserBot):
    """
    Parse the Abuse.ch Feodo Tracker feed (json)

    List of source fields:
    [
        'ip_address',
        'port',
        'status',
        'hostname',
        'as_number',
        'as_name',
        'country',
        'first_seen',
        'last_online',
        'malware'
    ]

    """

    parse = ParserBot.parse_json
    recover_line = ParserBot.recover_line_json

    def parse_line(self, line, report):

        event = self.new_event(report)

        if line.get("first_seen"):
            try:
                event.add("time.source",
                          str(DateTime.convert_from_format(value=line.get("first_seen"), format="%Y-%m-%d %H:%M:%S")),
                          raise_failure=False)

            except ValueError:
                self.logger.warning("Failed to parse '%s' to DateTime.", line.get('first_seen'))
                pass

        elif line.get("last_online"):
            try:
                event.add("time.source",
                          str(DateTime.convert_from_format_midnight(line.get("last_online"), format="%Y-%m-%d")),
                          raise_failure=False)
            except ValueError:
                self.logger.warning("Failed to parse '%s' to DateTime.", line.get('last_online'))
                pass

        event.add("classification.type", "c2-server")
        event.add("source.ip", line.get("ip_address"))
        event.add("source.port", line.get("port"))
        event.add("source.asn", line.get("as_number"), raise_failure=False)
        event.add("source.as_name", line.get("as_name"), raise_failure=False)
        event.add("source.geolocation.cc", line.get("country"), raise_failure=False)
        event.add("source.reverse_dns", line.get("hostname"), raise_failure=False)
        event.add("malware.name", line.get("malware"), raise_failure=False)
        event.add("extra.last_online", line.get("last_online"), raise_failure=False)
        event.add("status", line.get("status"), raise_failure=False)
        event.add("raw", self.recover_line(line))

        yield event


BOT = AbusechFeodoTrackerParserBot
