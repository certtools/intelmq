# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ftp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible FTP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2019-03-25T00:00:00+00:00",
                  "extra.file_name": "2019-03-25-scan_ftp-test-test.csv",
                  }
EVENTS = [{
            '__type': 'Event',
            'feed.name': 'Accessible FTP',
            'time.observation': '2019-03-25T00:00:00+00:00',
            'time.source': '2019-03-06T06:37:00+00:00',
            'classification.taxonomy': 'vulnerable',
            'classification.type': 'vulnerable service',
            'classification.identifier': 'accessible-ftp',
            'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
            'source.ip': '61.126.3.70',
            'source.port': 21,
            'protocol.transport': 'tcp',
            'protocol.application': 'ftp',
            'source.reverse_dns': 'arcus-net.co.jp',
            'extra.tag': 'ftp',
            'source.asn': 4713,
            'source.geolocation.cc': 'JP',
            'source.geolocation.region': 'TOKYO',
            'source.geolocation.city': 'TOKYO',
            'extra.naics': 517311,
            'extra.sic': 737401,
            'extra.banner': '220 FTP Server ready.|',
            'extra.handshake': 'TLSv1.2',
            'extra.cipher_suite': 'TLS_RSA_WITH_AES_128_CBC_SHA',
            'extra.cert_length':  2048,
            'extra.subject_common_name': '*.bizmw.com',
            'extra.issuer_common_name': 'GlobalSign Organization Validation CA - SHA256 - G2',
            'extra.cert_issue_date': 'Jan 14 08:04:50 2015 GMT',
            'extra.cert_expiration_date': 'Jan 14 08:04:50 2020 GMT',
            'extra.sha1_fingerprint': 'D9:98:3F:2E:F9:D1:BE:9A:10:1E:DE:51:2C:C1:DF:01:18:0A:20:65',
            'extra.cert_serial_number': '1121DC7421AB7924C3B1D396AEA3707E9E29',
            'extra.ssl_version': '2',
            'extra.signature_algorithm': 'sha256WithRSAEncryption',
            'extra.key_algorithm': 'rsaEncryption',
            'extra.subject_organization_name': 'NTT Communications Corporation',
            'extra.subject_country': 'JP',
            'extra.subject_state_or_province_name': 'Tokyo',
            'extra.subject_locality_name': 'Minato-ku',
            'extra.issuer_organization_name': 'GlobalSign nv-sa',
            'extra.issuer_country': 'BE',
            'extra.sha256_fingerprint': '27:4A:8A:3A:A7:DF:82:D0:43:03:0E:6F:48:30:30:C9:24:77:11:1A:08:EF:F7:B9:74:0C:CE:40:87:03:D2:51',
            'extra.sha512_fingerprint': 'E5:93:8B:72:84:0F:35:52:8E:7A:6C:E3:EF:36:90:4C:F2:86:A7:4D:B2:DD:C0:C6:23:83:18:EF:DD:86:34:92:91:57:22:29:75:45:71:8B:3A:CD:F1:27:A9:CA:5F:70:5E:AC:15:A5:E6:63:FD:6F:BB:C5:E2:45:99:73:E9:E6',
            'extra.md5_fingerprint': 'D1:A7:BC:96:78:1D:16:D0:24:A8:62:7C:3A:95:5A:4A',
            'extra.cert_valid': False,
            'extra.self_signed': False,
            'extra.cert_expired': False,
            'extra.validation_level': 'OV',
            'extra.auth_tls_response': '234 AUTH TLS successful',
          },
          {
            '__type': 'Event',
            'feed.name': 'Accessible FTP',
            'time.observation': '2019-03-25T00:00:00+00:00',
            'time.source': '2019-03-06T06:37:00+00:00',
            'classification.taxonomy': 'vulnerable',
            'classification.type': 'vulnerable service',
            'classification.identifier': 'accessible-ftp',
            'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
            'source.ip': '62.48.156.65',
            'source.port': 21,
            'protocol.transport': 'tcp',
            'protocol.application': 'ftp',
            'source.reverse_dns': 'dial-62-48-156-65.ptprime.net',
            'extra.tag': 'ftp',
            'source.asn': 15525,
            'source.geolocation.cc': 'PT',
            'source.geolocation.region': 'LISBOA',
            'source.geolocation.city': 'FRIELAS',
            'extra.banner': '220-================================================================|        PT Empresas|        Acesso Reservado|        Acesso nao autorizado punido por lei: 109/91; 67/98|    ----------------------------------------------------------------|        HENNES & MAURITZ LDA - 149093|        SITE: PT303 - Cascais Shopping|        MORADA: <MORADA>|        NIR: EWS1822940|    ================================================================|220 FTP server ready, 1 active clients of 4 simultaneous clients allowed.|',
            'extra.auth_tls_response': '500 Syntax error, command unrecognized.',
            'extra.auth_ssl_response': '500 Syntax error, command unrecognized.'
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
