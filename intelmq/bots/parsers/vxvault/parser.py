# -*- coding: utf-8 -*-
import sys
from urllib.parse import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.message import Event


class VXVaultParserBot(ParserBot):

    def parse(self, report):
        report_split = utils.base64_decode(report["raw"]).strip().splitlines()
        self.tempdata = report_split[:2]
        for line in report_split[3:]:
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

        event = Event(report)

        if IPAddress.is_valid(hostname):
            event.add("source.ip", hostname)
        else:
            event.add("source.fqdn", hostname)

        event.add('classification.type', 'malware')
        event.add("source.url", url)
        if port:
            event.add("source.port", port)
        event.add("raw", row)
        event.add("time.source", self.tempdata[1])

        yield event

    def recover_line(self, line):
        return '\n'.join(self.tempdata + [line])


if __name__ == "__main__":
    bot = VXVaultParserBot(sys.argv[1])
    bot.start()
