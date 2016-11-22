# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.bitcash.parser import BitcashBlocklistParserBot

with open(os.path.join(os.path.dirname(__file__), 'blacklist')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {'feed.url': 'http://bitcash.cz/misc/log/blacklist',
                 'feed.name': 'bitcash_blocklist',
                 '__type': 'Report',
                 'raw': utils.base64_encode(EXAMPLE_FILE),
                 'time.observation': '2016-11-21T20:05:54+00:00'
                  }

EXAMPLE_EVENT = [{'feed.url': 'http://bitcash.cz/misc/log/blacklist',
                 'feed.name': 'bitcash_blocklist',
                 'time.source': '2016-10-01T00:15:01+00:00',
                 'source.ip': '81.95.123.209',
                 'source.reverse_dns': 'npvpn.dco.fusa.be',
                 'classification.type': 'scanner',
                 'event_description.text': 'IPs banned for serious abusing of Bitcash services (scanning, sniffing, harvesting, dos attacks)',
                 'raw': 'ODEuOTUuMTIzLjIwOSwjLG5wdnBuLmRjby5mdXNhLmJlLGxhc3QsYWNjZXNzLDIwMTYtMTAtMDEsMDA6MTU6MDE=',
                 '__type': 'Event'
                 },
                 {'feed.url': 'http://bitcash.cz/misc/log/blacklist',
                 'feed.name': 'bitcash_blocklist',
                 'time.source': '2016-10-01T17:10:01+00:00',
                 'source.ip': '194.213.39.138',
                 'classification.type': 'scanner',
                 'event_description.text': 'IPs banned for serious abusing of Bitcash services (scanning, sniffing, harvesting, dos attacks)',
                 'raw': 'MTk0LjIxMy4zOS4xMzgsIywxOTQuMjEzLjM5LjEzOCxsYXN0LGFjY2VzcywyMDE2LTEwLTAxLDE3OjEwOjAx',
                 '__type': 'Event'
                  }]


class TestBitcashBlocklistParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase of BitcashBlockListParserBot """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BitcashBlocklistParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Events have been produced """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT[0])
        self.assertMessageEqual(1, EXAMPLE_EVENT[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
