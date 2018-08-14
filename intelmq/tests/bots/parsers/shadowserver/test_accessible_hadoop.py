# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'accessible-hadoop.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Accessible-Hadoop",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Accessible-Hadoop',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-hadoop',
           'extra.version': '2.7.3, rbaa91f7c6bc9cb92be5982de4719c1c8af91ccff',
           'extra.server_type': 'namenode',
           'extra.clusterid': 'CID-64471a53-60cb-4302-9832-92f321f111fe',
           'extra.total_disk': 41567956992,
           'extra.used_disk': 53248,
           'extra.free_disk': 25160089600,
           'extra.livenodes': 'edmonton:50010',
           'protocol.application': 'hadoop',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 15296,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'CALGARY',
           'source.geolocation.region': 'ALBERTA',
           'source.ip': '199.116.235.200',
           'source.port': 50070,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-09-13T02:06:05+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Accessible-Hadoop',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-hadoop',
           'extra.version': '2.7.1.2.4.0.0-169',
           'extra.naics': 334111,
           'extra.sic': 357101,
           'extra.server_type': 'datanode',
           'extra.clusterid': 'CID-771bae52-9e4f-4ec4-bc1a-c867585751f0',
           'extra.namenodeaddress': 'sandbox.hortonworks.com',
           'extra.volumeinfo': '/hadoop/hdfs/data/current',
           'protocol.application': 'hadoop',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 8075,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'DES MOINES',
           'source.geolocation.region': 'IOWA',
           'source.ip': '104.43.235.92',
           'source.port': 50075,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-09-13T02:07:48+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Accessible-Hadoop'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
