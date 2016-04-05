# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from dateutil.parser import parse as dateparser
from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

__all__ = ['SpamhausDropParserBot']


class SpamhausDropParserBot(Bot):

    def process(self):
        report = self.receive_message()
        self.event_date = None

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.get("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()

            if row.startswith('; Last-Modified:'):
                self.event_date = row.split('; Last-Modified: ')[1].strip()
                self.event_date = dateparser(self.event_date)

            if row == "" or row.startswith(';'):
                continue

            row_splitted = row.split(';')
            network = row_splitted[0].strip()

            event = Event(report)

            event.add('source.network', network)
            event.add('extra', {'blocklist': row_splitted[1].strip()})
            if self.event_date:
                event.add('time.source', self.event_date.isoformat())

            event.add('classification.type', u'spam')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = SpamhausDropParserBot(sys.argv[1])
    bot.start()
