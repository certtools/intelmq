# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'accessible-cisco-smart-install.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Accessible Cisco Smart Install",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Accessible Cisco Smart Install',
           'classification.identifier': 'accessible-cisco-smart-install',
           'classification.type': 'vulnerable service',
           'classification.taxonomy': 'vulnerable',
           'protocol.application': 'cisco-smart-install',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 8559,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '198.51.100.103',
           'source.port': 4786,
           'extra.tag': 'cisco-smart-install',
           'source.reverse_dns': '198-51-100-103.example.net',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-11-18T08:42:45+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Accessible Cisco Smart Install',
           'classification.identifier': 'accessible-cisco-smart-install',
           'classification.type': 'vulnerable service',
           'classification.taxonomy': 'vulnerable',
           'protocol.application': 'cisco-smart-install',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 35609,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '198.51.100.218',
           'source.port': 4786,
           'extra.tag': 'cisco-smart-install',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-11-18T08:47:54+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Accessible-Cisco-Smart-Install'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
