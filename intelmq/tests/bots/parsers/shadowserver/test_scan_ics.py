# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ics.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Acessible ICS',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_ics-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ics',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.device_model' : 'device_model',
   'extra.device_type' : 'device_type',
   'extra.device_vendor' : 'Vendor 1',
   'extra.device_version' : 'device_version',
   'extra.raw_response' : 'dGVzdDE=',
   'extra.response_size' : 5,
   'extra.source.sector' : 'Sector',
   'feed.name' : 'Acessible ICS',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'CITY',
   'source.geolocation.region' : 'REGION',
   'source.ip' : '192.168.0.1',
   'source.port' : 502,
   'source.reverse_dns' : 'host1.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-03-02T00:34:22+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ics',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.device_model' : 'device_model',
   'extra.device_type' : 'device_type',
   'extra.device_vendor' : 'Vendor 2',
   'extra.device_version' : 'device_version',
   'extra.raw_response' : 'dGVzdDI=',
   'extra.response_size' : 5,
   'extra.source.sector' : 'Sector',
   'feed.name' : 'Acessible ICS',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64513,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'CITY',
   'source.geolocation.region' : 'REGION',
   'source.ip' : '192.168.0.2',
   'source.port' : 502,
   'source.reverse_dns' : 'host2.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-03-02T00:34:22+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ics',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.device_model' : 'device_model',
   'extra.device_type' : 'device_type',
   'extra.device_vendor' : 'Vendor 3',
   'extra.device_version' : 'device_version',
   'extra.raw_response' : 'dGVzdDM=',
   'extra.response_size' : 5,
   'extra.source.sector' : 'Sector',
   'feed.name' : 'Acessible ICS',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64514,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'CITY',
   'source.geolocation.region' : 'REGION',
   'source.ip' : '192.168.0.3',
   'source.port' : 502,
   'source.reverse_dns' : 'host3.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-03-02T00:34:22+00:00'
}
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
