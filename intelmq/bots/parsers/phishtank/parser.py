# SPDX-FileCopyrightText: 2022 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import dateutil.parser

from intelmq.lib.bot import ParserBot


class PhishTankParserBot(ParserBot):
    """
    Parse the PhishTank feed (json)
    List of source fields:
    [
        'phish_id',
        'url',
        'phish_detail_url',
        'submission_time',
        'verified',
        'verification_time',
        'online',
        'target',
        'details'
    ]
    """

    parse = ParserBot.parse_json
    recover_line = ParserBot.recover_line_json

    def parse_line(self, line, report):

        event = self.new_event(report)

        if line.get("submission_time"):
            try:
                event.add("time.source", str(dateutil.parser.parse(line.get("submission_time"))), raise_failure=False)
            except dateutil.parser.ParserError:
                self.logger.warning("Could not parse submission_time value '%s'", line.get("submission_time"))
                pass

        event.add("classification.type", "phishing")
        event.add("extra.phishtank.phish_id", line.get("phish_id"), raise_failure=False)
        event.add("source.url", line.get("url"))
        event.add("event_description.url", line.get("phish_detail_url"), raise_failure=False)
        event.add("event_description.target", line.get("target"), raise_failure=False)
        event.add("status", "online", raise_failure=False)  # Phishtank provides only online phishing websites
        event.add("extra.phishtank.verified", line.get("verified"), raise_failure=False)
        event.add("extra.phishtank.verification_time", line.get("verification_time"), raise_failure=False)

        if line.get("details") and isinstance(line.get("details"), list) and len(line.get("details")) > 0:
            detail = line.get("details")[0]
            event.add("source.ip", detail.get("ip_address"), raise_failure=False)
            event.add("source.network", detail.get("cidr_block"), raise_failure=False)
            event.add("source.asn", detail.get("announcing_network"), raise_failure=False)
            event.add("source.geolocation.cc", detail.get("country"), raise_failure=False)

        event.add("raw", self.recover_line(line))

        yield event


BOT = PhishTankParserBot
