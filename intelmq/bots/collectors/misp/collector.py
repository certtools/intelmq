# -*- coding: utf-8 -*-
"""
A collector for grabbing appropriately tagged events from MISP.

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - misp_tag_to_process: MISP tag identifying events to be processed
  - misp_tag_processed: MISP tag identifying events that have been processed

"""
import json
import sys
import time
from urllib.parse import urljoin

import requests
from pymisp import PyMISP

from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Report


class MISPCollectorBot(Bot):

    def init(self):
        # Initialise MISP connection
        self.misp = PyMISP(self.parameters.misp_url,
                           self.parameters.misp_key, 'json')

        # URLs used for deleting and adding MISP event tags
        self.misp_add_tag_url = urljoin(self.parameters.misp_url,
                                        'events/addTag')
        self.misp_del_tag_url = urljoin(self.parameters.misp_url,
                                        'events/removeTag')

    def process(self):
        # Grab the events from MISP
        misp_result = self.misp.search(
            tags=self.parameters.misp_tag_to_process
        )

        # Process the response and events
        if 'response' in misp_result:

            # Extract the MISP event details
            misp_events = list()
            for result in misp_result['response']:
                misp_events.append(result['Event'])

            # Send the results to the parser
            report = Report()
            report.add('raw', json.dumps(misp_events, sort_keys=True))
            report.add('feed.name', self.parameters.feed)
            report.add('feed.url', self.parameters.misp_url)
            report.add('feed.accuracy', self.parameters.accuracy)
            self.send_message(report)

            # Finally, update the tags on the MISP events.
            # Note PyMISP does not currently support this so we use
            # the API URLs directly with the requests module.

            session = requests.Session()
            session.headers.update({
                'Authorization': self.misp.key,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
            post_data = {
                'request': {
                    'Event': {
                        'tag': None,
                        'id': None,
            }}}

            for misp_event in misp_events:
                post_data['request']['Event']['id'] = misp_event['id']

                # Remove the 'to be processed' tag
                tag = self.parameters.misp_tag_to_process
                post_data['request']['Event']['tag'] = tag
                session.post(self.misp_del_tag_url, data=json.dumps(post_data))

                # Add a 'processed' tag to the event
                tag = self.parameters.misp_tag_processed
                post_data['request']['Event']['tag'] = tag
                session.post(self.misp_add_tag_url, data=json.dumps(post_data))


if __name__ == '__main__':
    bot = MISPCollectorBot(sys.argv[1])
    bot.start()
