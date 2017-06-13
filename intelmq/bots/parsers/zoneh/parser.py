# -*- coding: utf-8 -*-
"""
ZoneH CSV defacement report parser
"""
import csv
import io
from urllib.parse import urlparse

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue
from intelmq.lib.message import Event


class ZoneHParserBot(ParserBot):
    def init(self):
        pass

    def process(self):
        report = self.receive_message()

        for row in self.parse(report):
            event = Event(report)
            parsed_url = urlparse(row["domain"])

            event.add('classification.identifier', "compromised-website")
            event.add('classification.type', 'compromised')
            event.add('time.source', row["add_date"] + ' UTC')
            event.add('raw', ','.join(row))
            event.add('source.ip', row["ip_address"], raise_failure=False)
            event.add('source.fqdn', parsed_url.netloc, raise_failure=False)
            event.add('source.geolocation.cc', row["country_code"],
                      raise_failure=False)
            event.add('source.port', parsed_url.port)
            # yes, the URL is called 'domain'
            event.add('source.url', row["domain"], raise_failure=False)
            self.send_message(event)
        self.acknowledge_message()

    def parse(self, report):
        raw_report = utils.base64_decode(report["raw"])
        # Temporary fix for https://github.com/certtools/intelmq/issues/967
        raw_report = raw_report.translate({0: None})
        csvr = csv.DictReader(io.StringIO(raw_report))

        # create an array of fieldnames,
        # those were automagically created by the dictreader
        self.fieldnames = csvr.fieldnames

        for row in csvr:
            yield row


BOT = ZoneHParserBot
