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
                       'testdata/event4_microsoft_sinkhole.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Microsoft Sinkhole",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_microsoft_sinkhole.csv",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'b68-zeroaccess-2-32bit',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'HK',
           'destination.geolocation.city': 'HONG KONG',
           'destination.geolocation.region': 'HONG KONG',
           'destination.ip': '168.63.134.179',
           'destination.port': 16464,
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517311,
           'feed.name': 'ShadowServer Microsoft Sinkhole',
           'malware.name': 'b68-zeroaccess-2-32bit',
           'protocol.transport': 'tcp',
           'source.asn': 7303,
           'source.geolocation.cc': 'AR',
           'source.geolocation.city': 'CASEROS',
           'source.geolocation.region': 'BUENOS AIRES',
           'source.ip': '190.229.1.2',
           'source.port': 52955,
           'time.source': '2021-06-07T00:00:00+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           },
          {'__type': 'Event',
           'classification.identifier': 'b68-zeroaccess-2-32bit',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'IE',
           'destination.geolocation.city': 'DUBLIN',
           'destination.geolocation.region': 'DUBLIN',
           'destination.ip': '52.169.3.4',
           'destination.port': 16464,
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517311,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'feed.name': 'ShadowServer Microsoft Sinkhole',
           'malware.name': 'b68-zeroaccess-2-32bit',
           'protocol.transport': 'tcp',
           'source.asn': 5769,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'LAVAL',
           'source.geolocation.region': 'QUEBEC',
           'source.ip': '96.20.3.4',
           'source.port': 16464,
           'time.source': '2021-06-07T00:00:00+00:00',
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
           'destination.ip': '168.63.134.179',
           'destination.port': 16464,
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517311,
           'feed.name': 'ShadowServer Microsoft Sinkhole',
           'malware.name': 'b68-zeroaccess-2-32bit',
           'protocol.transport': 'tcp',
           'source.asn': 8151,
           'source.geolocation.cc': 'MX',
           'source.geolocation.city': 'MEXICO CITY',
           'source.geolocation.region': "CIUDAD DE MEXICO",
           'source.ip': '187.222.5.6',
           'source.port': 55049,
           'time.source': '2021-06-07T00:00:00+00:00',
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
