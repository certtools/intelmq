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
                       'testdata/scan_netbios.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Netbios',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_netbios-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'open-netbios-nameservice',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 4.58,
    'extra.mac_address': '00-00-00-00-00-00',
    'extra.machine_name': 'NBG6503',
    'extra.response_size': 229,
    'extra.tag': 'netbios',
    'feed.name': 'Netbios',
    'protocol.application': 'netbios-nameservice',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.account': 'NBG6503',
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 137,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-netbios-nameservice',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.86,
    'extra.mac_address': '00-00-00-00-00-00',
    'extra.machine_name': 'NAS-OLD',
    'extra.response_size': 193,
    'extra.tag': 'netbios',
    'extra.workgroup': 'PRACOWNIAELN.',
    'feed.name': 'Netbios',
    'protocol.application': 'netbios-nameservice',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.account': 'NAS-OLD',
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 137,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'open-netbios-nameservice',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 3.14,
    'extra.mac_address': '00-25-90-F0-64-64',
    'extra.machine_name': 'HR-SRV01',
    'extra.response_size': 157,
    'extra.sector': 'Government',
    'extra.tag': 'netbios',
    'extra.workgroup': 'HRSIGMA',
    'feed.name': 'Netbios',
    'protocol.application': 'netbios-nameservice',
    'protocol.transport': 'udp',
    'raw': 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJtYWNfYWRkcmVzcyIsImFzbiIsImdlbyIsInJlZ2lvbiIsImNpdHkiLCJ3b3JrZ3JvdXAiLCJtYWNoaW5lX25hbWUiLCJ1c2VybmFtZSIsIm5haWNzIiwic2ljIiwic2VjdG9yIiwicmVzcG9uc2Vfc2l6ZSIsImFtcGxpZmljYXRpb24iCiIyMDEwLTAyLTEwIDAwOjAwOjAyIiwxOTIuMTY4LjAuMyx1ZHAsMTM3LG5vZGUwMy5leGFtcGxlLmNvbSxuZXRiaW9zLDAwLTI1LTkwLUYwLTY0LTY0LDY0NTEyLFpaLFJlZ2lvbixDaXR5LEhSU0lHTUEsSFItU1JWMDEsLDAsMCxHb3Zlcm5tZW50LDE1NywzLjE0',
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 137,
    'source.reverse_dns': 'node03.example.com',
    'time.source': '2010-02-10T00:00:02+00:00'
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
