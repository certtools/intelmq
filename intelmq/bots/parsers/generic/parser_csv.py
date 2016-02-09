# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from dateutil.parser import parse
import re

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class GenericCsvParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report or not report.contains("raw"):
            self.acknowledge_message()
            return

        columns = self.parameters.columns

        raw_report = utils.base64_decode(report.value("raw"))
        # ignore lines starting with #
        raw_report = re.sub(r'(?m)^#.*\n?', '', raw_report)
        # ignore null bytes
        raw_report = re.sub(r'(?m)\0', '', raw_report)
        for row in utils.csv_reader(raw_report,
                                    delimiter=str(self.parameters.delimiter)):
            event = Event(report)

            for key, value in zip(columns, row):

                if key in ["__IGNORE__", ""]:
                    continue
                try:
                    if key in ["time.source", "time.destination"]:
                        value = parse(value, fuzzy=True).isoformat()
                        value += " UTC"
                    # regex from http://stackoverflow.com/a/23483979
                    # matching ipv4/ipv6 IP within string
                    elif key in ["source.ip", "destination.ip"]:
                        value = re.compile(
                            '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
                            '\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0'
                            '-5])|(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])'
                            '\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])|'
                            '\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|('
                            '([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]'
                            '|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d'
                            '\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:['
                            '0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|['
                            '1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|'
                            ':))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1'
                            ',3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d'
                            '\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){'
                            '3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,'
                            '4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-'
                            '4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-'
                            '9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-'
                            'Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0'
                            '-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1'
                            '\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(('
                            '(:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4'
                            '}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2['
                            '0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]'
                            '{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2'
                            '[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|'
                            '[1-9]?\d)){3}))|:)))(%.+)?').match(value).group()
                    elif key.endswith('.url') and '://' not in value:
                        value = self.parameters.default_url_protocol + value
                except:
                    self.logger.exception('Encountered error while parsing'
                                          'line in csv file, ignoring.')
                    continue
                event.add(key, value)

            event.add('classification.type', self.parameters.type)
            event.add("raw", ",".join(row))

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = GenericCsvParserBot(sys.argv[1])
    bot.start()
