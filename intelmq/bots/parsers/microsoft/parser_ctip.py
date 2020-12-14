# -*- coding: utf-8 -*-
"""
Parses CTIP data in JSON format.

Key indicatorexpirationdatetime is ignored, meaning is unknown.

There are two different variants of data
1. Interflow format: JSON format, MAPPING
2. Azure format: JSON stream format, a short example structure:
  "DataFeed": "CTIP-Infected",
  "SourcedFrom": "SinkHoleMessage|SensorMessage"",
  "DateTimeReceivedUtc": nt time
  "DateTimeReceivedUtcTxt": human readable
  "Malware":
  "ThreatCode": "B67-SS-TINBA",
  "ThreatConfidence": "High|Medium|Low|Informational", -> 100/50/20/10
  "TotalEncounters": 3,
  "TLP": "Amber",
  "SourceIp":
  "SourcePort":
  "DestinationIp":
  "DestinationPort":
  "TargetIp": Deprecated, so we gonne ignore it
  "TargetPort": Deprecated, so we gonne ignore it
  "SourceIpInfo": {
    "SourceIpAsnNumber":
    "SourceIpAsnOrgName":
    "SourceIpCountryCode":
    "SourceIpRegion":
    "SourceIpCity"
    "SourceIpPostalCode"
    "SourceIpLatitude"
    "SourceIpLongitude"
    "SourceIpMetroCode"
    "SourceIpAreaCode"
    "SourceIpConnectionType"
  },
  "HttpInfo": {
    "HttpHost": "",
    "HttpRequest": "",
    "HttpMethod": "",
    "HttpReferrer": "",
    "HttpUserAgent": "",
    "HttpVersion": ""
  },
  "CustomInfo": {
    "CustomField1": "",
    "CustomField2": "",
    "CustomField3": "",
    "CustomField4": "",
    "CustomField5": ""
  },
  "Payload": base64 encoded json
}

"""
import json

import intelmq.lib.utils as utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime

INTERFLOW = {"additionalmetadata": "extra.additionalmetadata",
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
AZURE = {
    "DataFeed": "feed.name",
    "SourcedFrom": "event_description.text",
    "DateTimeReceivedUtc": "time.source",
    "DateTimeReceivedUtcTxt": "__IGNORE__",
    "Malware": "extra.malware",
    "ThreatCode": "malware.name",
    "ThreatConfidence": "feed.accuracy",
    "TotalEncounters": "extra.total_encounters",
    "TLP": "tlp",
    "SourceIp": "source.ip",
    "SourcePort": "source.port",
    "DestinationIp": "destination.ip",
    # DestinationIpInfo.* fields are used in the ctip-c2 feed
    "DestinationIpInfo.DestinationIpAsnNumber": "destination.asn",
    "DestinationIpInfo.DestinationIpAsnOrgName": "destination.as_name",
    "DestinationIpInfo.DestinationIpCountryCode": "destination.geolocation.cc",
    "DestinationIpInfo.DestinationIpRegion": "destination.geolocation.region",
    "DestinationIpInfo.DestinationIpCity": "destination.geolocation.city",
    "DestinationIpInfo.DestinationIpPostalCode": "extra.destination.geolocation.postal_code",
    "DestinationIpInfo.DestinationIpLatitude": "destination.geolocation.latitude",
    "DestinationIpInfo.DestinationIpLongitude": "destination.geolocation.longitude",
    "DestinationIpInfo.DestinationIpMetroCode": "extra.destination.geolocation.metro_code",
    "DestinationIpInfo.DestinationIpAreaCode": "extra.destination.geolocation.area_code",
    "DestinationIpInfo.DestinationIpConnectionType": "protocol.application",
    "DestinationIpInfo.DestinationIpv4Int": "__IGNORE__",
    "DestinationPort": "destination.port",
    "TargetIp": "__IGNORE__",
    "TargetPort": "__IGNORE__",
    "Signatures.Sha256": "extra.signatures.sha256",
    "SourceIpInfo.SourceIpAsnNumber": "source.asn",
    "SourceIpInfo.SourceIpAsnOrgName": "source.as_name",
    "SourceIpInfo.SourceIpCountryCode": "source.geolocation.cc",
    "SourceIpInfo.SourceIpRegion": "source.geolocation.region",
    "SourceIpInfo.SourceIpCity": "source.geolocation.city",
    "SourceIpInfo.SourceIpPostalCode": "extra.source.geolocation.postal_code",
    "SourceIpInfo.SourceIpLatitude": "source.geolocation.latitude",
    "SourceIpInfo.SourceIpLongitude": "source.geolocation.longitude",
    "SourceIpInfo.SourceIpMetroCode": "extra.source.geolocation.metro_code",
    "SourceIpInfo.SourceIpAreaCode": "extra.source.geolocation.area_code",
    "SourceIpInfo.SourceIpConnectionType": "protocol.application",
    "HttpInfo.HttpHost": "extra.http.host",
    "HttpInfo.HttpRequest": "extra.http.request",
    "HttpInfo.HttpMethod": "extra.http.method",
    "HttpInfo.HttpReferrer": "extra.http.referrer",
    "HttpInfo.HttpUserAgent": "extra.user_agent",
    "HttpInfo.HttpVersion": "extra.http.version",
    "CustomInfo.CustomField1": "extra.custom_field1",
    "CustomInfo.CustomField2": "extra.custom_field2",
    "CustomInfo.CustomField3": "extra.custom_field3",
    "CustomInfo.CustomField4": "extra.custom_field4",
    "CustomInfo.CustomField5": "extra.custom_field5",
    "Payload.ts": "extra.payload.timestamp",
    "Payload.ip": "extra.payload.ip",
    "Payload.port": "extra.payload.port",
    "Payload.serverIp": "extra.payload.server.ip",
    "Payload.serverPort": "extra.payload.server.port",
    "Payload.domain": "extra.payload.domain",
    "Payload.family": "extra.payload.family",
    "Payload.malware": "extra.payload.malware",
    "Payload.response": "extra.payload.response",
    "Payload.handler": "extra.payload.handler",
    "Payload.type": "protocol.application",
    "Payload": "extra.payload.text",
    "Payload.Time": "extra.payload.time",
    "Payload.SourceIP": "extra.payload.source.ip",
    "Payload.DestIP": "extra.payload.destination.ip",
    "Payload.RemotePort": "extra.payload.remote.port",
    "Payload.RemoteHost": "extra.payload.remote.host",
    "Payload.ServerPort": "extra.payload.server.port",
    "Payload.BCode": "extra.payload.b_code",
    "Payload.Protocol": "extra.payload.protocol",
    "Payload.Length": "extra.payload.length",
    "Payload.URI": "destination.urlpath",
    "Payload.Referer": "extra.http_referer",
    "Payload.UserAgent": "extra.user_agent",
    "Payload.RequestMethod": "extra.http.method",
    "Payload.HTTPHost": "extra.http.host",
    "Payload.Custom1": "extra.payload.custom_field1",
    "Payload.Custom2": "extra.payload.custom_field2",
    "Payload.Custom3": "extra.payload.custom_field3",
    "Payload.Custom4": "extra.payload.custom_field4",
    "Payload.Custom5": "extra.payload.custom_field5",
}
CONFIDENCE = {
    "High": 100,
    "Medium": 50,
    "Low": 20,
    "Informational": 10,
}


class MicrosoftCTIPParserBot(ParserBot):

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        if raw_report.startswith('['):
            self.recover_line = self.recover_line_json
            yield from self.parse_json(report)
        elif raw_report.startswith('{'):
            self.recover_line = self.recover_line_json_stream
            yield from self.parse_json_stream(report)

    def parse_line(self, line, report):
        if line.get('version', None) == 1.5:
            yield from self.parse_interflow(line, report)
        else:
            yield from self.parse_azure(line, report)

    def parse_interflow(self, line, report):
        raw = self.recover_line(line)
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
            event[INTERFLOW[key]] = value
        event.add('feed.accuracy',
                  event.get('feed.accuracy', 100) * line['confidence'] / 100,
                  overwrite=True)
        event.add('classification.type', 'infected-system')
        event.add('raw', raw)
        yield event

    def parse_azure(self, line, report):
        raw = self.recover_line(line)

        event = self.new_event(report)

        for key, value in line.copy().items():
            if key == 'Payload':
                if value == 'AA==':  # NULL
                    del line[key]
                    continue
                try:
                    value = json.loads(utils.base64_decode(value))
                    # continue unpacking in next loop
                except json.decoder.JSONDecodeError:
                    line[key] = utils.base64_decode(value)
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    line['%s.%s' % (key, subkey)] = subvalue
                del line[key]
        for key, value in line.items():
            if key == 'ThreatConfidence':
                if value == 'None':
                    continue
                value = event.get('feed.accuracy', 100) * CONFIDENCE[value] / 100
            elif key == 'DateTimeReceivedUtc':
                value = DateTime.from_windows_nt(value)
            elif key == 'Payload.ts':
                value = DateTime.from_timestamp(value)
            elif key == 'Payload.Protocol':
                event.add('protocol.application', value[:value.find('/')])  # "HTTP/1.1", save additionally
            elif not value:
                continue
            if AZURE[key] != '__IGNORE__':
                event.add(AZURE[key], value, overwrite=True)
        event.add('classification.type', 'infected-system')
        event.add('raw', raw)
        yield event


BOT = MicrosoftCTIPParserBot
