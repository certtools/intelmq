# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'Accessible-SMB.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

with open(os.path.join(os.path.dirname(__file__),
                       'Accessible-SMB_reconstructed.csv')) as handle:
    RECONSTRUCTED_FILE = handle.read()
RECONSTRUCTED_LINES = RECONSTRUCTED_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Accessible-SMB",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Accessible-SMB',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'opensmb',
           'extra.smb_implant': False,
           'protocol.application': 'smb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[1], ''])),
           'source.asn': 8559,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'EISENSTADT',
           'source.geolocation.region': 'BURGENLAND',
           'source.ip': '198.51.100.39',
           'source.port': 445,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-06-24T06:12:04+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Accessible-SMB',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.smb_implant': True,
           'extra.arch': 'x86',
           'extra.key': '0xcb68e558',
           'classification.identifier': 'opensmb',
           'protocol.application': 'smb',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[2], ''])),
           'source.asn': 8447,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'GUNSKIRCHEN',
           'source.geolocation.region': 'OBEROSTERREICH',
           'source.ip': '198.51.100.94',
           'source.port': 445,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2017-06-24T06:22:59+00:00'},
          ]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Accessible-SMB'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
