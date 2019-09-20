# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ipmi.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open IPMI',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ipmi-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open IPMI',
           "classification.identifier": "open-ipmi",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.anon_login": False,
           "extra.defaultkg": "-",
           "extra.ipmi_version": "1.5",
           "extra.md2_auth": False,
           "extra.md5_auth": True,
           "extra.naics": "0",
           "extra.none_auth": True,
           "extra.nulluser": True,
           "extra.oem_auth": False,
           "extra.passkey_auth": True,
           "extra.permessage_auth": True,
           "extra.sic": "0",
           "extra.tag": "ipmi",
           "extra.userlevel_auth": True,
           "extra.usernames": False,
           "protocol.application": "ipmi",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 2914,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "BERLIN",
           "source.geolocation.region": "BERLIN",
           "source.ip": "198.51.100.4",
           "source.port": 623,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:09:42+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open IPMI',
           "classification.identifier": "open-ipmi",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.anon_login": False,
           "extra.defaultkg": "default",
           "extra.ipmi_version": "2.0",
           "extra.md2_auth": False,
           "extra.md5_auth": False,
           "extra.naics": "0",
           "extra.none_auth": False,
           "extra.nulluser": False,
           "extra.oem_auth": False,
           "extra.passkey_auth": False,
           "extra.permessage_auth": False,
           "extra.sic": "0",
           "extra.tag": "ipmi",
           "extra.userlevel_auth": True,
           "extra.usernames": True,
           "protocol.application": "ipmi",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 28753,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "FRANKFURT AM MAIN",
           "source.geolocation.region": "HESSEN",
           "source.ip": "198.51.100.182",
           "source.port": 623,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:09:43+00:00"
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
