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


class RewindableFileHandle:
    def __init__(self, f):
        self.f = f
        self.last_line = None

    def __iter__(self):
        return self

    def __next__(self):
        self.last_line = next(self.f)
        return self.last_line


class ZoneHParserBot(ParserBot):
    def init(self):
        pass

    def process(self):
        report = self.receive_message()

        for row, raw in self.parse(report):
            event = Event(report)
            parsed_url = urlparse(row["domain"])
            extra = {}

            event.add('classification.identifier', "compromised-website")
            event.add('classification.type', 'compromised')
            event.add('event_description.text', 'defacement')
            event.add('time.source', row["add_date"] + ' UTC')
            event.add('raw', raw)
            event.add('source.ip', row["ip_address"], raise_failure=False)
            event.add('source.fqdn', parsed_url.netloc, raise_failure=False)
            event.add('source.geolocation.cc', row["country_code"],
                      raise_failure=False)
            event.add('protocol.application', parsed_url.scheme)
            # yes, the URL field is called 'domain'
            event.add('source.url', row["domain"], raise_failure=False)
            if row.get("accept_date"):
                extra["accepted_date"] = row.get("accept_date")
            extra["actor"] = row.get("attacker")
            extra["http_target"] = row.get("web_server")
            extra["os.name"] = row["system"]
            extra["compromise_method"] = row["hackmode"]
            extra["zoneh_report_id"] = row["defacement_id"]
            if extra:
                event.add('extra', extra)
            self.send_message(event)
        self.acknowledge_message()

    def parse(self, report):
        raw_report = utils.base64_decode(report["raw"])
        # Temporary fix for https://github.com/certtools/intelmq/issues/967
        raw_report = raw_report.translate({0: None})
        fh = RewindableFileHandle(io.StringIO(raw_report))
        csvr = csv.DictReader(fh)

        # create an array of fieldnames,
        # those were automagically created by the dictreader
        self.fieldnames = csvr.fieldnames

        for row in csvr:
            # need fh to populate the raw field in main event handler
            yield row, fh.last_line.strip()


BOT = ZoneHParserBot
