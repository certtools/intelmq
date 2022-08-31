# SPDX-FileCopyrightText: 2019 Guillermo Rodriguez
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ubiquiti.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open Ubiquiti',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-03-04T00:00:00+00:00",
                  "extra.file_name": "2019-03-25-scan_ubiquiti-test-test.csv",
                  }
EVENTS = [
{
    '__type': 'Event',
    'classification.identifier': 'accessible-ubiquiti-discovery-service',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 37.0,
    'extra.essid': 'Kachine-Meta-Lidia-Tereixa',
    'extra.firmwarerev': 'XS5.ar2313.v3.5.4494.091109.1459',
    'extra.mac_address': '00156db98c3a',
    'extra.model': 'NS5',
    'extra.radio_name': 'kachine.meta.lidia.tereixa',
    'extra.response_size': 148,
    'extra.tag': 'ubiquiti,iot',
    'feed.name': 'Open Ubiquiti',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.1',
    'source.port': 10001,
    'source.reverse_dns': 'node01.example.com',
    'time.source': '2010-02-10T00:00:00+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-ubiquiti-discovery-service',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 39.0,
    'extra.essid': 'Adana-Mason-Lanikai-Ozaner',
    'extra.firmwarerev': 'XM.ar7240.v5.6.3.28591.151130.1749',
    'extra.mac_address': '00156d7c9188',
    'extra.model': 'LM5',
    'extra.model_full': 'NanoStation Loco M5',
    'extra.radio_name': 'adana.mason.lanikai.ozaner',
    'extra.response_size': 156,
    'extra.tag': 'ubiquiti,iot',
    'feed.name': 'Open Ubiquiti',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.2',
    'source.port': 10001,
    'source.reverse_dns': 'node02.example.com',
    'time.source': '2010-02-10T00:00:01+00:00'
},
{
    '__type': 'Event',
    'classification.identifier': 'accessible-ubiquiti-discovery-service',
    'classification.taxonomy': 'vulnerable',
    'classification.type': 'vulnerable-system',
    'extra.amplification': 36.25,
    'extra.essid': 'Tailynn-Kadija-Noreen-Dinkar',
    'extra.firmwarerev': 'XW.ar934x.v5.6.5.29033.160515.2108',
    'extra.mac_address': '0418d6000fd5',
    'extra.model': 'P2B-400',
    'extra.model_full': 'PowerBeam M2 400',
    'extra.radio_name': 'tailynn.kadija.noreen.dinkar',
    'extra.response_size': 145,
    'extra.tag': 'ubiquiti,iot',
    'feed.name': 'Open Ubiquiti',
    'protocol.transport': 'udp',
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
    'source.asn': 64512,
    'source.geolocation.cc': 'ZZ',
    'source.geolocation.city': 'City',
    'source.geolocation.region': 'Region',
    'source.ip': '192.168.0.3',
    'source.port': 10001,
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
