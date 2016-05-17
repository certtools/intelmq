# -*- coding: utf-8 -*-
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class OpenPhishParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.splitlines():

            row = row.strip()
            if row == "":
                continue

            event = Event(report)

            event.add('classification.type', 'phishing')
            event.add('source.url', row)
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = OpenPhishParserBot(sys.argv[1])
    bot.start()
