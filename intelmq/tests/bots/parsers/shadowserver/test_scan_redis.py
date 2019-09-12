# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_redis.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Redis',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_redis-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open Redis',
           "classification.identifier": "open-redis",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.build_id": "26069fb482f6334b",
           "extra.connected_clients": "50",
           "extra.gcc_version": "4.7.2",
           "extra.git_sha1": "00000000",
           "extra.mode": "standalone",
           "extra.multiplexing_api": "epoll",
           "extra.naics": 541512,
           "extra.os.name": "Linux 3.2.0-4-amd64 x86_64",
           "extra.process_id": "2127",
           "extra.run_id": "d440b0b2fb3d1db655ad607e11e6f38011a0f599",
           "extra.sic": 737999,
           "extra.tag": "redis",
           "extra.uptime": "27946314",
           "extra.version": "2.8.19",
           "protocol.application": "redis",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 201229,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "FRANKFURT AM MAIN",
           "source.geolocation.region": "HESSEN",
           "source.ip": "198.51.100.152",
           "source.port": 6379,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:42:33+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open Redis',
           "classification.identifier": "open-redis",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.build_id": "e41bf84a0cecf09d",
           "extra.connected_clients": "25376",
           "extra.gcc_version": "4.8.4",
           "extra.git_sha1": "00000000",
           "extra.mode": "standalone",
           "extra.multiplexing_api": "epoll",
           "extra.os.name": "Linux 3.18.24-sirzion x86_64",
           "extra.process_id": "343519",
           "extra.run_id": "53d63f23511dc0080b49aaa8e8203d65619f1c8c",
           "extra.tag": "redis",
           "extra.uptime": "310556",
           "extra.version": "3.0.6",
           "protocol.application": "redis",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 12586,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "FRANKFURT AM MAIN",
           "source.geolocation.region": "HESSEN",
           "source.ip": "198.51.100.67",
           "source.port": 6379,
           "source.reverse_dns": "198-51-100-67.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:42:43+00:00"
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
