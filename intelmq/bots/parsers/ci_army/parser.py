# -*- coding: utf-8 -*-

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class CIArmyParserBot(Bot):

    def process(self):

        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw"))
        for row in raw_report.splitlines():

            if row.startswith('#') or row == "":
                continue

            event = self.new_event(report)

            event.add('source.ip', row)
            event.add('classification.type', 'blacklist')
            event.add("raw", row)

            self.send_message(event)
        self.acknowledge_message()


BOT = CIArmyParserBot
