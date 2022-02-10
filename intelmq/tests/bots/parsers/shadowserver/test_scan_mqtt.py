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
   'extra.source.naics' : 454110,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : '*.tracesafe.io',
   'extra.tag' : 'mqtt',
   'feed.name' : 'Open-MQTT',
   'protocol.application' : 'mqtt',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsImlwIiwicHJvdG9jb2wiLCJwb3J0IiwiaG9zdG5hbWUiLCJ0YWciLCJhc24iLCJnZW8iLCJyZWdpb24iLCJjaXR5IiwibmFpY3MiLCJzaWMiLCJhbm9ueW1vdXNfYWNjZXNzIiwicmF3X3Jlc3BvbnNlIiwiaGV4X2NvZGUiLCJjb2RlIiwiY2lwaGVyX3N1aXRlIiwiY2VydF9sZW5ndGgiLCJzdWJqZWN0X2NvbW1vbl9uYW1lIiwiaXNzdWVyX2NvbW1vbl9uYW1lIiwiY2VydF9pc3N1ZV9kYXRlIiwiY2VydF9leHBpcmF0aW9uX2RhdGUiLCJzaGExX2ZpbmdlcnByaW50Iiwic2hhMjU2X2ZpbmdlcnByaW50Iiwic2hhNTEyX2ZpbmdlcnByaW50IiwibWQ1X2ZpbmdlcnByaW50IiwiY2VydF9zZXJpYWxfbnVtYmVyIiwic3NsX3ZlcnNpb24iLCJzaWduYXR1cmVfYWxnb3JpdGhtIiwia2V5X2FsZ29yaXRobSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX25hbWUiLCJzdWJqZWN0X29yZ2FuaXphdGlvbl91bml0X25hbWUiLCJzdWJqZWN0X2NvdW50cnkiLCJzdWJqZWN0X3N0YXRlX29yX3Byb3ZpbmNlX25hbWUiLCJzdWJqZWN0X2xvY2FsaXR5X25hbWUiLCJzdWJqZWN0X3N0cmVldF9hZGRyZXNzIiwic3ViamVjdF9wb3N0YWxfY29kZSIsInN1YmplY3Rfc3VybmFtZSIsInN1YmplY3RfZ2l2ZW5fbmFtZSIsInN1YmplY3RfZW1haWxfYWRkcmVzcyIsInN1YmplY3RfYnVzaW5lc3NfY2F0ZWdvcnkiLCJzdWJqZWN0X3NlcmlhbF9udW1iZXIiLCJpc3N1ZXJfb3JnYW5pemF0aW9uX25hbWUiLCJpc3N1ZXJfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsImlzc3Vlcl9jb3VudHJ5IiwiaXNzdWVyX3N0YXRlX29yX3Byb3ZpbmNlX25hbWUiLCJpc3N1ZXJfbG9jYWxpdHlfbmFtZSIsImlzc3Vlcl9zdHJlZXRfYWRkcmVzcyIsImlzc3Vlcl9wb3N0YWxfY29kZSIsImlzc3Vlcl9zdXJuYW1lIiwiaXNzdWVyX2dpdmVuX25hbWUiLCJpc3N1ZXJfZW1haWxfYWRkcmVzcyIsImlzc3Vlcl9idXNpbmVzc19jYXRlZ29yeSIsImlzc3Vlcl9zZXJpYWxOdW1iZXIiCiIyMDIyLTAyLTA3IDEyOjU2OjUzIiwiMTguMjIwLjAuMCIsInRjcCIsODg4MywiMTgtMjIwLTAtMC5leGFtcGxlLmNvbSIsIm1xdHQiLDEyMzQ1LCJVUyIsIk9ISU8iLCJDT0xVTUJVUyIsNDU0MTEwLCwiTiIsMjAwMjAwMDUsMDUsIkNvbm5lY3Rpb24gUmVmdXNlZCwgbm90IGF1dGhvcml6ZWQiLCJUTFNfRUNESEVfUlNBX1dJVEhfQUVTXzEyOF9HQ01fU0hBMjU2IiwyMDQ4LCIqLnRyYWNlc2FmZS5pbyIsIlNlY3RpZ28gUlNBIERvbWFpbiBWYWxpZGF0aW9uIFNlY3VyZSBTZXJ2ZXIgQ0EiLCIyMDIwLTA4LTEyIDAwOjAwOjAwIiwiMjAyMi0xMS0xNCAwMDowMDowMCIsIjcwOjg0OkYxOjZEOjI4OkRBOkI2OkU2OjI3OjYwOjEzOjhCOjJDOjkzOjUyOkI2OjdCOjRCOjEzOjdCIiwiRDI6RDc6NTQ6NTI6RUI6ODY6NEU6MkQ6MzQ6NEQ6RkM6Q0U6Q0Q6Q0Y6Mzk6NDE6RTE6MDY6NUM6OEI6Qjg6NTQ6RTY6MEM6REY6RkQ6NkU6RTM6RjE6QjU6NDE6MDAiLCIxNzo1NzpGQjo4ODo5RDpCRTpBNzpGMDoyOTpBNTozMTpGQzo3OTpERjpGNzo4QToxQzpENjo0QTpERjoxQjo0QTpEQzpCRjowNTpFNzpFODoyRjo3OTo5QTpGQTpGRTpGNzpFODo2NjoyMjpDQjpCOTo0Qzo3MjpGNzpGQjo2QzoxRDo1OTo4Qzo1NDo2Mzo3MDowNTpERTo3RjozQzoyRjpCQTpCODozNzoxODpDRToyOTo2RjoxMTpFODpBQiIsIkRFOjJDOjk4OjMwOjI3OjJFOjdEOkM5OkVEOkEzOjlEOkFGOjlFOkNFOjE0OkNDIiwiMDg1Njk5NzQzQTIzMTE0QzlCNkI4REM5NzVBOEFGNDIiLDIsInNoYTI1NldpdGhSU0FFbmNyeXB0aW9uIiwicnNhRW5jcnlwdGlvbiIsLCwsLCwsLCwsLCwsIlNlY3RpZ28gTGltaXRlZCIsLCJHQiIsIkdyZWF0ZXIgTWFuY2hlc3RlciIsIlNhbGZvcmQiLCwsLCwsLA==',
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
