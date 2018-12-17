# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot


with open(os.path.join(os.path.dirname(__file__), 'accessible-rsync.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Accessible Rsync",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'accessible-rsync',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.module': 'Public;foo;bar;',
           'extra.password': False,
           'extra.tag': 'rsync',
           'feed.name': 'ShadowServer Accessible Rsync',
           'protocol.application': 'rsync',
           'protocol.transport': 'tcp',
           'source.asn': 65536,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'STEYR',
           'source.geolocation.region': 'OBEROSTERREICH',
           'source.ip': '10.10.10.1',
           'source.port': 873,
           'source.reverse_dns': 'foo.example.com',
           'time.source': '2018-10-22T11:11:11+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           },
          {'__type': 'Event',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'classification.identifier': 'accessible-rsync',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.module': 'Shared folder;',
           'extra.password': False,
           'extra.tag': 'rsync',
           'feed.name': 'ShadowServer Accessible Rsync',
           'protocol.application': 'rsync',
           'protocol.transport': 'tcp',
           'source.asn': 65537,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'SALZBURG',
           'source.geolocation.region': 'SALZBURG',
           'source.ip': '10.10.10.2',
           'source.port': 873,
           'source.reverse_dns': 'bar.example.com',
           'time.source': '2018-10-22T11:11:12+00:00',
           'time.observation': '2015-01-01T00:00:00+00:00',
           },
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Accessible-Rsync'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
