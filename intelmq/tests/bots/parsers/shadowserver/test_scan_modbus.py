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
                       'testdata/scan_modbus.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Acessible Modbus',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_modbus-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-modbus',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.conformity_level' : '1',
   'extra.function_code' : '43',
   'extra.object_count' : '3',
   'extra.product_code' : '145',
   'extra.raw_response' : 'DgEVVDSsACFSb2Nrd2VsbCBBdXRvbWF0aW9uIEFsbGVuLUJyYWRsZXkBAzE0NQIFMDkuMEI=',
   'extra.response_length' : 55,
   'extra.revision' : '09.0B',
   'extra.source.sector' : 'information',
   'extra.tag' : 'modbus',
   'extra.vendor' : 'Rockwell Automation Allen-Bradley',
   'feed.name' : 'Acessible Modbus',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'PL',
   'source.geolocation.city' : 'WARSAW',
   'source.geolocation.region' : 'MAZOWIECKIE',
   'source.ip' : '87.251.0.0',
   'source.port' : 502,
   'source.reverse_dns' : 'scan.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-16T12:29:04+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-modbus',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.conformity_level' : '1',
   'extra.function_code' : '43',
   'extra.object_count' : '3',
   'extra.product_code' : 'AMiNi4DW2    - NOS166 - DbNET',
   'extra.raw_response' : 'DgEBAAADACBBTWHDGYUEB2wuIHMgci5vLiBQcmFoYSAgICAgICAgIAEgQU1pTmk0RFcyICAgIC0gTk9TMTY2IC0gRGJORVQgICAC',
   'extra.response_length' : 110,
   'extra.revision' : 'V1.00        - V3.72  - V1.51',
   'extra.source.sector' : 'information',
   'extra.tag' : 'modbus',
   'extra.vendor' : 'AMiT spol. s r.o. Praha',
   'feed.name' : 'Acessible Modbus',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'CZ',
   'source.geolocation.city' : 'PRAGUE',
   'source.geolocation.region' : 'PRAHA',
   'source.ip' : '89.24.0.0',
   'source.port' : 502,
   'source.reverse_dns' : 'scan.example.net',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-16T12:29:04+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-modbus',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.conformity_level' : '129',
   'extra.function_code' : '43',
   'extra.object_count' : '3',
   'extra.product_code' : '2020',
   'extra.raw_response' : 'DgGBAADBFADTY2huZWlkZXIgRWxlY3RyaWMgIAEMQk1YIFAzNCAyMDIwAgR2Mi45',
   'extra.response_length' : 50,
   'extra.revision' : 'v2.9',
   'extra.source.naics' : 517311,
   'extra.tag' : 'modbus',
   'extra.vendor' : 'Schneider Electric',
   'feed.name' : 'Acessible Modbus',
   'protocol.application' : 'modbus',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ES',
   'source.geolocation.city' : 'MADRID',
   'source.geolocation.region' : 'MADRID',
   'source.ip' : '212.169.0.0',
   'source.port' : 502,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-02-16T12:29:04+00:00'
}]


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
