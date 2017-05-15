# -*- coding: utf-8 -*-
"""
The source provides a JSON file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.
"""
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot

__all__ = ['FraunhoferDGAParserBot']


class FraunhoferDGAParserBot(Bot):

    def process(self):
        report = self.receive_message()
        dict_report = json.loads(utils.base64_decode(report.get("raw")))

        # add all lists together, only one loop needed
        for row in sum(dict_report.values(), []):

            event = self.new_event(report)

            event.add('classification.type', 'c&c')
            if not event.add('source.ip', row, raise_failure=False):
                event.add('source.fqdn', row)
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = FraunhoferDGAParserBot
