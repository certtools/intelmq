# -*- coding: utf-8 -*-
"""
Parses CTIP data in JSON format.

Key indicatorexpirationdatetime is ignored, meaning is unknown.
"""
import json

from intelmq.lib.bot import ParserBot


MAPPING = {"additionalmetadata": "extra.additionalmetadata",
           "description": "event_description.text",
           "externalid": "malware.name",
           "tlplevel": "tlp",
           "firstreporteddatetime": "time.source",
           "networksourceipv4": "source.ip",
           "networksourceport": "source.port",
           "networkdestinationipv4": "destination.ip",
           "networkdestinationport": "destination.port",
           "isproductlicensed": "extra.isproductlicensed",
           "ispartnershareable": "extra.ispartnershareable",
           "networksourceasn": "source.asn",
           "hostname": "destination.fqdn",
           "useragent": "extra.user_agent",
           "severity": "extra.severity",
           "tags": "extra.tags",
           }


class MicrosoftCTIPParserBot(ParserBot):

    parse = ParserBot.parse_json

    def recover_line(self, line: dict):
        return json.dumps([line], sort_keys=True)  # not applying formatting here

    def parse_line(self, line, report):
        raw = self.recover_line(line)
        if line['version'] != 1.5:
            raise ValueError('Data is in unknown format %r, only version 1.5 is supported.' % line['version'])
        if line['indicatorthreattype'] != 'Botnet':
            raise ValueError('Unknown indicatorthreattype %r, only Botnet is supported.' % line['indicatorthreattype'])
        if 'additionalmetadata' in line and line['additionalmetadata'] in [[], [''], ['null'], [None]]:
            del line['additionalmetadata']
        event = self.new_event(report)
        for key, value in line.items():
            if key in ['version', 'indicatorthreattype', 'confidence', 'indicatorexpirationdatetime']:
                continue
            if key == "firstreporteddatetime":
                value += ' UTC'
            if key == "hostname" and value == line["networkdestinationipv4"]:  # ignore IP in FQDN field
                continue
            if key == "hostname" and not event.is_valid("source.fqdn", value):
                # can contain very weird characters
                continue
            if key == 'networkdestinationipv4' and value == '0.0.0.0':
                continue
            if key == 'networkdestinationipv4' and ',' in value:
                """
                data contains:
                "networkdestinationipv4": "192.88.99.209, 192.88.99.209",
                since 2019-03-14, reported upstream, IP addresses are always the same
                """
                value = value[:value.find(',')]
            event[MAPPING[key]] = value
        event.add('feed.accuracy',
                  event.get('feed.accuracy', 100) * line['confidence'] / 100,
                  overwrite=True)
        event.add('classification.type', 'infected system')
        event.add('raw', raw)
        yield event


BOT = MicrosoftCTIPParserBot
