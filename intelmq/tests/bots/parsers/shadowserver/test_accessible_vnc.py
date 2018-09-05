# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'accessible_vnc.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Accessible VNC",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Accessible VNC',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-vnc',
           'extra.product': 'RealVNC Enterprise v5.3 or later',
           'extra.banner': 'RFB 005.000',
           'protocol.application': 'vnc',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 64496,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '203.0.113.93',
           'source.port': 5900,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-03-06T16:03:10+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Accessible VNC',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-vnc',
           'extra.sic': 737415,
           'extra.product': 'VNC protocol 3.6',
           'extra.banner': 'RFB 003.006',
           'extra.naics': 518210,
           'protocol.application': 'vnc',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 64497,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'GRAZ',
           'source.geolocation.region': 'STEIERMARK',
           'source.ip': '198.18.0.123',
           'source.port': 5900,
           'source.reverse_dns': 'reverse_dns.example.com',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-03-06T16:03:12+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Accessible-VNC'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
