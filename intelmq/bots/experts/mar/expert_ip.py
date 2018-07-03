# -*- coding: utf-8 -*-
"""

MARIPExpertBot queries environment for IP communication via McAfee Active Response.

Parameter:
dxl_config_file: string

"""
try:
    from dxlclient.client_config import DxlClientConfig
    from dxlclient.client import DxlClient
    from dxlmarclient import MarClient, ResultConstants, ProjectionConstants, ConditionConstants
except ImportError:
    dxlclient = None

# imports for additional libraries and intelmq
from intelmq.lib.bot import Bot


class MARIPParserBot(Bot):

    def init(self):
        if dxlclient is None:
            self.logger.error('Could not import dxlclient or dxlmarclient. Please install it.')
            self.stop()
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
                projections=[
                    {
                        "name": "HostInfo",
                        "outputs": ["hostname", "ip_address"]
                    }
                ],
                conditions={
                    "or": [
                        {
                            "and": [
                                {
                                    "name": "NetworkFlow",
                                    "output": "dst_ip",
                                    "op": "EQUALS",
                                    "value": report.get('destination.ip')
                                },
                                {
                                    "name": "NetworkFlow",
                                    "output": "dst_port",
                                    "op": "EQUALS",
                                    "value": report.get('destination.port')
                                }
                            ]
                        }
                    ]
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

        self.logger.info('Query done')
        self.acknowledge_message()


BOT = MARIPParserBot
