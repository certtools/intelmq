# -*- coding: utf-8 -*-
"""
See README for database download.
"""

from intelmq.lib.bot import Bot
import csv


class RecordedFutureIPRiskExpertBot(Bot):

    database = dict()

    def init(self):
        self.logger.info("Loading recorded future risk list.")

        try:
            with open(self.parameters.database) as fp:
                rfreader = csv.DictReader(fp)
                for row in rfreader:
                    self.database[row['Name']] = row['Risk']

        except IOError:
            raise ValueError("Recorded future risklist not defined or failed on open.")

        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source", "destination"]:
            if key + '.ip' in event:
                if "extra.rf_iprisk." + key not in event:
                    if event.get(key + '.ip') in self.database:
                        event.add("extra.rf_iprisk." + key, int(self.database[event.get(key + '.ip')]))
                    else:
                        event.add("extra.rf_iprisk." + key, 0)
                elif "extra.rf_iprisk." + key in event and self.overwrite:
                    if event.get(key + '.ip') in self.database:
                        event.change("extra.rf_iprisk." + key, int(self.database[event.get(key + '.ip')]))

        self.send_message(event)
        self.acknowledge_message()


BOT = RecordedFutureIPRiskExpertBot
