# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.spamhaus.parser_drop import SpamhausDropParserBot

with open(os.path.join(os.path.dirname(__file__), 'drop.txt')) as handle:
    NETWORK_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'asndrop.txt')) as handle:
    ASN_FILE = handle.read()

NETWORK_REPORT = {'feed.name': 'Spamhaus drop feed',
                  'feed.url': 'https://www.spamhaus.org/drop/drop.txt',
                  '__type': 'Report',
                  'time.observation': '2016-11-29T17:26:00+00:00',
                  'raw': utils.base64_encode(NETWORK_FILE)
                 }

NETWORK_EVENTS = [{'feed.name': 'Spamhaus drop feed',
                   'feed.url': 'https://www.spamhaus.org/drop/drop.txt',
                   '__type': 'Event',
                   'time.observation': '2016-11-29T17:26:00+00:00',
                   'time.source': '2015-09-14T04:39:22+00:00',
                   'classification.type': 'spam',
                   'source.network': '1.4.0.0/17',
                   'extra': '{"blocklist": "SBL256893"}',
                   'raw': 'MS40LjAuMC8xNyA7IFNCTDI1Njg5Mw==',
                  },
                  {'feed.name': 'Spamhaus drop feed',
                   'feed.url': 'https://www.spamhaus.org/drop/drop.txt',
                   '__type': 'Event',
                   'time.observation': '2016-11-29T17:26:00+00:00',
                   'time.source': '2015-09-14T04:39:22+00:00',
                   'classification.type': 'spam',
                   'source.network': '2a06:e480::/29',
                   'extra': '{"blocklist": "SBL301771"}',
                   'raw': 'MmEwNjplNDgwOjovMjkgOyBTQkwzMDE3NzE=',
                  }]

ASN_REPORT = {'feed.name': 'Spamhaus ASN feed',
              'feed.url': 'https://www.spamhaus.org/drop/asndrop.txt',
              '__type': 'Report',
              'time.observation': '2016-11-29T17:26:00+00:00',
              'raw': utils.base64_encode(ASN_FILE)
             }

ASN_EVENTS = [{'feed.name': 'Spamhaus ASN feed',
               'feed.url': 'https://www.spamhaus.org/drop/asndrop.txt',
               '__type': 'Event',
               'time.observation': '2016-11-29T17:26:00+00:00',
               'time.source': '2015-09-14T04:39:22+00:00',
               'classification.type': 'spam',
               'source.asn': 260,
               'source.as_name': 'XCONNECT24 - Xconnect24 Inc., US',
               'source.geolocation.cc': 'AE',
               'raw': 'QVMyNjAgOyBBRSB8IFhDT05ORUNUMjQgLSBYY29ubmVjdDI0IEluYy4sIFVT',
              },
              {'feed.name': 'Spamhaus ASN feed',
               'feed.url': 'https://www.spamhaus.org/drop/asndrop.txt',
               '__type': 'Event',
               'time.observation': '2016-11-29T17:26:00+00:00',
               'time.source': '2015-09-14T04:39:22+00:00',
               'classification.type': 'spam',
               'source.asn': 10516,
               'source.as_name': 'Orb-bit Design Group',
               'raw': 'QVMxMDUxNiA7IHwgT3JiLWJpdCBEZXNpZ24gR3JvdXA=',
              }]


class TestSpamhausDropParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for SpamhausDropParserBot with Network and ASN feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SpamhausDropParserBot
        cls.default_input_message = NETWORK_REPORT

    def test_network(self):
        """ Test if correct IP Events have been produced. """
        self.run_bot()
        self.assertMessageEqual(0, NETWORK_EVENTS[0])
        self.assertMessageEqual(1, NETWORK_EVENTS[1])

    def test_asn(self):
        """ Test if correct ASN Events have been produced. """
        self.input_message = ASN_REPORT
        self.run_bot()
        self.assertMessageEqual(0, ASN_EVENTS[0])
        self.assertMessageEqual(1, ASN_EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
