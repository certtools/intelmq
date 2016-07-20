# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'chargen.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Chargen",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'classification.taxonomy': 'Other',
           'extra': '{"naics": 123456, "response_size": 116, "sic": 654321, '
                    '"tag": "chargen"}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1], ''])),
           'source.asn': 12969,
           'source.geolocation.cc': 'IS',
           'source.geolocation.city': 'REYKJAVIK',
           'source.geolocation.region': 'HOFUOBORGARSVAOIO',
           'source.ip': '88.149.23.230',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'classification.taxonomy': 'Other',
           'extra': '{"response_size": 116, "tag": "chargen"}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2], ''])),
           'source.asn': 45543,
           'source.geolocation.cc': 'VN',
           'source.geolocation.city': 'THANH PHO HO CHI MINH',
           'source.geolocation.region': 'HO CHI MINH',
           'source.ip': '112.197.240.1',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'classification.taxonomy': 'Other',
           'extra': '{"response_size": 116, "tag": "chargen"}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3], ''])),
           'source.asn': 3269,
           'source.geolocation.cc': 'IT',
           'source.geolocation.city': 'ROMA',
           'source.geolocation.region': 'LAZIO',
           'source.ip': '85.36.146.26',
           'source.port': 19,
           'source.reverse_dns': 'host26-146-static.36-85-b.business.telecomit'
           'alia.it',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'classification.taxonomy': 'Other',
           'extra': '{"response_size": 116, "tag": "chargen"}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[4], ''])),
           'source.asn': 6327,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'VICTORIA',
           'source.geolocation.region': 'BRITISH COLUMBIA',
           'source.ip': '184.69.168.237',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'classification.taxonomy': 'Other',
           'extra': '{"response_size": 116, "tag": "chargen"}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[5], ''])),
           'source.asn': 6360,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'HONOLULU',
           'source.geolocation.region': 'HAWAII',
           'source.ip': '128.171.32.12',
           'source.port': 19,
           'source.reverse_dns': 'dhcp-128-171-32-12.bilger.hawaii.edu',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Open-Chargen'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':
    unittest.main()
