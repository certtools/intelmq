# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.openphish.parser_commercial import OpenPhishCommercialParserBot

with open(os.path.join(os.path.dirname(__file__), 'feed_commercial.txt'), 'r') as fh:
    FILE = fh.read()
RAW = utils.base64_encode(FILE.encode())
SPLITTED = FILE.splitlines()

OUTPUT1 = {"source.url": "http://example.com/glossy/zip/secure/d553c33636b465c21554b757e48bcf04/",
           "source.ip": "104.24.119.70",
           "time.source": "2018-02-06T15:16:06+00:00",
           "source.as_name": "Example Pete",
           "source.asn": 13335,
           "source.fqdn": "example.com",
           "source.geolocation.cc": "US",
           "raw": utils.base64_encode(SPLITTED[0]),
           "extra.brand": "Webmail Providers",
           "extra.country_name": "United States",
           "extra.discover_time": "06-02-2018 15:16:06 UTC",
           "extra.family_id": "922070603a96d81be0e354099d62f54e",
           "extra.sector": "Email Provider",
           "extra.tld": "ga",
           "classification.type": "phishing",
           "__type": "Event",
           }
OUTPUT2 = {"source.url": "http://signin.eby.de.h7r9pganeatdzn6.civpro.example.com/?Ct5A47GsT3bMpTNwYXCmsa6JR7ylCJx2tpr3GordYJZnl",
           "source.ip": "196.41.123.211",
           "time.source": "2018-02-06T15:13:22+00:00",
           "source.as_name": "Example Richard",
           "source.asn": 36874,
           "source.fqdn": "signin.eby.de.h7r9pganeatdzn6.civpro.example.com",
           "source.geolocation.cc": "ZA",
           "raw": utils.base64_encode(SPLITTED[1]),
           "extra.brand": "eBay Inc.",
           "extra.country_name": "South Africa",
           "extra.discover_time": "06-02-2018 15:13:22 UTC",
           "extra.family_id": "3513702e078b6e6d70bb7f9abbf40cd6",
           "extra.sector": "e-Commerce",
           "extra.tld": "co.za",
           "classification.type": "phishing",
           "__type": "Event",
           }


class TestOpenPhishCommercialParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenPhishCommercialParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenPhishCommercialParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
