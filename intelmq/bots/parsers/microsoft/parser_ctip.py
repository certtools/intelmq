# -*- coding: utf-8 -*-
"""
Parses CTIP data in JSON format.
"""
import json

from intelmq.lib.bot import ParserBot
from intelmq.lib.utils import base64_decode


MAPPING = {
    "description": "event_description.text",
    "externalid": "malware.name",
    "tlplevel": "extra.tlp",
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
    def process(self):
        report = self.receive_message()
        for ioc in json.loads(base64_decode(report['raw'])):
            raw = json.dumps(ioc, sort_keys=True)  # not applying formatting here
            if ioc['version'] != 1.5:
                raise ValueError('Data is in unknown format %r, only version 1.5 is supported.' % ioc['version'])
            if ioc['indicatorthreattype'] != 'Botnet':
                raise ValueError('Unknown indicatorthreattype %r, only Botnet is supported.' % ioc['indicatorthreattype'])
            if 'additionalmetadata' in ioc and ioc['additionalmetadata'] not in [[], [''], ['null'], [None]]:
                raise ValueError("Cannot parse IOC, format of field 'additionalmetadata' is unknown: %r." % ioc['additionalmetadata'])
            event = self.new_event(report)
            for key, value in MAPPING.items():
                if key in ioc:
                    if key == "firstreporteddatetime":
                        ioc[key] += ' UTC'
                    event[value] = ioc[key]
            event.add('feed.accuracy',
                      event.get('feed.accuracy', 100)*ioc['confidence']/100,
                      overwrite=True)
            event.add('classification.type', 'botnet drone')
            event.add('raw', raw)
            self.send_message(event)

        self.acknowledge_message()


BOT = MicrosoftCTIPParserBot
