# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_sinkhole.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Sinkhole",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_sinkhole.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 28753,
           'destination.geolocation.cc': 'DE',
           'destination.geolocation.city': 'FRANKFURT AM MAIN',
           'destination.geolocation.region': 'HESSEN',
           'destination.ip': '178.162.1.2',
           'destination.port': 4455,
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.public_source': 'eset',
           'feed.name': 'ShadowServer Sinkhole',
           'malware.name': 'victorygate.b',
           'protocol.transport': 'tcp',
           'source.asn': 12252,
           'source.geolocation.cc': 'PE',
           'source.geolocation.city': 'LIMA',
           'source.geolocation.region': 'METROPOLITANA DE LIMA',
           'source.ip': '190.113.1.2',
           'source.port': 17409,
           'time.source': '2021-03-04T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'b68-zeroaccess-2-32bit',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'SG',
           'destination.geolocation.city': 'SINGAPORE',
           'destination.geolocation.region': 'CENTRAL',
           'destination.ip': '137.116.3.4',
           'destination.port': 16464,
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 541611,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'feed.name': 'ShadowServer Sinkhole',
           'protocol.transport': 'tcp',
           'source.asn': 8220,
           'source.geolocation.cc': 'IE',
           'source.geolocation.city': 'DUBLIN',
           'source.geolocation.region': 'DUBLIN',
           'source.ip': '217.173.3.4',
           'source.port': 28940,
           'time.source': '2021-03-04T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'b68-zeroaccess-2-32bit',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'HK',
           'destination.geolocation.city': 'HONG KONG',
           'destination.geolocation.region': 'HONG KONG',
           'destination.ip': '168.63.5.6',
           'destination.port': 16464,
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'feed.name': 'ShadowServer Sinkhole',
           'protocol.transport': 'tcp',
           'source.asn': 6697,
           'source.geolocation.cc': 'BY',
           'source.geolocation.city': 'VITEBSK',
           'source.geolocation.region': "VITEBSKAJA OBLAST'",
           'source.ip': '37.212.5.6',
           'source.port': 36735,
           'time.source': '2021-03-04T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
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
