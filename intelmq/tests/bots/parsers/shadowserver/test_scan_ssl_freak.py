# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ssl_freak.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'SSL FREAK Vulnerable Servers',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ssl_freak-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'SSL FREAK Vulnerable Servers',
           "classification.identifier": "ssl-freak",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.browser_error": "x509: unknown error",
           "extra.browser_trusted": False,
           "extra.cert_expiration_date": "2032-05-05 00:01:19",
           "extra.cert_expired": False,
           "extra.cert_issue_date": "2012-05-10 00:01:19",
           "extra.cert_length": "1024",
           "extra.cert_serial_number": "4FAB054F",
           "extra.cert_valid": True,
           "extra.cipher_suite": "TLS_RSA_WITH_RC4_128_SHA",
           "extra.content_type": "text/html",
           "extra.freak_cipher_suite": "TLS_RSA_EXPORT_WITH_RC4_40_MD5",
           "extra.freak_vulnerable": True,
           "extra.handshake": "TLSv1.0",
           "extra.http_code": 200,
           "extra.http_date": "2018-04-23T13:25:26+00:00",
           "extra.http_reason": "OK",
           "extra.http_response_type": "HTTP/1.1",
           "extra.issuer_common_name": "usg50_B0B2DC2FA69D",
           "extra.key_algorithm": "rsaEncryption",
           "extra.md5_fingerprint": "1C:96:78:29:AA:E2:2E:11:AC:61:E5:AA:56:E1:91:BE",
           "extra.self_signed": True,
           "extra.sha1_fingerprint": "14:09:8C:6E:64:5F:50:C9:E9:A3:62:5E:02:BB:33:67:E1:05:D3:D2",
           "extra.sha256_fingerprint": "57:7A:FC:7C:A1:0F:79:11:67:E0:31:AC:66:F5:84:22:28:4E:AC:9D:27:A6:3E:93:84:D9:65:8C:FC:21:BF:A1",
           "extra.sha512_fingerprint": "E9:AE:EE:6C:D1:D1:9C:08:A5:8E:00:07:40:39:60:A0:CF:6D:A0:14:F0:A4:4C:47:28:9D:43:2E:A5:F6:45:66:3A:6F:5A:A4:CC:20:9A:FC:93:88:9B:BD:0B:EF:79:AF:EA:17:0A:08:6A:8A:98:9C:16:EC:94:1E:E7:C4:C7:87",
           "extra.signature_algorithm": "sha1WithRSAEncryption",
           "extra.subject_common_name": "usg50_B0B2DC2FA69D",
           "extra.tag": "ssl-freak",
           "extra.transfer_encoding": "chunked",
           "protocol.application": "https",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 8447,
           "source.geolocation.cc": "AT",
           "source.geolocation.city": "VIENNA",
           "source.geolocation.region": "WIEN",
           "source.ip": "198.51.100.232",
           "source.port": 443,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2018-04-23T13:25:21+00:00"
          },
          {'__type': 'Event',
           'feed.name': 'SSL FREAK Vulnerable Servers',
           "classification.identifier": "ssl-freak",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.browser_error": "x509: unknown error",
           "extra.browser_trusted": False,
           "extra.cert_expiration_date": "2029-12-27 00:00:53",
           "extra.cert_expired": False,
           "extra.cert_issue_date": "2010-01-01 00:00:53",
           "extra.cert_length": "1024",
           "extra.cert_serial_number": "4B3D3B35",
           "extra.cert_valid": True,
           "extra.cipher_suite": "TLS_RSA_WITH_RC4_128_SHA",
           "extra.content_type": "text/html",
           "extra.freak_cipher_suite": "TLS_RSA_EXPORT_WITH_RC4_40_MD5",
           "extra.freak_vulnerable": True,
           "extra.handshake": "TLSv1.0",
           "extra.http_code": 200,
           "extra.http_date": "2018-04-23T13:25:29+00:00",
           "extra.http_reason": "OK",
           "extra.http_response_type": "HTTP/1.1",
           "extra.issuer_common_name": "usg20w_C86C870287EC",
           "extra.key_algorithm": "rsaEncryption",
           "extra.md5_fingerprint": "1C:96:78:29:AA:E2:2E:11:AC:61:E5:AA:56:E1:91:BE",
           "extra.self_signed": True,
           "extra.sha1_fingerprint": "14:09:8C:6E:64:5F:50:C9:E9:A3:62:5E:02:BB:33:67:E1:05:D3:D2",
           "extra.sha256_fingerprint": "57:7A:FC:7C:A1:0F:79:11:67:E0:31:AC:66:F5:84:22:28:4E:AC:9D:27:A6:3E:93:84:D9:65:8C:FC:21:BF:A1",
           "extra.sha512_fingerprint": "E9:AE:EE:6C:D1:D1:9C:08:A5:8E:00:07:40:39:60:A0:CF:6D:A0:14:F0:A4:4C:47:28:9D:43:2E:A5:F6:45:66:3A:6F:5A:A4:CC:20:9A:FC:93:88:9B:BD:0B:EF:79:AF:EA:17:0A:08:6A:8A:98:9C:16:EC:94:1E:E7:C4:C7:87",
           "extra.signature_algorithm": "sha1WithRSAEncryption",
           "extra.subject_common_name": "usg20w_C86C870287EC",
           "extra.tag": "ssl-freak",
           "extra.transfer_encoding": "chunked",
           "protocol.application": "https",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 12577,
           "source.geolocation.cc": "AT",
           "source.geolocation.city": "BADEN",
           "source.geolocation.region": "NIEDEROSTERREICH",
           "source.ip": "198.51.100.224",
           "source.port": 443,
           "source.reverse_dns": "198-51-100-224.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2018-04-23T13:25:26+00:00"
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
