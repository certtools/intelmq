# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mssql.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open MSSQL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_mssql-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open MSSQL',
           "classification.identifier": "open-mssql",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.amplification": 18.49,
           "extra.instance_name": "MSSQLSERVER",
           "extra.named_pipe": "\\\\EXAMPLEURL",
           "extra.response_length": 832,
           "extra.tag": "mssql",
           "extra.tcp_port": 1433,
           "extra.version": "10.50.4000.0",
           "protocol.application": "mssql",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 8972,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "WEEZE",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.152",
           "source.local_hostname": "EXAMPLESERVERNAME",
           "source.port": 1434,
           "source.reverse_dns": "198-51-100-152.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T06:39:24+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open MSSQL',
           "classification.identifier": "open-mssql",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.amplification": 10.27,
           "extra.instance_name": "ACT7",
           "extra.named_pipe": "\\\\EXAMPLEURL",
           "extra.response_length": 462,
           "extra.tag": "mssql",
           "extra.tcp_port": 49180,
           "extra.version": "10.50.1600.1",
           "protocol.application": "mssql",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 20773,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "COLOGNE",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.67",
           "source.local_hostname": "EXAMPLESERVERNAME",
           "source.port": 1434,
           "source.reverse_dns": "198-51-100-67.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T06:39:25+00:00"
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
