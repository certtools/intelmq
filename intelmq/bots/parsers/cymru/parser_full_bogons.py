# -*- coding: utf-8 -*-
import dateutil

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class CymruFullBogonsParserBot(ParserBot):

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw")).strip()

        if not len(raw_report):  # We depend on first line = date
            return

        first_row = raw_report[:raw_report.find('\n')]
        time_str = first_row[first_row.find('(') + 1:first_row.find(')')]
        self.last_updated = dateutil.parser.parse(time_str).isoformat()
        self.tempdata.append(first_row)

        for row in raw_report.splitlines():
            yield row.strip()

    def parse_line(self, val, report):
        if not len(val) or val.startswith('#') or val.startswith('//'):
            return

        event = self.new_event(report)

        if not event.add('source.ip', val, raise_failure=False):
            event.add('source.network', val)

        event.add('time.source', self.last_updated)
        event.add('classification.type', 'blacklist')
        event.add('raw', self.recover_line(val))

        yield event


BOT = CymruFullBogonsParserBot
