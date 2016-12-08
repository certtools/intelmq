# -*- coding: utf-8 -*-
"""
The source provides a JSOn file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import InvalidValue

__all__ = ['FraunhoferDGAParserBot']


class FraunhoferDGAParserBot(Bot):

    def process(self):
        report = self.receive_message()
        dict_report = json.loads(utils.base64_decode(report.get("raw")))

        # add all lists together, only one loop needed
        for row in sum(dict_report.values(), []):

            event = self.new_event(report)

            event.add('classification.type', 'c&c')
            try:
                event.add('source.ip', row)
            except InvalidValue:
                event.add('source.fqdn', row)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = FraunhoferDGAParserBot
