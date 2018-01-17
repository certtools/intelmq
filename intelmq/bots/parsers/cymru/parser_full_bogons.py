# -*- coding: utf-8 -*-
import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class CymruFullBogonsParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get("raw")).strip()

        if not len(raw_report):  # We depend on first line = date
            self.acknowledge_message()
            return

        row = raw_report.splitlines()[0]
        time_str = row[row.find('(') + 1:row.find(')')]
        time = dateutil.parser.parse(time_str).isoformat()

        for row in raw_report.splitlines():
            val = row.strip()
            if not len(val) or val.startswith('#') or val.startswith('//'):
                continue

            event = self.new_event(report)

            if not event.add('source.ip', val, raise_failure=False):
                event.add('source.network', val)

            event.add('time.source', time)
            event.add('classification.type', 'blacklist')
            event.add('raw', row)

            self.send_message(event)
        self.acknowledge_message()


BOT = CymruFullBogonsParserBot
