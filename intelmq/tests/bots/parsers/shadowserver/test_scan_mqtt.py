# SPDX-FileCopyrightText: 2020 Thomas Hungenberg
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mqtt.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open-MQTT',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2020-03-15T00:00:00+00:00",
                  "extra.file_name": "2020-03-14-scan_mqtt-test-geo.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'open-mqtt',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.anonymous_access' : False,
   'extra.cert_expiration_date' : '2022-11-14 00:00:00',
   'extra.cert_issue_date' : '2020-08-12 00:00:00',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '085699743A23114C9B6B8DC975A8AF42',
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
   'extra.code' : 'Connection Refused, not authorized',
   'extra.hex_code' : '05',
   'extra.issuer_common_name' : 'Sectigo RSA Domain Validation Secure Server CA',
   'extra.issuer_country' : 'GB',
   'extra.issuer_locality_name' : 'Salford',
   'extra.issuer_organization_name' : 'Sectigo Limited',
   'extra.issuer_state_or_province_name' : 'Greater Manchester',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'DE:2C:98:30:27:2E:7D:C9:ED:A3:9D:AF:9E:CE:14:CC',
   'extra.raw_response' : '20020005',
   'extra.sha1_fingerprint' : '70:84:F1:6D:28:DA:B6:E6:27:60:13:8B:2C:93:52:B6:7B:4B:13:7B',
   'extra.sha256_fingerprint' : 'D2:D7:54:52:EB:86:4E:2D:34:4D:FC:CE:CD:CF:39:41:E1:06:5C:8B:B8:54:E6:0C:DF:FD:6E:E3:F1:B5:41:00',
   'extra.sha512_fingerprint' : '17:57:FB:88:9D:BE:A7:F0:29:A5:31:FC:79:DF:F7:8A:1C:D6:4A:DF:1B:4A:DC:BF:05:E7:E8:2F:79:9A:FA:FE:F7:E8:66:22:CB:B9:4C:72:F7:FB:6C:1D:59:8C:54:63:70:05:DE:7F:3C:2F:BA:B8:37:18:CE:29:6F:11:E8:AB',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.naics' : 454110,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : '*.tracesafe.io',
   'extra.tag' : 'mqtt',
   'feed.name' : 'Open-MQTT',
   'protocol.application' : 'mqtt',
   'protocol.transport' : 'tcp',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 12345,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'COLUMBUS',
   'source.geolocation.region' : 'OHIO',
   'source.ip' : '18.220.0.0',
   'source.port' : 8883,
   'source.reverse_dns' : '18-220-0-0.example.com',
   'time.observation' : '2020-03-15T00:00:00+00:00',
   'time.source' : '2022-02-07T12:56:53+00:00'
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
