# -*- coding: utf-8 -*-
"""
See README for database download.
"""

import csv

from intelmq.lib.bot import Bot


class RecordedFutureIPRiskExpertBot(Bot):

    database = dict()

    def init(self):
        self.logger.info("Loading recorded future risk list.")

        try:
            with open(self.parameters.database) as fp:
                rfreader = csv.DictReader(fp)
                for row in rfreader:
                    self.database[row['Name']] = int(row['Risk'])

        except IOError:
            raise ValueError("Recorded future risklist not defined or failed on open.")

        self.overwrite = getattr(self.parameters, 'overwrite', False)

    def process(self):
        event = self.receive_message()

        for key in ["source", "destination"]:
            if key + '.ip' in event:
                if "extra.rf_iprisk." + key not in event:
                    event.add("extra.rf_iprisk." + key, self.database.get(event.get(key + '.ip'), 0))
                elif "extra.rf_iprisk." + key in event and self.overwrite:
                    event.change("extra.rf_iprisk." + key, self.database.get(event.get(key + '.ip'), 0))

        self.send_message(event)
        self.acknowledge_message()


BOT = RecordedFutureIPRiskExpertBot
