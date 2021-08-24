# SPDX-FileCopyrightText: 2016 kralca
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""A collector for grabbing appropriately tagged events from MISP.

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - misp_tag_to_process: MISP tag identifying events to be processed
  - misp_tag_processed: MISP tag identifying events that have been processed


PyMISP versions released after January 2020 will no longer support the
"old" PyMISP class.
For compatibility:
 * older versions of pymisp still work with this bot
 * the deprecated parameter `misp_verify` will create a DeprecationWarning
"""
import json
import warnings
import sys

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    try:
        from pymisp import ExpandedPyMISP as PyMISP
    except ImportError:
        from pymisp import PyMISP
except ImportError:
    PyMISP = None
    import_fail_reason = 'import'


class MISPCollectorBot(CollectorBot):
    """Collect events from a MISP server"""
    misp_key: str = "<insert MISP Authkey>"
    misp_tag_processed: str = None
    misp_tag_to_process: str = "<insert MISP tag for events to be processed>"
    misp_url: str = "<insert url of MISP server (with trailing '/')>"
    rate_limit: int = 3600

    def init(self):
        if PyMISP is None:
            raise MissingDependencyError("pymisp")

        if hasattr(self, 'misp_verify'):
            self.http_verify_cert = self.misp_verify
            warnings.warn("The parameter 'misp_verify' is deprecated in favor of"
                          "'http_verify_cert'.", DeprecationWarning)

        # Initialize MISP connection
        self.misp = PyMISP(self.misp_url,
                           self.misp_key,
                           self.http_verify_cert)

    def process(self):
        # Grab the events from MISP
        misp_result = self.misp.search(
            tags=self.misp_tag_to_process
        )

        # Process the response and events

        # Compatibility with old pymisp versions before 2019:
        if 'response' in misp_result:
            misp_result = misp_result['response']

        # Extract the MISP event details
        for e in misp_result:
            misp_event = e['Event']

            # Send the results to the parser
            report = self.new_report()
            report.add('raw', json.dumps(misp_event, sort_keys=True))
            report.add('feed.url', self.misp_url)
            self.send_message(report)

        # Finally, update the tags on the MISP events.

        for e in misp_result:
            misp_event = e['Event']
            if self.misp_tag_processed is not None:
                # Add a 'processed' tag to the event
                self.misp.tag(misp_event['uuid'], self.misp_tag_processed)

            # Remove the 'to be processed' tag
            self.misp.untag(misp_event['uuid'], self.misp_tag_to_process)


BOT = MISPCollectorBot
