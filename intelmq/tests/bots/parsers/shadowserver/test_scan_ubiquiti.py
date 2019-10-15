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
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open Ubiquiti',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-ubiquiti-discovery-service',
           'time.source': '2019-02-04T15:34:33+00:00',
           'source.ip': '177.22.68.220',
           'protocol.transport': 'udp',
           'source.port': 10001,
           'source.reverse_dns': '220.68.22.177.strnet.com.br',
           'extra.tag': 'ubiquiti',
           'source.asn': 262890,
           'source.geolocation.cc': 'BR',
           'source.geolocation.region': 'SAO PAULO',
           'source.geolocation.city': 'TAMBAU',
           'extra.mac_address': '0027223ae564',
           'extra.radio_name': 'Sartori Tecnologia',
           'extra.essid': 'NETTAMBAU23N-2',
           'extra.model': 'AG5-HP',
           'extra.firmwarerev': 'XM.ar7240.v6.0.4-licensed.30805.170505.1649',
           'extra.response_size': 164,
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2018-03-04T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'Open Ubiquiti',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'accessible-ubiquiti-discovery-service',
           'time.source': '2019-02-04T15:34:33+00:00',
           'source.ip': '195.32.35.53',
           'protocol.transport': 'udp',
           'source.port': 10001,
           'source.reverse_dns': 'c-35-53.cust.wadsl.it',
           'extra.tag': 'ubiquiti',
           'source.asn': 205005,
           'source.geolocation.cc': 'IT',
           'source.geolocation.region': 'ASTI',
           'source.geolocation.city': 'MONTECHIARO D\'ASTI',
           'extra.mac_address': '802aa8b03d28',
           'extra.radio_name': 'DETTORI Daniela',
           'extra.essid': 'find-adsl',
           'extra.model': 'LB5',
           'extra.firmwarerev': 'XW.ar934x.v6.0.4.30805.170505.1510',
           'extra.response_size': 142,
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.observation': '2018-03-04T00:00:00+00:00'}
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
