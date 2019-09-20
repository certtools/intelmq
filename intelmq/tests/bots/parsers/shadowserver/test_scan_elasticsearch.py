# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_elasticsearch.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Elasticsearch',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_elasticsearch-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open Elasticsearch',
           'classification.identifier': 'open-elasticsearch',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           'extra.build_hash': 'b9e4a6acad4008027e4038f6abed7f7dba346f94',
           'extra.build_snapshot': False,
           'extra.build_timestamp': '2016-04-21T16:03:47Z',
           'extra.cluster_name': 'Example Clustername',
           'extra.lucene_version': '5.5.0',
           'extra.name': 'Example Name',
           'extra.tag': 'elasticsearch',
           'extra.tagline': 'You Know, for Search',
           'extra.version': '2.3.2',
           'protocol.application': 'elasticsearch',
           'protocol.transport': 'tcp',
           'source.asn': 64496,
           'source.geolocation.cc': 'DE',
           'source.geolocation.city': 'FRANKFURT AM MAIN',
           'source.geolocation.region': 'HESSEN',
           'source.ip': '198.0.0.1',
           'source.port': 9200,
           'time.source': '2016-07-24T00:31:27+00:00',
           },
           {'__type': 'Event',
           'feed.name': 'Open Elasticsearch',
           'classification.identifier': 'open-elasticsearch',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           'extra.name': 'Silver Fox',
           'extra.ok': True,
           'extra.tag': 'elasticsearch',
           'extra.status': 200,
           'extra.tagline': 'You Know, for Search',
           'extra.version': '0.90.0.Bet',
           'protocol.application': 'elasticsearch',
           'protocol.transport': 'tcp',
           'source.asn': 42910,
           'source.geolocation.cc': 'TR',
           'source.geolocation.city': 'ISTANBUL',
           'source.geolocation.region': 'ISTANBUL',
           'source.ip': '31.210.46.170',
           'source.reverse_dns': 'trvds4.aysima.net',
           'source.port': 9200,
           'time.source': '2015-05-27T19:57:23+00:00',
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
