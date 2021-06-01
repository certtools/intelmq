# SPDX-FileCopyrightText: 2014 Tomás Lima
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class VXVaultParserBot(ParserBot):
    """Parse the VXVault feed"""

    def parse(self, report):
        report_split = utils.base64_decode(report["raw"]).strip().splitlines()
        self.tempdata = report_split[:3]
        for line in report_split[4:]:
            yield line.strip()

    def parse_line(self, row, report):
        if not row.startswith('http'):
            return []

        url_object = urlparse(row)

        if not url_object:
            return []

        url = url_object.geturl()
        hostname = url_object.hostname
        port = url_object.port

        event = self.new_event(report)

        if not event.add("source.ip", hostname, raise_failure=False):
            event.add("source.fqdn", hostname)

        event.add('classification.type', 'malware-distribution')
        event.add("source.url", url)
        if port:
            event.add("source.port", port)
        event.add("raw", row)
        event.add("time.source", self.tempdata[2])

        yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])


BOT = VXVaultParserBot
