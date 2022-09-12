# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
EVENTS = [
{   
    '__type': 'Event',
    'classification.identifier': 'open-elasticsearch',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.build_hash': '90f439ff60a3c0f497f91663701e64ccd01edbb4',
    'extra.build_snapshot': False,
    'extra.build_timestamp': '2016-07-27T10:36:52Z',
    'extra.cluster_name': 'elasticsearch',
    'extra.lucene_version': '5.5.0',
    'extra.name': 'Red Skull',
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'elasticsearch',
    'extra.tagline': 'You Know, for Search',
    'extra.version': '2.3.5',
    'feed.name': 'Open Elasticsearch',
    'protocol.application': 'elasticsearch',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 9200,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
   {'__type': 'Event',
    'classification.identifier': 'open-elasticsearch',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.build_hash': 'bee86328705acaa9a6daede7140defd4d9ec56bd',
    'extra.build_snapshot': False,
    'extra.cluster_name': 'docker-cluster',
    'extra.lucene_version': '8.11.1',
    'extra.name': 'allinonepod',
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'elasticsearch',
    'extra.tagline': 'You Know, for Search',
    'extra.version': '7.17.0',
    'feed.name': 'Open Elasticsearch',
    'protocol.application': 'elasticsearch',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 9200,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-elasticsearch',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.build_hash': '79d65f6e357953a5b3cbcc5e2c7c21073d89aa29',
    'extra.build_snapshot': False,
    'extra.cluster_name': 'docker-cluster',
    'extra.lucene_version': '8.9.0',
    'extra.name': 'f547c2952610',
    'extra.sector': 'Communications, Service Provider, and Hosting Service',
    'extra.tag': 'elasticsearch',
    'extra.tagline': 'You Know, for Search',
    'extra.version': '7.15.0',
    'feed.name': 'Open Elasticsearch',
    'protocol.application': 'elasticsearch',
    'protocol.transport': 'tcp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 9200,
    'source.reverse_dns': 'node03.example.com',
    'time.source': '2010-02-10T00:00:02+00:00'
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
