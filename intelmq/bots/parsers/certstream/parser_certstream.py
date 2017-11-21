"""
A bot to parse certstream data.
@author: Christoph Giese (Telekom Security, CDR)
"""

import json

import sys
import datetime
import validators
from intelmq.lib import utils, exceptions
from intelmq.lib.bot import Bot


class CertStreamParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw_report = utils.base64_decode(report.get('raw'))
        try:

            json_report = json.loads(raw_report)
        except:
            self.logger.exception("Failed to convert raw_report to json!")
            return

        if 'data' not in json_report:
            self.logger.debug("No data to check..")
            return
        data = json_report['data']

        event = self.new_event(report)
        event.add('raw', raw_report)

        if 'seen' in data:
            event.add('time.source', datetime.datetime.fromtimestamp(int(data['seen'])).strftime('%Y-%m-%d %H:%M:%S UTC'))

        # ToDo: Check if leaf_cert --> extensions --> subjectAltName is identical to all_domains
        # ToDo: Check if leaf_cert --> extensions --> extendedKeyUsage is always for Web Server Authentication (if not filter)

        if 'leaf_cert' in data:
            if 'all_domains' in data['leaf_cert']:
                for domain in data['leaf_cert']['all_domains']:

                    try:
                        event.add('source.fqdn', domain, force=True)
                    except exceptions.InvalidValue:
                        if validators.ipv4(domain):
                            event.add('source.ip', domain, force=True)
                        else:
                            self.logger.debug("Invalid value (%s) in all_domains field. Not a valid ipv4 or domain." % domain)
                    except:
                        self.logger.exception('Other error adding (%s)!' % domain)
                    self.logger.debug("Send domain (%s) from certificate chain." % domain)
                    self.send_message(event)

        if 'chain' in data:
            for chain_element in data['chain']:
                pass  # ToDo: Add chains

        self.acknowledge_message()

BOT = CertStreamParserBot
