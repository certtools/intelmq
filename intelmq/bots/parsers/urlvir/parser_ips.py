# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class URLVirIPsParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report:
            self.acknowledge_message()
            return
        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()
            if row == "" or row.startswith("#"):
                continue

            event = Event(report)

            event.add('source.ip', row)

            event.add('classification.type', u'malware')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = URLVirIPsParserBot(sys.argv[1])
    bot.start()
