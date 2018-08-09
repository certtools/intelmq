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
           'classification.identifier': 'SSL-Poodle',
           'extra': '{"browser_error": "x509: unknown error", "browser_trusted": false, '
                    '"cert_expiration_date": "2034-06-20 00:00:42", "cert_expired": '
                    'false, "cert_issue_date": "2014-06-25 00:00:42", "cert_length": '
                    '"1024", "cert_serial_number": "53AA112A", "cert_valid": true, '
                    '"cipher_suite": "TLS_RSA_WITH_RC4_128_SHA", "content_type": '
                    '"text/html", "handshake": "TLSv1.0", "http_code": 200, "http_date": '
                    '"2018-08-08T00:51:44+00:00", "http_reason": "OK", '
                    '"http_response_type": "HTTP/1.1", "issuer_common_name": '
                    '"usg20_107BEF394BA5", "key_algorithm": "rsaEncryption", '
                    '"md5_fingerprint": '
                    '"33:E3:61:3F:5D:AA:96:99:38:A5:D6:F1:11:C7:ED:FC", "self_signed": '
                    'true, "sha1_fingerprint": '
                    '"04:FA:DE:1D:BD:4A:05:25:61:FB:F3:D6:64:74:66:44:01:22:D7:C3", '
                    '"sha256_fingerprint": '
                    '"16:25:9F:C7:A1:8D:64:1F:D9:25:42:BF:87:5C:4F:F3:63:14:97:21:EC:B6:67:10:F2:CA:52:37:C9:FE:49:2E", '
                    '"sha512_fingerprint": '
                    '"0B:2D:48:8C:4B:55:8B:F3:AB:F8:45:ED:E0:A0:63:F4:84:2F:4C:19:DC:A8:6F:7D:6A:AF:61:D7:98:AA:58:0F:CB:CA:87:D2:C3:0B:C5:DF:49:A7:84:7C:47:58:89:7D:92:B6:7B:98:7D:B1:64:4B:DC:DD:BE:9D:11:2A:D1:AE", '
                    '"signature_algorithm": "sha1WithRSAEncryption", "ssl_poodle": true, '
                    '"ssl_version": "2", "subject_common_name": "usg20_107BEF394BA5", '
                    '"tag": "ssl-poodle", "transfer_encoding": "chunked"}',
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
           'raw': 'InRpbWVzdGFtcCIsImlwIiwicG9ydCIsImhvc3RuYW1lIiwidGFnIiwiaGFuZHNoYWtlIiwiYXNuIiwiZ2VvIiwicmVnaW9uIiwiY2l0eSIsImNpcGhlcl9zdWl0ZSIsInNzbF9wb29kbGUiLCJjZXJ0X2xlbmd0aCIsInN1YmplY3RfY29tbW9uX25hbWUiLCJpc3N1ZXJfY29tbW9uX25hbWUiLCJjZXJ0X2lzc3VlX2RhdGUiLCJjZXJ0X2V4cGlyYXRpb25fZGF0ZSIsInNoYTFfZmluZ2VycHJpbnQiLCJjZXJ0X3NlcmlhbF9udW1iZXIiLCJzc2xfdmVyc2lvbiIsInNpZ25hdHVyZV9hbGdvcml0aG0iLCJrZXlfYWxnb3JpdGhtIiwic3ViamVjdF9vcmdhbml6YXRpb25fbmFtZSIsInN1YmplY3Rfb3JnYW5pemF0aW9uX3VuaXRfbmFtZSIsInN1YmplY3RfY291bnRyeSIsInN1YmplY3Rfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsInN1YmplY3RfbG9jYWxpdHlfbmFtZSIsInN1YmplY3Rfc3RyZWV0X2FkZHJlc3MiLCJzdWJqZWN0X3Bvc3RhbF9jb2RlIiwic3ViamVjdF9zdXJuYW1lIiwic3ViamVjdF9naXZlbl9uYW1lIiwic3ViamVjdF9lbWFpbF9hZGRyZXNzIiwic3ViamVjdF9idXNpbmVzc19jYXRlZ29yeSIsInN1YmplY3Rfc2VyaWFsX251bWJlciIsImlzc3Vlcl9vcmdhbml6YXRpb25fbmFtZSIsImlzc3Vlcl9vcmdhbml6YXRpb25fdW5pdF9uYW1lIiwiaXNzdWVyX2NvdW50cnkiLCJpc3N1ZXJfc3RhdGVfb3JfcHJvdmluY2VfbmFtZSIsImlzc3Vlcl9sb2NhbGl0eV9uYW1lIiwiaXNzdWVyX3N0cmVldF9hZGRyZXNzIiwiaXNzdWVyX3Bvc3RhbF9jb2RlIiwiaXNzdWVyX3N1cm5hbWUiLCJpc3N1ZXJfZ2l2ZW5fbmFtZSIsImlzc3Vlcl9lbWFpbF9hZGRyZXNzIiwiaXNzdWVyX2J1c2luZXNzX2NhdGVnb3J5IiwiaXNzdWVyX3NlcmlhbF9udW1iZXIiLCJuYWljcyIsInNpYyIsInNlY3RvciIsInNoYTI1Nl9maW5nZXJwcmludCIsInNoYTUxMl9maW5nZXJwcmludCIsIm1kNV9maW5nZXJwcmludCIsImh0dHBfcmVzcG9uc2VfdHlwZSIsImh0dHBfY29kZSIsImh0dHBfcmVhc29uIiwiY29udGVudF90eXBlIiwiaHR0cF9jb25uZWN0aW9uIiwid3d3X2F1dGhlbnRpY2F0ZSIsInNldF9jb29raWUiLCJzZXJ2ZXJfdHlwZSIsImNvbnRlbnRfbGVuZ3RoIiwidHJhbnNmZXJfZW5jb2RpbmciLCJodHRwX2RhdGUiLCJjZXJ0X3ZhbGlkIiwic2VsZl9zaWduZWQiLCJjZXJ0X2V4cGlyZWQiLCJicm93c2VyX3RydXN0ZWQiLCJ2YWxpZGF0aW9uX2xldmVsIiwiYnJvd3Nlcl9lcnJvciIKIjIwMTgtMDgtMDggMDA6NTE6NDIiLCIyMDMuMC4xMTMuODUiLCI4NDQzIiwiZXhhbXBsZS5jb20iLCJzc2wtcG9vZGxlIiwiVExTdjEuMCIsIjY1NTQwIiwiQVQiLCJXSUVOIiwiVklFTk5BIiwiVExTX1JTQV9XSVRIX1JDNF8xMjhfU0hBIiwiWSIsIjEwMjQiLCJ1c2cyMF8xMDdCRUYzOTRCQTUiLCJ1c2cyMF8xMDdCRUYzOTRCQTUiLCIyMDE0LTA2LTI1IDAwOjAwOjQyIiwiMjAzNC0wNi0yMCAwMDowMDo0MiIsIjA0OkZBOkRFOjFEOkJEOjRBOjA1OjI1OjYxOkZCOkYzOkQ2OjY0Ojc0OjY2OjQ0OjAxOjIyOkQ3OkMzIiwiNTNBQTExMkEiLCIyIiwic2hhMVdpdGhSU0FFbmNyeXB0aW9uIiwicnNhRW5jcnlwdGlvbiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIiIsIjAiLCIwIiwiIiwiMTY6MjU6OUY6Qzc6QTE6OEQ6NjQ6MUY6RDk6MjU6NDI6QkY6ODc6NUM6NEY6RjM6NjM6MTQ6OTc6MjE6RUM6QjY6Njc6MTA6RjI6Q0E6NTI6Mzc6Qzk6RkU6NDk6MkUiLCIwQjoyRDo0ODo4Qzo0Qjo1NTo4QjpGMzpBQjpGODo0NTpFRDpFMDpBMDo2MzpGNDo4NDoyRjo0QzoxOTpEQzpBODo2Rjo3RDo2QTpBRjo2MTpENzo5ODpBQTo1ODowRjpDQjpDQTo4NzpEMjpDMzowQjpDNTpERjo0OTpBNzo4NDo3Qzo0Nzo1ODo4OTo3RDo5MjpCNjo3Qjo5ODo3RDpCMTo2NDo0QjpEQzpERDpCRTo5RDoxMToyQTpEMTpBRSIsIjMzOkUzOjYxOjNGOjVEOkFBOjk2Ojk5OjM4OkE1OkQ2OkYxOjExOkM3OkVEOkZDIiwiSFRUUC8xLjEiLCIyMDAiLCJPSyIsInRleHQvaHRtbCIsIiIsIiIsIiIsIiIsIiIsImNodW5rZWQiLCJXZWQsIDA4IEF1ZyAyMDE4IDAwOjUxOjQ0IEdNVCIsIlkiLCJZIiwiTiIsIk4iLCJ1bmtub3duIiwieDUwOTogdW5rbm93biBlcnJvciIK',
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
        cls.sysconfig = {'feedname': 'Ssl-Scan'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
