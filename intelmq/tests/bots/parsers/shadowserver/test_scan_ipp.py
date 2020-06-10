# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_ipp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open-IPP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-06-09T00:00:00+00:00",
                  "extra.file_name": "2020-06-08-scan_ipp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open-IPP',
           "classification.identifier": "open-ipp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.naics": 517311,
           "extra.tag": "ipp",
           "extra.ipp_version": "IPP/2.1",
           "extra.cups_version": "CUPS/2.0",
           "extra.printer_uris": "ipp://123.45.67.89:631/ipp/print",
           "extra.printer_name": "NPI3F0D22",
           "extra.printer_info": "HP Color LaserJet MFP M277dw",
           "extra.printer_more_info": "http://123.45.67.89:631/hp/device/info_config_AirPrint.html?tab=Networking&menu=AirPrintStatus",
           "extra.printer_make_and_model": "HP Color LaserJet MFP M277dw",
           "extra.printer_firmware_name": "20191203",
           "extra.printer_firmware_string_version": "20191203",
           "extra.printer_firmware_version": "20191203",
           "extra.printer_organization": "org",
           "extra.printer_organization_unit": "unit",
           "extra.printer_uuid": "urn:uuid:456e4238-4a44-4643-4c42-10e1813f0a18",
           "extra.printer_wifi_ssid": "wifissid",
           "protocol.application": "ipp",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 12345,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "CITY",
           "source.geolocation.region": "REGION",
           "source.ip": "123.45.67.89",
           "source.port": 631,
           'source.reverse_dns': 'some.host.com',
           "time.observation": "2020-06-09T00:00:00+00:00",
           "time.source": "2020-06-08T11:30:14+00:00"
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
