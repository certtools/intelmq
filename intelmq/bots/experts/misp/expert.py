# SPDX-FileCopyrightText: 2019 Raphaël Vinot
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
An expert to for looking up values in MISP.

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - http_verify_cert: true or false, check the validity of the certificate
"""
import sys

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from pymisp import ExpandedPyMISP
except ImportError:
    ExpandedPyMISP = None


class MISPExpertBot(Bot):
    """Looking up the IP address in MISP instance and retrieve attribute and event UUIDs"""
    misp_key: str = "<insert MISP Authkey>"
    misp_url: str = "<insert url of MISP server (with trailing '/')>"

    def init(self):
        if ExpandedPyMISP is None:
            raise MissingDependencyError('pymisp', '>=2.4.117.3')

        # Initialize MISP connection
        self.misp = ExpandedPyMISP(self.misp_url,
                                   self.misp_key,
                                   self.http_verify_cert)

    def process(self):
        event = self.receive_message()

        if 'source.ip' in event:

            # Grab the attributes from MISP
            # TODO: Run the query in reverse order (new->old)
            misp_result = self.misp.search('attributes', value=event['source.ip'],
                                           page=1, limit=1, pythonify=True)
            if misp_result:
                attribute = misp_result[0]
                # Process the response
                event.add('misp.attribute_uuid', attribute.uuid)
                event.add('misp.event_uuid', attribute.Event.uuid)

        self.send_message(event)
        self.acknowledge_message()


BOT = MISPExpertBot
