# -*- coding: utf-8 -*-
import base64
import json
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.shodan.parser import ShodanParserBot

with open(os.path.join(os.path.dirname(__file__), 'tests.json'), 'rt') as fh:
    RAWS_UNENCODED = fh.read().splitlines()
    RAWS = [base64.b64encode(x.encode()).decode() for x in RAWS_UNENCODED]

REPORTS = [{"feed.name": "Test feed",
                    "raw": raw,
                    "__type": "Report",
                    } for raw in RAWS]
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org 1',
           'extra.data': '220-FileZilla Server version 0.9.41 beta\n'
                         '220-written by Tim Kosse (Tim.Kosse@gmx.de)\n'
                         '220 Please visit http://sourceforge.net/projects/filezilla/\r\n'
                         '530 Login or password incorrect!\r\n'
                         '214-The following commands are recognized:\n'
                         '   USER   PASS   QUIT   CWD    PWD    PORT   PASV   TYPE\n'
                         '   LIST   REST   CDUP   RETR   STOR   SIZE   DELE   RMD \n'
                         '   MKD    RNFR   RNTO   ABOR   SYST   NOOP   APPE   NLST\n'
                         '   MDTM   XPWD   XCUP   XMKD   XRMD   NOP    EPSV   EPRT\n'
                         '   AUTH   ADAT   PBSZ   PROT   FEAT   MODE   OPTS   HELP\n'
                         '   ALLO   MLST   MLSD   SITE   P@SW   STRU   CLNT   MFMT\n'
                         '   HASH\n'
                         '214 Have a nice day.\r\n'
                         '211-Features:\n'
                         ' MDTM\n'
                         ' REST STREAM\n'
                         ' SIZE\n'
                         ' MLST type*;size*;modify*;\n'
                         ' MLSD\n'
                         ' UTF8\n'
                         ' CLNT\n'
                         ' MFMT\n'
                         '211 End',
           'extra.ftp.features.mlst': ['type', 'size', 'modify'],
           'extra.ftp.rest.parameters': ['STREAM'],
           'feed.name': 'Test feed',
           'protocol.transport': 'tcp',
           'raw': RAWS[0],
           'source.asn': 64496,
           'source.fqdn': "example.at",
           'source.geolocation.cc': 'AT',
           'source.ip': '240.15.82.82',
           'source.port': 21,
           'source.reverse_dns': "mail.example.at",
           'time.source': '2018-06-19T13:02:37.371273+00:00',
           'source.geolocation.longitude': 16.0,
           'source.geolocation.latitude': 48.0,
           'extra.isp': 'Example ISP',
           'extra.shodan.event_hash': 2125142980,
           'feed.name': 'Test feed',
           'protocol.application': 'ftp',
           },{
           '__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org',
           'extra.http.location': '/',
           'extra.isp': 'Example ISP',
           'feed.name': 'Test feed',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'source.asn': 64496,
           'source.geolocation.cc': 'DE',
           'source.geolocation.latitude': 51.0,
           'source.geolocation.longitude': 9.0,
           'source.ip': '203.0.113.58',
           'source.port': 8888,
           'time.source': '2018-06-19T14:14:15.931753+00:00',
           'raw': RAWS[1],
           },
          {'__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org 2',
           'extra.data': 'VPN (IKE)\n'
                         '\n'
                         'Initiator SPI: 8890defa029\n'
                         'Responder SPI: 4098340248029309d88007\n'
                         'Next Payload: Notification (N)\n'
                         'Version: 1.0\n'
                         'Exchange Type: Informational\n'
                         'Flags:\n'
                         '    Encryption:     False\n'
                         '    Commit:         False\n'
                         '    Authentication: False\n'
                         'Message ID: 00000000\n'
                         'Length: 40',
           'extra.isakmp.exchange_type': 5,
           'extra.isakmp.initiator_spi': '092384023480dab023340',
           'extra.isakmp.length': 40,
           'extra.isakmp.msg_id': '00000000',
           'extra.isakmp.next_payload': 11,
           'extra.isakmp.responder_spi': '4240808ab039409',
           'extra.isakmp.version': '1.0',
           'extra.isp': 'Example ISP 3',
           'extra.postal_code': '000-9999',
           'extra.raw': '20398452d0782095b8084c0294e80f294',
           'extra.region_code': '32',
           'extra.shodan.event_hash': -441119144,
           'extra.tags': ['vpn'],
           'feed.name': 'Test feed',
           'protocol.application': 'isakmp',
           'protocol.transport': 'udp',
           'source.asn': 64496,
           'source.fqdn': 'example.jp',
           'source.geolocation.cc': 'JP',
           'source.geolocation.city': 'Example City',
           'source.geolocation.latitude': 34.0,
           'source.geolocation.longitude': 135.0,
           'source.ip': '172.0.0.8',
           'source.port': 500,
           'source.reverse_dns': 'foobar.example.jp',
           'time.source': '2018-06-19T14:14:15.587093+00:00',
           'raw': RAWS[2],
           }
          ]
MINIMAL = [{'__type': 'Event',
            'classification.type': 'other',
            'event_description.target': 'Example Org 1',
            'extra.data': EVENTS[0]['extra.data'],
            'feed.name': 'Test feed',
            'protocol.transport': 'tcp',
            'source.asn': 64496,
            'source.geolocation.cc': 'AT',
            'source.ip': '240.15.82.82',
            'source.port': 21,
            'time.source': '2018-06-19T13:02:37.371273+00:00',
            'feed.name': 'Test feed',
            'extra.shodan': json.loads(RAWS_UNENCODED[0]),
            'raw': RAWS[0],
            },{
            '__type': 'Event',
            'classification.type': 'other',
            'event_description.target': 'Example Org',
            'feed.name': 'Test feed',
            'protocol.transport': 'tcp',
            'source.asn': 64496,
            'source.geolocation.cc': 'DE',
            'source.ip': '203.0.113.58',
            'source.port': 8888,
            'time.source': '2018-06-19T14:14:15.931753+00:00',
            'extra.shodan': json.loads(RAWS_UNENCODED[1]),
            'raw': RAWS[1],
            },
           {'__type': 'Event',
            'classification.type': 'other',
            'event_description.target': 'Example Org 2',
            'extra.tags': ['vpn'],
            'feed.name': 'Test feed',
            'protocol.transport': 'udp',
            'source.asn': 64496,
            'source.geolocation.cc': 'JP',
            'source.ip': '172.0.0.8',
            'source.port': 500,
            'time.source': '2018-06-19T14:14:15.587093+00:00',
            'extra.data': EVENTS[2]['extra.data'],
            'extra.shodan': json.loads(RAWS_UNENCODED[2]),
            'raw': RAWS[2],
            }
           ]


class TestShodanParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShodanParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShodanParserBot
        cls.default_input_message = REPORTS[0]

    def test_ftp(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])

    def test_http(self):
        self.input_message = REPORTS[1]
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[1])

    def test_ike(self):
        self.input_message = REPORTS[2]
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[2])


class TestShodanParserBot_minimal(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShodanParserBot with minimal_mode.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShodanParserBot
        cls.default_input_message = REPORTS[0]
        cls.sysconfig = {"minimal_mode": True}

    def test_minimal_ftp(self):
        self.run_bot()
        self.assertMessageEqual(0, MINIMAL[0])

    def test_minimal_http(self):
        self.input_message = REPORTS[1]
        self.run_bot()
        self.assertMessageEqual(0, MINIMAL[1])

    def test_minimal_ike(self):
        self.input_message = REPORTS[2]
        self.run_bot()
        self.assertMessageEqual(0, MINIMAL[2])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
