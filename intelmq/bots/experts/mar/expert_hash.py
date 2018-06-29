# -*- coding: utf-8 -*-
"""

MARHashExpertBot queries environment for occurences of file hashes via McAfee Active Response.

Parameter:
dxl_config_file: string

"""
from __future__ import unicode_literals
import sys
import json

from dxlclient.client_config import DxlClientConfig
from dxlclient.client import DxlClient
from dxlmarclient import MarClient, ResultConstants, ProjectionConstants, \
                         ConditionConstants, SortConstants, OperatorConstants

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot

class MARHashParserBot(Bot):

    def init(self):
        self.logger.info('Initializing')
        self.config = DxlClientConfig.create_dxl_config_from_file(self.parameters.dxl_config_file)
        self.logger.info('Init done.')

    def process(self):
        self.logger.info('Start processing.')
        report = self.receive_message()
        self.logger.info('Received Message')

        # Create the client
        with DxlClient(self.config) as client:

            # Connect to the fabric
            client.connect()

            # Create the McAfee Active Response (MAR) client
            marclient = MarClient(client)

            marclient.response_timeout = 30
            # Start the search
            results_context = marclient.search(
                projections=[{
                                 "name": "HostInfo",
                                 "outputs": ["hostname","ip_address"]
                             }],
                conditions={
                                 "or": [{
                                     "and": [{
                                              "name": "Files",
                                              "output": "md5",
                                              "op": "EQUALS",
                                              "value": report.get('malware.hash.md5')
                                             }, {
                                              "name": "Files",
                                              "output": "sha1",
                                              "op": "EQUALS",
                                              "value": report.get('malware.hash.sha1')
                                             }, {
                                              "name": "Files",
                                              "output": "sha256",
                                              "op": "EQUALS",
                                              "value": report.get('malware.hash.sha256')
                                            }]
                                        }]
                           }
            )

            # Iterate the results of the search in pages
            if results_context.has_results:
                results = results_context.get_results()
                # Display items in the current page
                for item in results[ResultConstants.ITEMS]:
                    event = self.new_event(report)
                    event.add('source.ip', item['output']['HostInfo|ip_address'])
                    self.send_message(event)
                    # print (item['output']['HostInfo|hostname'] + '    ' + item['output']['HostInfo|ip_address'])

        self.logger.info('Query done')
        self.acknowledge_message()

BOT = MARHashParserBot
