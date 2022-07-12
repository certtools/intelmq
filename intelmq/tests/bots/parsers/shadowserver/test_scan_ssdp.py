# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ssdp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open SSDP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ssdp-test-geo.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'open-ssdp',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.content_type' : 'plex/media-server',
   'extra.header' : 'HTTP/1.0 200 OK',
   'extra.instance' : 'DESKTOP-DJ4NNGP',
   'extra.resource_identifier' : 'e9d68a3332542938345388a40001be08f8907b32',
   'extra.server' : 'c6ca79537ead4f14aa1456890f9d5c71.plex.direct',
   'extra.server_port' : '32400',
   'extra.naics' : 517311,
   'extra.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'plex',
   'extra.updated_at' : '1644185489',
   'extra.version' : '1.19.3.2764-ef515a800',
   'feed.name' : 'Open SSDP',
   'protocol.application' : 'ssdp',
   'protocol.transport' : 'udp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 12345,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'LITTLETON',
   'source.geolocation.region' : 'COLORADO',
   'source.ip' : '98.53.0.0',
   'source.port' : 32414,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-02-07T06:11:01+00:00'
}
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
