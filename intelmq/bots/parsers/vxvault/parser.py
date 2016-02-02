# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress
from intelmq.lib.message import Event


class VXVaultParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report:
            self.acknowledge_message()
            return
        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            row = row.strip()

            if len(row) == 0 or not row.startswith('http'):
                continue

            url_object = urlparse(row)

            if not url_object:
                continue

            url = url_object.geturl()
            hostname = url_object.hostname
            port = url_object.port

            event = Event(report)

            if IPAddress.is_valid(hostname):
                event.add("source.ip", hostname)
            else:
                event.add("source.fqdn", hostname)

            event.add('classification.type', u'malware')
            event.add("source.url", url)
            if port:
                event.add("source.port", port)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultParserBot(sys.argv[1])
    bot.start()
