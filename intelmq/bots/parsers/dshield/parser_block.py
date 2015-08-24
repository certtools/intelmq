# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Event


class DshieldBlockParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()

            if row.startswith("#") or len(row) == 0 or row.startswith('Start'):
                continue

            values = row.split("\t")

            if len(values) < 3:
                continue    # raise an error

            network_ip = values[0]
            network_mask = values[2]
            network = '%s/%s' % (network_ip, network_mask)

            event = Event()

            event.add('source.network', network, sanitize=True)
            event.add('classification.type', u'blacklist')
            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DshieldBlockParserBot(sys.argv[1])
    bot.start()
