# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_rdp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible RDP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_rdp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible RDP',
           "classification.identifier": "open-rdp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.bluekeep_vulnerable": False,
           "extra.cert_expiration_date": "2019-10-29 02:22:06",
           "extra.cert_issue_date": "2019-04-29 02:22:06",
           "extra.cert_length": 5678,
           "extra.cert_serial_number": "1EF2B37AF850C9BF4E88F18177001D6B",
           "extra.cve20190708_vulnerable": False,
           "extra.issuer_common_name": "KABESRV.KABE.local",
           "extra.key_algorithm": "rsaEncryption",
           "extra.md5_fingerprint": "BC:6E:C3:E2:98:22:EC:BA:5B:30:E2:53:FD:4A:9D:FF",
           "extra.naics": 517311,
           "extra.rdp_protocol": "RDP",
           "extra.sha1_fingerprint": "EC:BB:4D:DB:9F:0C:D3:FF:5B:49:EA:B1:56:62:B6:A7:5D:60:54:42",
           "extra.sha256_fingerprint": "B7:C9:F4:07:D5:C0:75:1D:EA:0C:40:E7:26:39:C2:30:C6:13:83:7E:18:46:D8:E9:4C:45:3F:88:1B:0B:70:76",
           "extra.sha512_fingerprint": "08:AC:75:FA:EB:A3:2B:44:15:DE:6D:A7:0B:C0:AE:17:94:F3:55:D9:EC:70:AC:5B:B7:94:79:F0:D7:84:83:89:CB:A9:11:E0:08:D7:54:4D:33:85:89:D2:A8:DD:9D:15:F4:CC:95:DE:6A:E3:DF:6B:FA:8B:27:E3:DA:16:AF:0A",
           "extra.signature_algorithm": "sha256WithRSAEncryption",
           "extra.ssl_version": 2,
           "extra.subject_common_name": "KABESRV.KABE.local",
           "extra.tag": "rdp",
           "protocol.application": "rdp",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.178",
           "source.port": 5678,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T15:45:51+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Accessible RDP',
           "classification.identifier": "open-rdp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.bluekeep_vulnerable": False,
           "extra.cert_expiration_date": "2019-10-16 06:15:20",
           "extra.cert_issue_date": "2019-04-16 06:15:20",
           "extra.cert_length": 5678,
           "extra.cert_serial_number": "3FF3EBC5CF154BA54D128A8548C8AAF5",
           "extra.cve20190708_vulnerable": False,
           "extra.issuer_common_name": "RAMBLA01.rambla.local",
           "extra.key_algorithm": "rsaEncryption",
           "extra.md5_fingerprint": "38:73:6A:B3:AA:41:69:C9:BA:E7:3D:D7:40:16:F8:AA",
           "extra.naics": 517311,
           "extra.rdp_protocol": "RDP",
           "extra.sector": "Information Technology",
           "extra.sha1_fingerprint": "7A:67:1F:F8:87:C6:B0:AC:A9:84:15:B7:40:EC:CB:19:AA:E3:19:52",
           "extra.sha256_fingerprint": "8F:CD:7D:C4:80:2D:8D:9B:06:A0:40:18:9F:ED:73:7A:BA:83:55:BE:1B:56:83:A2:97:DF:BB:B4:06:57:CB:F1",
           "extra.sha512_fingerprint": "E8:9B:9A:93:69:B4:58:01:D8:46:C2:DC:01:20:1E:DD:93:E1:EB:E3:9D:6B:65:A0:C5:00:6C:A4:44:08:FE:A4:A6:19:FF:55:79:F2:AA:61:68:C8:1C:B0:CE:78:EB:84:DD:29:9D:64:2F:4E:25:31:3A:6C:B8:02:C9:AF:F5:1F",
           "extra.signature_algorithm": "sha1WithRSAEncryption",
           "extra.ssl_version": 2,
           "extra.subject_common_name": "RAMBLA01.rambla.local",
           "extra.tag": "rdp",
           "protocol.application": "rdp",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.233",
           "source.port": 5678,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T15:45:51+00:00"
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
