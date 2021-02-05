# -*- coding: utf-8 -*-

import os
import unittest
import json

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser_json import ShadowserverJSONParserBot
from intelmq.tests.bots.parsers.shadowserver.test_testdata import csvtojson

EXAMPLE_FILE = csvtojson(os.path.join(os.path.dirname(__file__), 'testdata/scan_smb.csv'))

EXAMPLE_REPORT = {
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_smb-test-geo.csv",
                  }

EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible-SMB',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-smb',
           'extra.smb_implant': False,
           'protocol.application': 'smb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode(json.dumps([json.loads(EXAMPLE_FILE)[0]])),
           'source.asn': 8559,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'EISENSTADT',
           'source.geolocation.region': 'BURGENLAND',
           'source.ip': '198.51.100.39',
           'source.port': 445,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-06-24T06:12:04+00:00'},
           {'__type': 'Event',
           'feed.name': 'Accessible-SMB',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.smb_implant': True,
           'extra.arch': 'x86',
           'extra.key': '0xcb68e558',
           'classification.identifier': 'open-smb',
           'protocol.application': 'smb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode(json.dumps([json.loads(EXAMPLE_FILE)[1]])),
           'source.asn': 8447,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'GUNSKIRCHEN',
           'source.geolocation.region': 'OBEROSTERREICH',
           'source.ip': '198.51.100.94',
           'source.port': 445,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-06-24T06:22:59+00:00'},
          ]

class TestShadowserverJSONParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverJSONParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverJSONParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
