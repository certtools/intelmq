# -*- coding: utf-8 -*-
"""
           "Tags": "extra.tags",
"""
import json
import os
import unittest

from intelmq.bots.parsers.microsoft.parser_bingmurls import MicrosoftCTIPParserBot
from intelmq.lib import test
from intelmq.lib.utils import base64_encode


with open(os.path.join(os.path.dirname(__file__), 'bingmurls.json')) as handle:
    EXAMPLE_DATA = handle.read()
EXAMPLE_PARSED = json.loads(EXAMPLE_DATA)


EXAMPLE_REPORT = {
    "__type": "Report",
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": base64_encode(EXAMPLE_DATA)
}

EXAMPLE_EVENTS = [{
    "__type": "Event",
    'classification.type': 'blacklist',
    'classification.identifier': 'MaliciousUrl',
    'event_description.text': 'Website has been identified as malicious by Bing',
    'extra.ispartnershareable': True,
    'extra.isproductlicensed': True,
    'tlp': 'AMBER',
    'source.url': 'http://01.example.com/foobar.html',
    'source.asn': 65540,
    'source.ip': '127.5.9.48',
    'source.port': 80,
    'time.source': '2018-05-28T07:00:00+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[0]], sort_keys=True)),
    'extra.attributable': True,
    'extra.indicator_provider': 'Bing',
    'extra.indicator_expiration_date_time': '2018-06-28T10:49:29Z',
    'extra.threat_detection_product': 'Forefront',
    'extra.tags': ['com'],
    }, {
    "__type": "Event",
    'classification.type': 'blacklist',
    'classification.identifier': 'MaliciousUrl',
    'event_description.text': 'Website has been identified as malicious by Bing',
    'extra.ispartnershareable': True,
    'extra.isproductlicensed': True,
    'tlp': 'AMBER',
    'source.url': 'http://010302.example.org/',
    'source.asn': 64510,
    'source.ip': '198.51.48.124',
    'source.port': 80,
    'time.source': '2018-05-28T07:00:00+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[1]], sort_keys=True)),
    'extra.attributable': True,
    'extra.indicator_provider': 'Bing',
    'extra.indicator_expiration_date_time': '2018-06-28T10:49:29Z',
    'extra.threat_detection_product': 'Forefront',
    'extra.tags': ['org'],
    },
    ]


class TestMicrosoftCTIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for the MicrosoftCTIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MicrosoftCTIPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        for i, event in enumerate(EXAMPLE_EVENTS):
            self.assertMessageEqual(i, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
