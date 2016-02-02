# -*- coding: utf-8 -*-
"""
The source provides a JSOn file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""
from __future__ import unicode_literals
import json
import sys

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidValue
from intelmq.lib.message import Event


__all__ = ['FraunhoferDGAParserBot']


class FraunhoferDGAParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        dict_report = json.loads(utils.base64_decode(report.value("raw")))

        # add all lists together, only one loop needed
        for row in sum(dict_report.values(), []):

            event = Event(report)

            event.add('classification.type', u'c&c')
            try:
                event.add('source.ip', row)
            except InvalidValue:
                event.add('source.fqdn', row)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = FraunhoferDGAParserBot(sys.argv[1])
    bot.start()
