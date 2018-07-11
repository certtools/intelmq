# -*- coding: utf-8 -*-
"""

MARExpertBot queries environment for occurences of IOCs via McAfee Active Response.

Parameter:
dxl_config_file: string
lookup_type: string

"""

import json
import ast

try:
    from dxlclient.client_config import DxlClientConfig
    from dxlclient.client import DxlClient
    from dxlmarclient import MarClient, ResultConstants, ProjectionConstants, ConditionConstants
except ImportError:
    DxlClient = None

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot


class MARExpertBot(Bot):

    query = {
        'Hash' : 
            """[
                 {
                     "name": "Files",
                     "output": "md5",
                     "op": "EQUALS",
                     "value": '%(malware.hash.md5)s'
                 },
                 {
                     "name": "Files",
                     "output": "sha1",
                     "op": "EQUALS",
                     "value": '%(malware.hash.sha1)s'
                 },
                 {
                     "name": "Files",
                     "output": "sha256",
                     "op": "EQUALS",
                     "value": '%(malware.hash.sha256)s'
                 }
            ]""",
        'DestSocket':
            """[
                 {
                     "name": "NetworkFlow",
                     "output": "dst_ip",
                     "op": "EQUALS",
                     "value": '%(destination.ip)s'
                 },
                 {
                     "name": "NetworkFlow",
                     "output": "dst_port",
                     "op": "EQUALS",
                     "value": '%(destination.port)s'
                 }
            ]""",
        'DestIP':
            """[
                 {
                     "name": "NetworkFlow",
                     "output": "dst_ip",
                     "op": "EQUALS",
                     "value": '%(destination.ip)s'
                 }
            ]""",
         'DestFQDN':
            """[
                 {
                     "name": "DNSCache",
                     "output": "hostname",
                     "op": "EQUALS",
                     "value": '%(destination.fqdn)s'
                 }
            ]"""
        }

    def init(self):
        if DxlClient is None:
            self.logger.error('Could not import dxlclient or dxlmarclient. Please review REQUIREMENTS.txt and install it.')
            self.stop()
        self.config = DxlClientConfig.create_dxl_config_from_file(self.parameters.dxl_config_file)
        self.logger.info('Init done.')

    def process(self):
        report = self.receive_message()

        try:
            mar_search_str = ast.literal_eval(self.query[self.parameters.lookup_type] % report)
            for ip_address in self.MAR_Query(mar_search_str):
                event = self.new_event(report)
                event.add('source.ip', ip_address)
                self.send_message(event)

        except KeyError:
            self.logger.info('No information of requested type contained.')
            pass

        self.logger.info('Query done')
        self.acknowledge_message()

    def MAR_Query(self, mar_search_str):

        # Create the client
        with DxlClient(self.config) as client:

            # Connect to the fabric
            client.connect()

            # Create the McAfee Active Response (MAR) client
            marclient = MarClient(client)
            marclient.response_timeout = 30

            # Start the search
            results_context = marclient.search(
                projections=[
                    {
                        "name": "HostInfo",
                        "outputs": ["hostname", "ip_address"]
                    }
                ],
                conditions={
                    "or": [
                        {
                            "and": mar_search_str
                        }
                    ]
                }
            )

            # Iterate the results of the search
            if results_context.has_results:
                results = results_context.get_results()
                for item in results[ResultConstants.ITEMS]:
                    yield (item['output']['HostInfo|ip_address'])


BOT = MARExpertBot
