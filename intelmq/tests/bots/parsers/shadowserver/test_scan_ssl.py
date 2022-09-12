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
                       'testdata/scan_ssl.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible SSL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2022-01-07T00:00:00+00:00",
                  "extra.file_name": "2022-01-07-scan_ssl-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_error' : 'x509: unknown error',
   'extra.browser_trusted' : False,
   'extra.cert_expiration_date' : '2038-01-19 03:14:07',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2014-06-23 09:56:32',
   'extra.cert_length' : 1024,
   'extra.cert_serial_number' : '168CAE',
   'extra.cert_valid' : True,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
   'extra.content_length' : 131,
   'extra.content_type' : 'text/html',
   'extra.freak_vulnerable' : False,
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : 'support',
   'extra.issuer_country' : 'US',
   'extra.issuer_email_address' : 'support@fortinet.com',
   'extra.issuer_locality_name' : 'Sunnyvale',
   'extra.issuer_organization_name' : 'Fortinet',
   'extra.issuer_organization_unit_name' : 'Certificate Authority',
   'extra.issuer_state_or_province_name' : 'California',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '99:45:1F:2E:AE:EB:88:91:27:43:33:79:FA:93:7D:CA',
   'extra.self_signed' : False,
   'extra.server_type' : 'xxxxxxxx-xxxxx',
   'extra.sha1_fingerprint' : '5A:3D:FF:06:F9:E9:25:37:57:F9:09:52:33:A4:85:15:24:2D:88:7F',
   'extra.sha256_fingerprint' : '35:AB:B6:76:2A:3D:17:B2:FB:40:45:1B:FC:0A:99:0A:6E:48:57:F7:30:0A:3B:B1:1A:E6:99:70:5B:7C:32:41',
   'extra.sha512_fingerprint' : '88:7B:16:DB:39:44:0C:47:0E:4A:8F:0B:C5:FB:4D:45:BC:93:5A:00:43:A1:D9:7F:05:1D:86:33:02:F8:FC:57:67:A6:1D:C0:FF:F7:D2:40:D8:9A:21:AE:4E:6D:DC:E7:FF:72:BF:13:CB:EE:A7:5F:CD:83:EA:8A:5E:FB:87:DD',
   'extra.signature_algorithm' : 'sha1WithRSAEncryption',
   'extra.source.naics' : 517311,
   'extra.ssl_poodle' : False,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : 'FGT60D4614030700',
   'extra.subject_country' : 'US',
   'extra.subject_email_address' : 'support@fortinet.com',
   'extra.subject_locality_name' : 'Sunnyvale',
   'extra.subject_organization_name' : 'Fortinet',
   'extra.subject_organization_unit_name' : 'FortiGate',
   'extra.subject_state_or_province_name' : 'California',
   'extra.tag' : 'ssl,vpn',
   'feed.name' : 'Accessible SSL',
   'protocol.application': 'https',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
   'source.asn' : 4181,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'MILWAUKEE',
   'source.geolocation.region' : 'WISCONSIN',
   'source.ip' : '96.60.0.0',
   'source.port' : 10443,
   'source.reverse_dns' : '96-60-0-0.example.com',
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_error' : 'x509: unknown error',
   'extra.browser_trusted' : False,
   'extra.cert_expiration_date' : '2023-02-06 01:01:34',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2022-01-04 01:01:34',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '36974C4C6B1B3785',
   'extra.cert_valid' : False,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
   'extra.content_type' : 'text/html; charset=UTF-8',
   'extra.freak_vulnerable' : False,
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_connection' : 'keep-alive',
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : '1078-btb-tbi-HungHa-61d39c6d5a7e2',
   'extra.issuer_organization_name' : 'pfSense webConfigurator Self-Signed Certificate',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : '16:93:9A:F4:35:7F:9A:85:45:71:91:C7:7C:80:88:00',
   'extra.self_signed' : True,
   'extra.server_type' : 'nginx',
   'extra.set_cookie' : 'PHPSESSID=e15bdfa5739c36877608eb4cf46cc388; path=/; secure; HttpO',
   'extra.sha1_fingerprint' : 'A9:00:BB:E1:54:4D:56:54:59:F1:B7:EA:F1:1A:D5:36:5C:63:90:8E',
   'extra.sha256_fingerprint' : '38:85:F0:44:1E:AD:84:B8:2F:43:68:BA:AC:EE:17:13:A4:BF:86:1D:48:75:7E:22:FA:08:4C:28:5F:AC:3E:5F',
   'extra.sha512_fingerprint' : 'AE:1B:4F:D1:E4:C0:35:9D:2A:4F:7A:37:B8:7B:11:9D:84:25:23:21:AB:EF:B2:0F:DC:C9:F2:A3:72:28:92:E1:74:72:FA:E1:09:6C:E1:F6:B6:E3:A7:61:1C:58:89:34:D7:06:5C:3D:0A:A7:F6:CC:8A:D6:24:D0:04:4C:03:02',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 517311,
   'extra.ssl_poodle' : False,
   'extra.ssl_version' : 2,
   'extra.subject_common_name' : '1078-btb-tbi-HungHa-61d39c6d5a7e2',
   'extra.subject_organization_name' : 'pfSense webConfigurator Self-Signed Certificate',
   'extra.tag' : 'ssl',
   'extra.transfer_encoding' : 'chunked',
   'feed.name' : 'Accessible SSL',
   'protocol.application': 'https',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
   'source.asn' : 45899,
   'source.geolocation.cc' : 'VN',
   'source.geolocation.city' : 'THAI BINH',
   'source.geolocation.region' : 'THAI BINH',
   'source.ip' : '113.160.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'open-ssl',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.browser_trusted' : True,
   'extra.cert_expiration_date' : '2022-11-06 15:30:28',
   'extra.cert_expired' : False,
   'extra.cert_issue_date' : '2021-10-07 15:30:28',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : '7B388364A24B88E77E5553B5C6748100',
   'extra.cert_valid' : True,
   'extra.cipher_suite' : 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
   'extra.content_length' : 131,
   'extra.content_type' : 'text/html',
   'extra.freak_vulnerable' : False,
   'extra.handshake' : 'TLSv1.2',
   'extra.http_code' : 200,
   'extra.http_date' : '2022-01-10T00:01:44+00:00',
   'extra.http_reason' : 'OK',
   'extra.http_response_type' : 'HTTP/1.1',
   'extra.issuer_common_name' : 'Entrust Certification Authority - L1K',
   'extra.issuer_country' : 'US',
   'extra.issuer_organization_name' : 'Entrust, Inc.',
   'extra.issuer_organization_unit_name' : '(c) 2012 Entrust, Inc. - for authorized use only',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'E7:34:BC:92:84:FA:39:DE:E1:46:6C:27:DA:5A:01:F4',
   'extra.self_signed' : False,
   'extra.server_type' : 'xxxxxxxx-xxxxx',
   'extra.sha1_fingerprint' : 'AD:19:B2:1C:CB:88:70:9B:DB:8E:7E:F5:65:50:13:D6:43:6C:BE:6E',
   'extra.sha256_fingerprint' : '9A:64:73:0B:8A:FA:DE:22:D4:6D:5A:C6:C4:6F:D4:A4:2A:28:FA:41:1E:FF:81:DC:D4:D9:00:FD:78:DF:C4:DD',
   'extra.sha512_fingerprint' : '9A:B7:BD:68:7D:F3:E7:C1:B7:D3:F4:2F:01:B6:C4:77:90:A3:2B:1E:C0:89:F5:08:EC:43:87:35:60:36:D4:87:61:AA:B8:A8:B3:8A:E9:F1:04:AA:5B:67:12:FF:63:D5:14:80:77:6E:8F:7D:C3:E2:3A:F3:13:DF:08:43:6C:B0',
   'extra.signature_algorithm' : 'sha256WithRSAEncryption',
   'extra.source.naics' : 454110,
   'extra.source.sector' : 'Retail Trade',
   'extra.ssl_poodle' : False,
   'extra.ssl_version' : 2,
   'extra.subject_country' : 'US',
   'extra.subject_locality_name' : 'Hanover',
   'extra.subject_organization_name' : 'Ciena Corporation',
   'extra.subject_state_or_province_name' : 'Maryland',
   'extra.tag' : 'ssl,vpn',
   'extra.validation_level' : 'OV',
   'feed.name' : 'Accessible SSL',
   'protocol.application': 'https',
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
   'source.asn' : 14618,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'ASHBURN',
   'source.geolocation.region' : 'VIRGINIA',
   'source.ip' : '34.224.0.0',
   'source.port' : 10443,
   'time.observation' : '2022-01-07T00:00:00+00:00',
   'time.source' : '2022-01-10T00:01:42+00:00'
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
