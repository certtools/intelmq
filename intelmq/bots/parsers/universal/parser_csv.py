# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from dateutil.parser import parse
from io import StringIO
import re

if sys.version_info[0] == 2:
    import unicodecsv as csv
else:
    import csv

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class UniversalCsvParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report or not report.contains("raw"):
            self.acknowledge_message()
            return

        columns = self.parameters.columns

        raw_report = utils.base64_decode(report.value("raw"))
        raw_report = re.sub(r'(?m)^#.*\n?', '', raw_report)
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        for row in csv.reader(StringIO(raw_report),
                              delimiter=str(self.parameters.delimiter)):
            event = Event(report)

            for key, value in zip(columns, row):

                if key in ["__IGNORE__", ""]:
                    continue
                try:
                    if key in ["time.source", "time.destination"]:
                        value = parse(value, fuzzy=True).isoformat()
                        value += " UTC"
                    if key in ["source.ip", "destination.ip"]:
                        value = re.findall(
                            r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", value)[0]

                except:
                    continue
                event.add(key, value, sanitize=True)

            event.add('classification.type', self.parameters.type)
            event.add("raw", ",".join(row), sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = UniversalCsvParserBot(sys.argv[1])
    bot.start()
