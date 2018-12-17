# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'db2.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Open-DB2-Discovery-Service",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Open-DB2-Discovery-Service',
           'classification.identifier': 'open-db2-discovery-service',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.size': 298,
           'extra.servername': 'server1',
           'extra.tag': 'db2',
           'extra.db2_hostname': 'server1.net',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 4837,
           'source.geolocation.cc': 'CN',
           'source.geolocation.city': 'JINAN',
           'source.geolocation.region': 'SHANDONG',
           'source.ip': '221.0.111.99',
           'source.port': 523,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2016-05-17T19:09:38+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Open-DB2-Discovery-Service',
           'classification.identifier': 'open-db2-discovery-service',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.naics': 541690,
           'extra.sic': 874899,
           'extra.size': 298,
           'extra.servername': 'kronos',
           'extra.tag': 'db2',
           'extra.db2_hostname': 'kronos.net',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 3320,
           'source.geolocation.cc': 'DE',
           'source.geolocation.city': 'NUREMBERG',
           'source.geolocation.region': 'BAYERN',
           'source.ip': '217.241.57.135',
           'source.port': 523,
           'source.reverse_dns': 'pd9f13987.dip0.t-ipconnect.de',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2016-05-17T19:09:44+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Open-DB2-Discovery-Service'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
