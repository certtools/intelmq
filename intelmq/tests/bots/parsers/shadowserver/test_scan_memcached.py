# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_memcached.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Memcached',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_memcached-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open Memcached',
           "classification.identifier": "open-memcached",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.curr_connections": 10,
           "extra.pid": 2787,
           "extra.pointer_size": 64,
           "extra.tag": "memcached",
           "extra.time": "2016-07-24 00:37:50",
           "extra.total_connections": 40,
           "extra.uptime": 2043742,
           "extra.version": "1.4.13",
           "protocol.application": "memcached",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 3209,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "GELSENKIRCHEN",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.4",
           "source.port": 11211,
           "source.reverse_dns": "198-51-100-4.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:37:50+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open Memcached',
           "classification.identifier": "open-memcached",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.curr_connections": 30,
           "extra.pid": 7147,
           "extra.pointer_size": 64,
           "extra.tag": "memcached",
           "extra.time": "2016-07-24 00:37:51",
           "extra.total_connections": 35609,
           "extra.uptime": 752706,
           "extra.version": "1.4.4",
           "protocol.application": "memcached",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 20773,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "WEEZE",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.182",
           "source.port": 11211,
           "source.reverse_dns": "198-51-100-182.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:37:51+00:00"
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

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
