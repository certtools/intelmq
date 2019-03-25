# -*- coding: utf-8 -*-
import json
import os
import unittest

from intelmq.bots.parsers.microsoft.parser_ctip import MicrosoftCTIPParserBot
from intelmq.lib import test
from intelmq.lib.utils import base64_encode


with open(os.path.join(os.path.dirname(__file__), 'ctip.txt')) as handle:
    EXAMPLE_DATA = handle.read()
EXAMPLE_PARSED = json.loads(EXAMPLE_DATA)


EXAMPLE_REPORT = {
    "__type": "Report",
    "feed.accuracy": 100.0,
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": base64_encode(EXAMPLE_DATA)
}

EXAMPLE_EVENTS = [{
    "__type": "Event",
    'classification.type': 'infected system',
    'destination.ip': '198.18.18.18',
    'destination.port': 443,
    'event_description.text': 'Host is a member of Botnet B85-R2S',
    'extra.ispartnershareable': 'true',
    'extra.isproductlicensed': 'true',
    'tlp': 'GREEN',
    'feed.accuracy': 20.0,
    'malware.name': 'b85-r2s',
    'source.asn': 65536,
    'source.ip': '224.0.5.8',
    'source.port': 1204,
    'time.source': '2018-02-06T09:37:02+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[0]], sort_keys=True)),
    }, {
    "__type": "Event",
    'classification.type': 'infected system',
    'destination.ip': '100.120.45.48',
    'destination.port': 80,
    'event_description.text': 'Host is a member of Botnet Conficker',
    'extra.ispartnershareable': 'true',
    'extra.isproductlicensed': 'true',
    'tlp': 'GREEN',
    'feed.accuracy': 100.0,
    'malware.name': 'conficker',
    'source.asn': 64496,
    'source.ip': '10.0.0.5',
    'source.port': 25310,
    'time.source': '2018-02-06T09:38:46+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[1]], sort_keys=True)),
    }, {
    "__type": "Event",
    'classification.type': 'infected system',
    'destination.ip': '203.0.113.212',
    'destination.port': 1085,
    'event_description.text': 'Host is a member of Botnet B106-Jenxcus',
    'extra.ispartnershareable': 'true',
    'extra.isproductlicensed': 'true',
    'tlp': 'GREEN',
    'feed.accuracy': 100.0,
    'malware.name': 'b106-jenxcus',
    'source.asn': 64511,
    'source.ip': '19.168.46.126',
    'source.port': 49970,
    'time.source': '2018-02-06T09:40:19+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[2]], sort_keys=True)),
    }, {
    "__type": "Event",
    'classification.type': 'infected system',
    'destination.port': 443,
    'event_description.text': 'Host is a member of Botnet B75-S12',
    'extra.additionalmetadata': [r'any??thing\x0000can\x01be!here??'],
    'extra.ispartnershareable': 'true',
    'extra.isproductlicensed': 'true',
    'tlp': 'GREEN',
    'feed.accuracy': 100.0,
    'malware.name': 'b75-s12',
    'source.asn': 65536,
    'source.ip': '198.51.100.100',
    'source.port': 42996,
    'time.source': '2018-02-06T09:43:19+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[3]], sort_keys=True)),
    }, {  # ignore hostname if invalid
    "__type": "Event",
    'classification.type': 'infected system',
    'destination.ip': '192.88.99.209',
    'destination.port': 16465,
    'event_description.text': 'Host is a member of Botnet B68-2-64',
    "extra.additionalmetadata": ["??\f??????9??\u001e??P??????%??a????????.??????\u0016/(????\u0006??$s????v????zU??,??????#_??d??\u0013????????????\u00131!}\u001e??2/+????@??P1??\u0016??????????<>tR??}^??t-h??G??F??+????l"],
    'extra.ispartnershareable': 'true',
    'extra.isproductlicensed': 'true',
    "extra.user_agent": "Q\u000bZk??8\u001d????????p??z????z??q)??\u001e\u0012??'??????,i3??????\u0006??q??\u0007d=????????-??b????={????????X??{iN}??\u0017\u0011\u0010|q??\u0014",
    'tlp': 'GREEN',
    'feed.accuracy': 100.0,
    'malware.name': 'b68-2-64',
    'source.asn': 64504,
    'source.ip': '224.34.234.52',
    'source.port': 55522,
    'time.source': '2019-03-17T09:05:50+00:00',
    "raw": base64_encode(json.dumps([EXAMPLE_PARSED[4]], sort_keys=True)),
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
        for i in range(5):
            self.assertMessageEqual(i, EXAMPLE_EVENTS[i])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
