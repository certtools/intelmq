# SPDX-FileCopyrightText: 2018 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import dateutil.parser

from intelmq.lib.bot import ParserBot


class OpenPhishCommercialParserBot(ParserBot):
    """
    Parse the OpenPhish feed

    List of source fields:
    [
        'asn',
        'asn_name',
        'brand',
        'country_code',
        'country_name',
        'discover_time',
        'emails',
        'family_id',
        'host',
        'ip',
        'isotime',
        'page_language',
        'phishing_kit',
        'screenshot',
        'sector',
        'ssl_cert_issued_by',
        'ssl_cert_issued_to',
        'ssl_cert_serial',
        'tld',
        'url',
    ]

    """

    parse = ParserBot.parse_json_stream
    recover_line = ParserBot.recover_line_json

    def parse_line(self, line, report):

        event = self.new_event(report)

        if line.get("asn"):
            try:
                event.add("source.asn", int(line["asn"][2:]), raise_failure=False)  # it comes as "AS12345"
            except ValueError:
                pass

        if line.get("isotime"):
            try:
                event.add("time.source", str(dateutil.parser.parse(line.get("isotime"))), raise_failure=False)
            except dateutil.parser.ParserError:
                pass

        elif line.get("discover_time"):
            try:
                event.add("time.source", str(dateutil.parser.parse(line.get("discover_time"))), raise_failure=False)
            except dateutil.parser.ParserError:
                pass

        event.add("classification.type", "phishing")
        event.add("source.as_name", line.get("asn_name"))
        event.add("extra.brand", line.get("brand"))
        event.add("source.geolocation.cc", line.get("country_code"), raise_failure=False)
        event.add("source.geolocation.country", line.get("country_name"), raise_failure=False)
        event.add("extra.emails", line.get("emails"))
        event.add("extra.family_id", line.get("family_id"))
        event.add("source.fqdn", line.get("host"), raise_failure=False)
        event.add("source.ip", line.get("ip"))
        event.add("extra.page_language", line.get("page_language"))
        event.add("extra.phishing_kit", line.get("phishing_kit"))
        event.add("screenshot_url", line.get("screenshot"), raise_failure=False)
        event.add("extra.sector", line.get("sector"))
        event.add("extra.ssl_cert_issued_by", line.get("ssl_cert_issued_by"))
        event.add("extra.ssl_cert_issued_to", line.get("ssl_cert_issued_to"))
        event.add("extra.ssl_cert_serial", line.get("ssl_cert_serial"))
        event.add("extra.tld", line.get("tld"))
        event.add("source.url", line.get("url"))
        event.add("raw", self.recover_line(line))

        yield event


BOT = OpenPhishCommercialParserBot
