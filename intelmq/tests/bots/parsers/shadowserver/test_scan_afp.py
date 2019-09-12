# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_afp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible AFP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-07-30T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_afp-test-test.csv",

                  }
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'Accessible AFP',
    "classification.identifier": "accessible-afp",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.afp_versions": "AFP3.3,AFP3.2,AFP3.1",
    "extra.flags": "SupportsCopyFile,SupportsChgPwd,SupportsServerMessages,SupportsServerSignature,SupportsTCP/IP,SupportsSrvrNotifications,SupportsReconnect,SupportsOpenDirectory,SupportsUTF8Servername,SupportsUUIDs,SupportsSuperClient",
    "extra.machine_type": "TimeCapsule8,119",
    "extra.naics": 517311,
    "extra.network_address": "198.33.24.165:548,10.0.1.1:548,fe80:0008:0000:0000:6e70:9fff:fed4::548,fe80:0009:0000:0000:6e70:9fff:fed4::548,179.24.24.165 (DNS address),",
    "extra.server_name": "airport-time-capsule-de-jack",
    "extra.signature": "4338364e37364442463948350069672d",
    "extra.tag": "afp",
    "extra.uams": "DHCAST128,DHX2,SRP,Recon1",
    "extra.utf8_servername": "AirPort Time Capsule de jack",
    "protocol.application": "afp",
    "protocol.transport": "tcp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
     "source.asn": 6057,
    "source.geolocation.cc": "AA",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.13.34.22",
    "source.port": 548,
    "source.reverse_dns": "host.local",
    "time.observation": "2018-07-30T00:00:00+00:00",
    "time.source": "2019-09-04T05:05:53+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Accessible AFP',
    "classification.identifier": "accessible-afp",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.afp_versions": "AFP3.3,AFP3.2,AFP3.1",
    "extra.flags": "SupportsCopyFile,SupportsChgPwd,SupportsServerMessages,SupportsServerSignature,SupportsTCP/IP,SupportsSrvrNotifications,SupportsReconnect,SupportsOpenDirectory,SupportsUTF8Servername,SupportsUUIDs,SupportsSuperClient",
    "extra.machine_type": "TimeCapsule8,119",
    "extra.naics": 517311,
    "extra.network_address": "0.0.0.1:548,10.0.1.1:548,198.33.42.1:548,fe80:000b:0000:0000:dea4:caff:feba::548,fe80:000c:0000:0000:dea4:caff:feba::548,fe80:000d:0000:0000:4c7d:ffff:fec7::548,0.0.0.1 (DNS address),",
    "extra.server_name": "time-capsule-del-jack",
    "extra.signature": "433836544b303147463948360069672d",
    "extra.tag": "afp",
    "extra.uams": "DHCAST128,DHX2,SRP,Recon1",
    "extra.utf8_servername": "Time Capsule del Jack",
    "protocol.application": "afp",
    "protocol.transport": "tcp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
    "source.asn": 6057,
    "source.geolocation.cc": "AA",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.40.27.212",
    "source.port": 548,
    "source.reverse_dns": "host.local",
    "time.observation": "2018-07-30T00:00:00+00:00",
    "time.source": "2019-09-04T05:05:56+00:00"
    },]


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
