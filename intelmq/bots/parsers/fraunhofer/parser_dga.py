# -*- coding: utf-8 -*-
"""
The source provides a JSON file with a dictionary. The keys of this dict are
identifiers and the values are lists of domains.

The first part of the identifiers, before the first underscore, can be treated
as malware name. The feed provider committed to retain this schema.

An overview of all names can be found here:
https://dgarchive.caad.fkie.fraunhofer.de/pcres
"""
import json

from intelmq.lib import utils
from intelmq.lib.bot import Bot

__all__ = ['FraunhoferDGAParserBot']


class FraunhoferDGAParserBot(Bot):

    def process(self):
        report = self.receive_message()
        dict_report = json.loads(utils.base64_decode(report.get("raw")))

        for key in dict_report:
            malware_name = key.split('_')[0]
            for row in dict_report[key]:
                event = self.new_event(report)
                event.add('classification.type', 'c2server')
                event.add('malware.name', malware_name)
                if not event.add('source.ip', row, raise_failure=False):
                    event.add('source.fqdn', row)
                event.add("raw", row)
                self.send_message(event)

        self.acknowledge_message()


BOT = FraunhoferDGAParserBot
