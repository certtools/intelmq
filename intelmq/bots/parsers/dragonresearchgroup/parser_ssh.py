# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class DragonResearchGroupSSHParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.splitlines():

            row = row.strip()

            if len(row) == 0 or row.startswith('#'):
                continue

            splitted_row = row.split('|')
            event = Event(report)

            columns = ["source.asn", "source.as_name",
                       "source.ip", "time.source"]

            for key, value in zip(columns, splitted_row):
                value = value.strip()

                if key == "time.source":
                    value += "+00:00"

                if value == "NA":
                    continue

                event.add(key, value)

            event.add("classification.type", "brute-force")
            event.add("protocol.application", "ssh")
            event.add("protocol.transport", "tcp")
            event.add("destination.port", 22)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DragonResearchGroupSSHParserBot(sys.argv[1])
    bot.start()
