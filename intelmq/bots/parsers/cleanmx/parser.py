# -*- coding: utf-8 -*-
from collections import OrderedDict

from intelmq.lib.bot import ParserBot

PHISHING = OrderedDict([
    ("line", "__IGNORE__"),
    ("id", "extra"),
    ("firsttime", "time.source"),
    ("lasttime", "__IGNORE__"),
    ("phishtank", "extra"),
    ("virusname", "event_description.target"),
    ("url", "source.url"),
    ("recent", "status"),  # can be 'down', 'toggle' or 'up'
    ("response", "extra"),
    ("ip", "source.ip"),
    ("review", "extra"),
    ("domain", "source.fqdn"),
    ("country", "source.geolocation.cc"),
    ("source", "source.registry"),
    ("email", "source.abuse_contact"),
    ("inetnum", "extra"),  # network range, probably source.network
    ("netname", "extra"),
    ("ddescr", "extra"),
    ("ns1", "extra"),
    ("ns2", "extra"),
    ("ns3", "extra"),
    ("ns4", "extra"),
    ("ns5", "extra"),
])
VIRUS = OrderedDict([
    ("line", "__IGNORE__"),
    ("id", "extra"),
    ("sub", "extra"),
    ("firsttime", "time.source"),
    ("lasttime", "__IGNORE__"),
    ("scanner", "extra"),
    ("virusname", "malware.name"),
    ("url", "source.url"),
    ("recent", "status"),
    ("response", "extra"),
    ("ip", "source.ip"),
    ("as", "source.asn"),
    ("review", "extra"),
    ("domain", "source.fqdn"),
    ("country", "source.geolocation.cc"),
    ("source", "extra"),
    ("email", "source.abuse_contact"),
    ("inetnum", "extra"),
    ("netname", "extra"),
    ("ddescr", "extra"),
    ("ns1", "extra"),
    ("ns2", "extra"),
    ("ns3", "extra"),
    ("ns4", "extra"),
    ("ns5", "extra"),
])


class CleanMXParserBot(ParserBot):

    def parse(self, report):
        url = report['feed.url']
        if 'xmlphishing' in url:
            self.csv_fieldnames = PHISHING
            self.type = 'phishing'
        elif 'xmlviruses' in url:
            self.csv_fieldnames = VIRUS
            self.type = 'malware'
        else:
            raise ValueError('Unknown report.')
        return self.parse_csv_dict(report)

    def parse_line(self, row, report):
        event = self.new_event(report)

        extra = {}
        for key, value in row.items():
            if not value:
                continue

            if key is None:
                self.logger.warning('Value without key found, skipping the'
                                    ' value: %r', value)
                continue

            key_orig = key
            key = self.csv_fieldnames[key]

            if key == "__IGNORE__":
                continue

            if key == "source.fqdn" and event.is_valid('source.ip', value):
                continue

            if key == "time.source":
                value = value + " UTC"

            if key == "source.asn":
                if value.upper().startswith("ASNA"):
                    continue
                for asn in value.upper().split(','):
                    if asn.startswith("AS"):
                        value = asn.split("AS")[1]
                        break

            if key == "status":
                if value == 'down':
                    value = 'offline'
                elif value == 'up':
                    value = 'online'

            if key_orig == 'scanner' and value == 'undef':
                continue

            if key == 'extra':
                extra[key_orig] = value
                continue

            event.add(key, value)

        if extra:
            event.add('extra', extra)

        event.add('classification.type', self.type)
        event.add("raw", self.recover_line_csv_dict(row))

        yield event


BOT = CleanMXParserBot
