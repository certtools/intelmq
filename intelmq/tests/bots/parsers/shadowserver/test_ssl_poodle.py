# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'ssl_poodle.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer SSL POODLE",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'ssl-poodle',
           'extra.browser_error': 'x509: unknown error',
           'extra.browser_trusted': False,
           'extra.cert_expiration_date': '2034-06-20 00:00:42',
           'extra.cert_expired': False,
           'extra.cert_issue_date': '2014-06-25 00:00:42',
           'extra.cert_length': '1024',
           'extra.cert_serial_number': '53AA112A',
           'extra.cert_valid': True,
           'extra.cipher_suite': 'TLS_RSA_WITH_RC4_128_SHA',
           'extra.content_type': 'text/html',
           'extra.handshake': 'TLSv1.0',
           'extra.http_code': 200,
           'extra.http_date': '2018-08-08T00:51:44+00:00',
           'extra.http_reason': 'OK',
           'extra.http_response_type': 'HTTP/1.1',
           'extra.issuer_common_name': 'usg20_107BEF394BA5',
           'extra.key_algorithm': 'rsaEncryption',
           'extra.md5_fingerprint': '33:E3:61:3F:5D:AA:96:99:38:A5:D6:F1:11:C7:ED:FC',
           'extra.self_signed': True,
           'extra.sha1_fingerprint': '04:FA:DE:1D:BD:4A:05:25:61:FB:F3:D6:64:74:66:44:01:22:D7:C3',
           'extra.sha256_fingerprint': '16:25:9F:C7:A1:8D:64:1F:D9:25:42:BF:87:5C:4F:F3:63:14:97:21:EC:B6:67:10:F2:CA:52:37:C9:FE:49:2E',
           'extra.sha512_fingerprint': '0B:2D:48:8C:4B:55:8B:F3:AB:F8:45:ED:E0:A0:63:F4:84:2F:4C:19:DC:A8:6F:7D:6A:AF:61:D7:98:AA:58:0F:CB:CA:87:D2:C3:0B:C5:DF:49:A7:84:7C:47:58:89:7D:92:B6:7B:98:7D:B1:64:4B:DC:DD:BE:9D:11:2A:D1:AE',
           'extra.signature_algorithm': 'sha1WithRSAEncryption',
           'extra.ssl_poodle': True,
           'extra.ssl_version': '2',
           'extra.subject_common_name': 'usg20_107BEF394BA5',
           'extra.tag': 'ssl-poodle',
           'extra.transfer_encoding': 'chunked',
           'feed.name': 'ShadowServer SSL POODLE',
           'protocol.application': 'https',
           'source.asn': 65540,
           'source.geolocation.cc': 'AT',
           'source.geolocation.city': 'VIENNA',
           'source.geolocation.region': 'WIEN',
           'source.ip': '203.0.113.85',
           'source.port': 8443,
           'source.reverse_dns': 'example.com',
           'time.source': '2018-08-08T00:51:42+00:00',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           '__type': 'Event',
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
        cls.sysconfig = {'feedname': 'SSL-POODLE-Vulnerable-Servers'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
