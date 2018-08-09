"""
A bot to parse certstream data.
@author: Christoph Giese (Telekom Security, CDR)
"""
import json

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.utils import base64_decode


class CertStreamParserBot(ParserBot):

    def parse(self, report):
        raw = base64_decode(report['raw'])
        data = json.loads(raw)['data']

        # ToDo: Check if leaf_cert --> extensions --> subjectAltName is identical to all_domains
        # ToDo: Check if leaf_cert --> extensions --> extendedKeyUsage is always for Web Server Authentication (if not filter)

        if 'leaf_cert' in data:
            if 'all_domains' in data['leaf_cert']:
                for domain in data['leaf_cert']['all_domains']:
                    yield domain, data, raw

    def parse_line(self, line, report):
        domain, data, raw = line
        event = self.new_event(report)
        event.add('time.source', DateTime.from_epoch_millis(int(data['seen'])))
        event.add('classification.type', 'other')
        event.add('raw', raw)

        if not event.add('source.fqdn', domain, raise_failure=False):
            event.add('source.ip', domain)

        yield event

    def recover_line(self, line):
        domain, data, raw = line
        return raw


BOT = CertStreamParserBot
