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
                       'testdata/scan_postgres.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible-PostgreSQL',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_postgres-test.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : 'open-postgres',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.cert_expiration_date' : '2021-11-12 11:18:27',
   'extra.cert_expired' : True,
   'extra.cert_issue_date' : '2012-11-14 11:18:27',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : 'B3F13DFBDBA2D8B2',
   'extra.cert_valid' : False,
   'extra.cipher_suite' : 'TLS_AES_256_GCM_SHA384',
   'extra.client_ssl' : False,
   'extra.issuer_common_name' : 'example.com',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'F1:8A:02:48:3C:6B:F4:00:CC:5C:D5:B0:71:E4:FA:00',
   'extra.protocol_error_code' : '0A000',
   'extra.protocol_error_file' : 'postmaster.c',
   'extra.protocol_error_line' : '1798',
   'extra.protocol_error_message' : 'unsupported frontend protocol 255.255: server supports 1.0 to 3.0',
   'extra.protocol_error_routine' : 'ProcessStartupPacket',
   'extra.protocol_error_severity' : 'FATAL',
   'extra.sha1_fingerprint' : '03:39:9E:5D:77:19:38:C4:49:DE:C3:3D:9B:E6:13:ED:5A:F1:42:55',
   'extra.sha256_fingerprint' : 'E1:D1:6E:87:49:B9:AC:74:B4:AC:9B:77:85:27:69:97:0D:16:B1:F6:63:F0:26:51:AA:89:42:39:66:BD:47:D0',
   'extra.sha512_fingerprint' : '1C:E9:04:22:90:46:68:0B:8B:54:33:38:C6:20:5F:EE:A6:73:A6:B5:2C:7D:12:94:DE:F1:CC:11:2E:72:0B:97:C2:7D:19:BF:E0:6B:98:A9:21:D9:9D:5A:CB:38:0B:D8:7E:E2:8E:2B:EA:15:EC:60:11:1E:41:E3:FB:4C:20:9F',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.startup_error_code' : '28000',
   'extra.startup_error_file' : 'postmaster.c',
   'extra.startup_error_line' : 1893,
   'extra.startup_error_message' : 'no PostgreSQL user name specified in startup packet',
   'extra.startup_error_routine' : 'ProcessStartupPacket',
   'extra.startup_error_severity' : 'FATAL',
   'extra.subject_common_name' : 'example.com',
   'extra.subject_country' : 'US',
   'extra.supported_protocols' : '1.0-3.0',
   'extra.tag' : 'postgres',
   'feed.name' : 'Accessible-PostgreSQL',
   'protocol.application' : 'postgres',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 5432,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-postgres',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.cert_expiration_date' : '2021-11-12 11:18:27',
   'extra.cert_expired' : True,
   'extra.cert_issue_date' : '2012-11-14 11:18:27',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : 'B3F13DFBDBA2D8B2',
   'extra.cert_valid' : False,
   'extra.cipher_suite' : 'TLS_AES_256_GCM_SHA384',
   'extra.client_ssl' : False,
   'extra.issuer_common_name' : 'example.com',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'F1:8A:02:48:3C:6B:F4:00:CC:5C:D5:B0:71:E4:FA:00',
   'extra.protocol_error_code' : '0A000',
   'extra.protocol_error_file' : 'postmaster.c',
   'extra.protocol_error_line' : '1798',
   'extra.protocol_error_message' : 'unsupported frontend protocol 255.255: server supports 1.0 to 3.0',
   'extra.protocol_error_routine' : 'ProcessStartupPacket',
   'extra.protocol_error_severity' : 'FATAL',
   'extra.sha1_fingerprint' : '03:39:9E:5D:77:19:38:C4:49:DE:C3:3D:9B:E6:13:ED:5A:F1:42:55',
   'extra.sha256_fingerprint' : 'E1:D1:6E:87:49:B9:AC:74:B4:AC:9B:77:85:27:69:97:0D:16:B1:F6:63:F0:26:51:AA:89:42:39:66:BD:47:D0',
   'extra.sha512_fingerprint' : '1C:E9:04:22:90:46:68:0B:8B:54:33:38:C6:20:5F:EE:A6:73:A6:B5:2C:7D:12:94:DE:F1:CC:11:2E:72:0B:97:C2:7D:19:BF:E0:6B:98:A9:21:D9:9D:5A:CB:38:0B:D8:7E:E2:8E:2B:EA:15:EC:60:11:1E:41:E3:FB:4C:20:9F',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.startup_error_code' : '28000',
   'extra.startup_error_file' : 'postmaster.c',
   'extra.startup_error_line' : 1893,
   'extra.startup_error_message' : 'no PostgreSQL user name specified in startup packet',
   'extra.startup_error_routine' : 'ProcessStartupPacket',
   'extra.startup_error_severity' : 'FATAL',
   'extra.subject_common_name' : 'example.com',
   'extra.subject_country' : 'US',
   'extra.supported_protocols' : '1.0-3.0',
   'extra.tag' : 'postgres',
   'feed.name' : 'Accessible-PostgreSQL',
   'protocol.application' : 'postgres',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 5432,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-postgres',
   'classification.taxonomy' : 'other',
   'classification.type' : 'other',
   'extra.cert_expiration_date' : '2021-11-12 11:18:27',
   'extra.cert_expired' : True,
   'extra.cert_issue_date' : '2012-11-14 11:18:27',
   'extra.cert_length' : 2048,
   'extra.cert_serial_number' : 'B3F13DFBDBA2D8B2',
   'extra.cert_valid' : False,
   'extra.cipher_suite' : 'TLS_AES_256_GCM_SHA384',
   'extra.client_ssl' : False,
   'extra.issuer_common_name' : 'example.com',
   'extra.key_algorithm' : 'rsaEncryption',
   'extra.md5_fingerprint' : 'F1:8A:02:48:3C:6B:F4:00:CC:5C:D5:B0:71:E4:FA:00',
   'extra.protocol_error_code' : '0A000',
   'extra.protocol_error_file' : 'postmaster.c',
   'extra.protocol_error_line' : '1798',
   'extra.protocol_error_message' : 'unsupported frontend protocol 255.255: server supports 1.0 to 3.0',
   'extra.protocol_error_routine' : 'ProcessStartupPacket',
   'extra.protocol_error_severity' : 'FATAL',
   'extra.sha1_fingerprint' : '03:39:9E:5D:77:19:38:C4:49:DE:C3:3D:9B:E6:13:ED:5A:F1:42:55',
   'extra.sha256_fingerprint' : 'E1:D1:6E:87:49:B9:AC:74:B4:AC:9B:77:85:27:69:97:0D:16:B1:F6:63:F0:26:51:AA:89:42:39:66:BD:47:D0',
   'extra.sha512_fingerprint' : '1C:E9:04:22:90:46:68:0B:8B:54:33:38:C6:20:5F:EE:A6:73:A6:B5:2C:7D:12:94:DE:F1:CC:11:2E:72:0B:97:C2:7D:19:BF:E0:6B:98:A9:21:D9:9D:5A:CB:38:0B:D8:7E:E2:8E:2B:EA:15:EC:60:11:1E:41:E3:FB:4C:20:9F',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.startup_error_code' : '28000',
   'extra.startup_error_file' : 'postmaster.c',
   'extra.startup_error_line' : 1893,
   'extra.startup_error_message' : 'no PostgreSQL user name specified in startup packet',
   'extra.startup_error_routine' : 'ProcessStartupPacket',
   'extra.startup_error_severity' : 'FATAL',
   'extra.subject_common_name' : 'example.com',
   'extra.subject_country' : 'US',
   'extra.supported_protocols' : '1.0-3.0',
   'extra.tag' : 'postgres',
   'feed.name' : 'Accessible-PostgreSQL',
   'protocol.application' : 'postgres',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 5432,
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:02+00:00'
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
