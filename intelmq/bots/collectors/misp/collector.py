# -*- coding: utf-8 -*-
"""
A collector for grabbing appropriately tagged events from MISP.

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - misp_verify: true or false, check the validity of the certificate
  - misp_tag_to_process: MISP tag identifying events to be processed
  - misp_tag_processed: MISP tag identifying events that have been processed

"""
import json
import sys

from intelmq.lib.bot import CollectorBot

try:
    if sys.version_info >= (3, 6):
        try:
            from pymisp import ExpandedPyMISP as PyMISP
        except ImportError:
            from pymisp import PyMISP
    else:
        from pymisp import PyMISP

except ImportError:
    PyMISP = None


class MISPCollectorBot(CollectorBot):

    def init(self):
        if PyMISP is None:
            raise ValueError('Could not import pymisp. Please install it.')

        # Initialize MISP connection
        self.misp = PyMISP(self.parameters.misp_url,
                           self.parameters.misp_key,
                           self.parameters.misp_verify)

    def process(self):
        # Grab the events from MISP
        misp_result = self.misp.search(
            tags=self.parameters.misp_tag_to_process
        )

        # Process the response and events
        if 'response' in misp_result:
            # Old response content
            misp_result = misp_result['response']

        # Extract the MISP event details
        for e in misp_result:
            misp_event = e['Event']

            # Send the results to the parser
            report = self.new_report()
            report.add('raw', json.dumps(misp_event, sort_keys=True))
            report.add('feed.url', self.parameters.misp_url)
            self.send_message(report)

        # Finally, update the tags on the MISP events.
        # Note PyMISP does not currently support this so we use
        # the API URLs directly with the requests module.

        for misp_event in misp_result:
            # Remove the 'to be processed' tag
            self.misp.untag(misp_event['uuid'],
                            self.parameters.misp_tag_to_process)

            # Add a 'processed' tag to the event
            self.misp.tag(misp_event['uuid'],
                          self.parameters.misp_tag_processed)


BOT = MISPCollectorBot
