# -*- coding: utf-8 -*-
"""
Parses BingMURLs data in JSON format.
"""
import json

from intelmq.lib.bot import ParserBot

MAPPING = {"Attributable": "extra.attributable",
           "Description": "event_description.text",
           "IndicatorThreatType": "classification.identifier",  # MaliciousUrl
           "TLPLevel": "tlp",
           "FirstReportedDateTime": "time.source",
           "NetworkDestinationAsn": "source.asn",
           "NetworkDestinationIPv4": "source.ip",
           "NetworkDestinationPort": "source.port",
           "IsProductLicensed": "extra.isproductlicensed",
           "IsPartnerShareable": "extra.ispartnershareable",
           "Url": "source.url",
           "IndicatorProvider": "extra.indicator_provider",
           "IndicatorExpirationDateTime": "extra.indicator_expiration_date_time",
           "ThreatDetectionProduct": "extra.threat_detection_product",
           "Tags": "extra.tags",
           }


class MicrosoftCTIPParserBot(ParserBot):

    parse = ParserBot.parse_json

    def recover_line(self, line: dict):
        return json.dumps([line], sort_keys=True)  # not applying formatting here

    def parse_line(self, line, report):
        raw = self.recover_line(line)
        if line['Version'] != 1.5:
            raise ValueError('Data is in unknown format %r, only version 1.5 is supported.' % line['version'])
        if line['IndicatorThreatType'] != 'MaliciousUrl':
            raise ValueError('Unknown indicatorthreattype %r, only MaliciousUrl is supported.' % line['indicatorthreattype'])
        event = self.new_event(report)
        for key, value in line.items():
            if key == "LastReportedDateTime" and value != line["FirstReportedDateTime"]:
                raise ValueError("Unexpectedly seen different values in 'FirstReportedDateTime' and "
                                 "'LastReportedDateTime', please open a bug report with example data.")
            elif key == "LastReportedDateTime":
                continue
            if key == 'Version':
                continue
            if key == 'NetworkDestinationIPv4' and value in ['0.0.0.0', '255.255.255.255']:
                continue
            if key == 'NetworkDestinationAsn' and value == 0:
                continue
            if key == 'Tags':
                if len(value) == 1:
                    if value[0] != '??':
                        event.add('source.geolocation.cc', value[0])
                    continue
                self.logger.warn("Field 'Tags' does not have expected "
                                 "length 1, but %r. Saving as %r, but "
                                 "please report this as bug with samples."
                                 "" % (len(value), MAPPING[key]))
            event[MAPPING[key]] = value
        event.add('classification.type', 'blacklist')
        event.add('raw', raw)
        yield event


BOT = MicrosoftCTIPParserBot
