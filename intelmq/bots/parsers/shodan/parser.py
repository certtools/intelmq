"""
Shodan Stream Parser

Copyright (C) 2018 by nic.at GmbH
"""
import json

from intelmq.lib.bot import Bot
from intelmq.lib.utils import base64_decode


MAPPING = {
    'hash': 'extra.shodan.event_hash',
    # 'ip': '__IGNORE__',  # using ip_str
    'hostnames': 'source.reverse_dns',  # TODO: multiple hostname
    'org': 'event_description.target',
    'data': 'extra.data',
    'port': 'source.port',
    'transport': 'protocol.transport',
    'isp': 'extra.isp',
    "ftp": {
            "features": {
                "MLST": {
                    "parameters": 'extra.ftp.features.mlst',
                },
                "UTF8": {
                    "parameters": 'extra.ftp.utf8.parameters',
                },
                "REST": {
                    "parameters": 'extra.ftp.rest.parameters',
                },
                "CLNT": {
                    "parameters": 'extra.ftp.clnt.parameters',
                },
                "MLSD": {
                    "parameters": 'extra.ftp.mlsd.parameters',
                },
                "MFMT": {
                    "parameters": 'extra.ftp.mfmt.parameters',
                },
                "MDTM": {
                    "parameters": 'extra.ftp.mdtm.parameters',
                },
                "SIZE": {
                    "parameters": 'extra.ftp.size.parameters',
                }
            },
        "anonymous": 'extra.ftp.anonymous',
        # "features_hash": '__IGNORE__',
    },
    'http': {
        # 'robots_hash': '__IGNORE__',
        # 'redirects': unknown,
        # 'securitytxt': unknown,
        'title': 'extra.http.html.title',
        # 'sitemap_hash': '__IGNORE__',
        # 'robots': '__IGNORE__',
        # 'favicon': '__IGNORE__',
        # 'host': '__IGNORE__',
        'html': 'extra.http.html.data',
        'location': 'extra.http.location',
        # 'components': unknown,
        # 'securitytxt_hash': unknown,
        'server': 'extra.http.server',
        # 'sitemap': unknown,
    },
    "isakmp": {
        "initiator_spi": "extra.isakmp.initiator_spi",
        "responder_spi": "extra.isakmp.responder_spi",
        "msg_id": "extra.isakmp.msg_id",
        "next_payload": "extra.isakmp.next_payload",
        "exchange_type": "extra.isakmp.exchange_type",
        "length": "extra.isakmp.length",
        "version": "extra.isakmp.version",
        "flags": {
            "encryption": "extra.isakmp.encryption",
            "authentication": "extra.isakmp.authentication",
            "commit": "extra.isakmp.commit",
        },
        # "aggressive": {  # same as above
        # "initiator_spi": "extra.isakmp.initiator_spi",
        # "responder_spi": "extra.isakmp.responder_spi",  # can be zeros
        # "msg_id": "extra.isakmp.msg_id",
        # "next_payload": "extra.isakmp.next_payload",
        # "exchange_type": "extra.isakmp.exchange_type",
        # "length": "extra.isakmp.length",
        # "version": "extra.isakmp.version",
        # "flags": {
        # "encryption": "extra.isakmp.encryption",
        # "authentication": "extra.isakmp.authentication",
        # "commit": "extra.isakmp.commit",
        # },
        #              "vendor_ids": [] unknown
        # },
        #            "vendor_ids": [] unknown
    },
    'asn': 'source.asn',
    # 'html': '__IGNORE__',  # use http.html
    'location': {
        # 'country_code3': '__IGNORE__',  # using country_code
        'city': 'source.geolocation.city',
        'region_code': 'extra.region_code',
        'postal_code': 'extra.postal_code',
        'longitude': 'source.geolocation.longitude',
        'country_code': 'source.geolocation.cc',
        'latitude': 'source.geolocation.latitude',
        # 'country_name': '__IGNORE__',  # using country_code
        'area_code': 'extra.area_code',
        'dma_code': 'extra.dma_code',
    },
    'timestamp': 'time.source',
    'domains': 'source.fqdn',  # TODO: multiple domains
    'ip_str': 'source.ip',
    'os': 'extra.os_name',
    # '_shodan': '__IGNORE__',  # for now
    'opts': {'raw': 'extra.raw',
             },
    'tags': 'extra.tags',
}

MAPPING_MINIMAL = {
    'source.ip': "ip_str",
    'source.asn': "asn",
    'source.port': "port",
    'protocol.transport': "transport",
    'event_description.target': "org",
    'extra.data': 'data',
    'extra.html_title': 'title',
    'extra.tags': 'tags',
}

PROTOCOLS = ['ftp', 'http', 'isakmp']

CONVERSIONS = {
    'timestamp': lambda x: x + '+00',
    'hostnames': lambda x: x[0],
    'domains': lambda x: x[0],
}


class ShodanParserBot(Bot):

    def init(self):
        if getattr(self.parameters, 'ignore_errors', True):
            self.ignore_errors = True
        else:
            self.ignore_errors = False
        if getattr(self.parameters, 'minimal_mode', False):
            self.minimal_mode = True
        else:
            self.minimal_mode = False

    def apply_mapping(self, mapping, data):
        self.logger.debug('Applying mapping %r to data %r.', mapping, data)
        event = {}
        for key, value in data.items():
            try:
                if value and mapping[key] != '__IGNORE__':
                    if isinstance(mapping[key], dict):
                        update = self.apply_mapping(mapping[key], value)
                        if update:
                            event.update(update)
                    else:
                        if key in CONVERSIONS:
                            value = CONVERSIONS[key](value)
                        event[mapping[key]] = value
            except KeyError:
                if not self.ignore_errors:
                    raise
        return event

    def process(self):
        report = self.receive_message()
        raw = base64_decode(report['raw'])
        decoded = json.loads(raw)

        event = self.new_event(report)
        event['raw'] = raw
        if self.minimal_mode:
            for intelmqkey, shodankey in MAPPING_MINIMAL.items():
                try:
                    if decoded[shodankey]:
                        event[intelmqkey] = decoded[shodankey]
                except KeyError:
                    pass
            try:
                event['source.geolocation.cc'] = decoded["location"]["country_code"]
            except KeyError:
                pass
            event['time.source'] = CONVERSIONS['timestamp'](decoded["timestamp"])

            event['extra.shodan'] = decoded
            event['classification.type'] = 'other'
        else:
            event.update(self.apply_mapping(MAPPING, decoded))
            event.add('classification.type', 'other')
            event.add('classification.identifier', 'shodan-scan')
            for protocol in PROTOCOLS:
                if protocol in decoded:
                    event.add('protocol.application', protocol)
        self.send_message(event)
        self.acknowledge_message()


BOT = ShodanParserBot
