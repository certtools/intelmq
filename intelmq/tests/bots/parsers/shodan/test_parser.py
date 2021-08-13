# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
           'extra.shodan.unique_keys': ['ftp'],
           'feed.name': 'Test feed',
           'protocol.application': 'ftp',
           },{
           '__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org',
           'extra.http.host': '203.0.113.58',
           'extra.http.location': '/',
           'extra.isp': 'Example ISP',
           'extra.shodan.unique_keys': ['http'],
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
           'extra.shodan.unique_keys': ['isakmp'],
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
           },
           {'__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org',
           'extra.coap.resources': ['/api', '/.well-known/core', '/api/v1'],
           'extra.data': 'CoAP Resources:\n  /.well-known/core\n  /api\n  /api/v1\n',
           'extra.isp': 'Example Org',
           'extra.raw': '6045b00ac128b102ff3c2f6170693e2c3c2f6170692f76313e2c3c2f2e77656c6c2d6b6e6f776e2f636f72653e',
           'extra.shodan.event_hash': 1160109285,
           'extra.shodan.unique_keys': ['coap'],
           'feed.name': 'Test feed',
           'protocol.application': 'coap',
           'protocol.transport': 'udp',
           'source.asn': 64509,
           'source.geolocation.cc': 'EE',
           'source.geolocation.latitude': 59.0,
           'source.geolocation.longitude': 26.0,
           'source.ip': '228.162.114.217',
           'source.port': 5683,
           'time.source': '2021-01-07T12:48:18.645363+00:00',
           'raw': RAWS[3]},
           {'__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org',
           'extra.data': 'LDAP:\n'
                         '  SupportedLDAPVersion: 3\n'
                         '  SupportedControl: 1.3.6.1.4.1.6666.5327.2\n'
                         '  HighestCommittedUSN: 0\n'
                         '  NamingContexts: cn=pbx0\n'
                         '  LdapServiceName: IP800-06-26-e6',
           'extra.isp': 'Example Org',
           'extra.ldap.ldapservicename': 'IP800-06-26-e6',
           'extra.ldap.namingcontexts': 'cn=pbx0',
           'extra.ldap.supportedcontrol': ['1.3.6.1.4.1.6666.5327.2'],
           'extra.ldap.supportedldapversion': ['3'],
           'extra.raw': '308201bb020102648201b40400308201ae301b0414737570706f727465644c44415056657273696f6e3103040133302c0410737570706f72746564436f6e74726f6c31180416312e322e3834302e3131333535362e312e342e333139302d0410737570706f72746564436f6e74726f6c31190417322e31362e3834302e312e3131333733302e332e342e39302c0410737570706f72746564436f6e74726f6c31180416312e322e3834302e3131333535362e312e342e343733302c0410737570706f72746564436f6e74726f6c31180416312e322e3834302e3131333535362e312e342e343137302c0410737570706f72746564436f6e74726f6c31180416312e322e3834302e3131333535362e312e342e353238302d0410737570706f72746564436f6e74726f6c31190417312e332e362e312e342e312e363636362e353332372e32301a041368696768657374436f6d6d697474656455534e3103040130301b040e6e616d696e67436f6e746578747331090407636e3d4b444230301b040e6e616d696e67436f6e746578747331090407636e3d706278303023040f6c646170536572766963654e616d653110040e49503830302d30362d32362d6536',
           'extra.shodan.event_hash': 2041456559,
           'extra.shodan.unique_keys': [],
           'feed.name': 'Test feed',
           'protocol.transport': 'tcp',
           'source.asn': 64509,
           'source.geolocation.cc': 'EE',
           'source.geolocation.latitude': 59.0,
           'source.geolocation.longitude': 26.0,
           'source.ip': '228.162.114.217',
           'source.port': 636,
           'time.source': '2021-01-26T19:20:47.941808+00:00',
           'raw': RAWS[4]
           },
           {'__type': 'Event',
           'classification.identifier': 'shodan-scan',
           'classification.type': 'other',
           'event_description.target': 'Example Org',
           'extra.data': 'LDAP:\n'
                         '  SupportedControl:\n'
                         '    1.2.826.0.1.3344810.2.3\n'
                         '    1.2.840.113556.1.4.1339\n'
                         '    1.2.840.113556.1.4.1340\n'
                         '    1.2.840.113556.1.4.1413\n'
                         '    1.2.840.113556.1.4.319\n'
                         '    1.2.840.113556.1.4.805\n'
                         '    1.3.6.1.1.12\n'
                         '    1.3.6.1.1.13.1\n'
                         '    1.3.6.1.1.13.2\n'
                         '    1.3.6.1.4.1.21008.108.63.1\n'
                         '    1.3.6.1.4.1.4203.1.10.1\n'
                         '    1.3.6.1.4.1.4203.1.9.1.1\n'
                         '    1.3.6.1.4.1.4203.666.5.12\n'
                         '    1.3.6.1.4.1.4203.666.5.15\n'
                         '    1.3.6.1.4.1.4203.666.5.18\n'
                         '    1.3.6.1.4.1.4203.666.5.2\n'
                         '    2.16.840.1.113730.3.4.18\n'
                         '    2.16.840.1.113730.3.4.2\n'
                         '  SupportedExtension:\n'
                         '    1.3.6.1.1.8\n'
                         '    1.3.6.1.4.1.1466.20037\n'
                         '    1.3.6.1.4.1.4203.1.11.1\n'
                         '    1.3.6.1.4.1.4203.1.11.3\n'
                         '  SupportedLDAPVersion: 3\n'
                         '  SupportedSASLMechanisms:\n'
                         '    CRAM-MD5\n'
                         '    DIGEST-MD5\n'
                         '    GSSAPI\n'
                         '    OTP\n'
                         '    SCRAM-SHA-1\n'
                         '  SubschemaSubentry: cn=Subschema',
           'extra.isp': 'Example Org',
           'extra.ldap.subschemasubentry': 'cn=Subschema',
           'extra.ldap.supportedcontrol': ['1.2.826.0.1.3344810.2.3',
                                           '1.2.840.113556.1.4.1339',
                                           '1.2.840.113556.1.4.1340',
                                           '1.2.840.113556.1.4.1413',
                                           '1.2.840.113556.1.4.319',
                                           '1.2.840.113556.1.4.805',
                                           '1.3.6.1.1.12',
                                           '1.3.6.1.1.13.1',
                                           '1.3.6.1.1.13.2',
                                           '1.3.6.1.4.1.21008.108.63.1',
                                           '1.3.6.1.4.1.4203.1.10.1',
                                           '1.3.6.1.4.1.4203.1.9.1.1',
                                           '1.3.6.1.4.1.4203.666.5.12',
                                           '1.3.6.1.4.1.4203.666.5.15',
                                           '1.3.6.1.4.1.4203.666.5.18',
                                           '1.3.6.1.4.1.4203.666.5.2',
                                           '2.16.840.1.113730.3.4.18',
                                           '2.16.840.1.113730.3.4.2'],
           'extra.ldap.supportedextension': ['1.3.6.1.1.8',
                                             '1.3.6.1.4.1.1466.20037',
                                             '1.3.6.1.4.1.4203.1.11.1',
                                             '1.3.6.1.4.1.4203.1.11.3'],
           'extra.ldap.supportedldapversion': ['3'],
           'extra.ldap.supportedsaslmechanisms': ['CRAM-MD5',
                                                  'DIGEST-MD5',
                                                  'GSSAPI',
                                                  'OTP',
                                                  'SCRAM-SHA-1'],
           'extra.raw': '308202ea020102648202e30400308202dd3014040e6e616d696e67436f6e746578747331020400308201c50410737570706f72746564436f6e74726f6c318201af0419312e332e362e312e342e312e343230332e3636362e352e31380418312e332e362e312e342e312e343230332e312e392e312e31041a312e332e362e312e342e312e32313030382e3130382e36332e310418322e31362e3834302e312e3131333733302e332e342e31380417322e31362e3834302e312e3131333733302e332e342e320419312e332e362e312e342e312e343230332e3636362e352e31320418312e332e362e312e342e312e343230332e3636362e352e320417312e332e362e312e342e312e343230332e312e31302e310417312e322e3834302e3131333535362e312e342e313334300416312e322e3834302e3131333535362e312e342e3830350417312e322e3834302e3131333535362e312e342e313431330419312e332e362e312e342e312e343230332e3636362e352e31350417312e322e3834302e3131333535362e312e342e313333390416312e322e3834302e3131333535362e312e342e3331390417312e322e3832362e302e312e333334343831302e322e33040e312e332e362e312e312e31332e32040e312e332e362e312e312e31332e31040c312e332e362e312e312e3132306d0412737570706f72746564457874656e73696f6e31570416312e332e362e312e342e312e313436362e32303033370417312e332e362e312e342e312e343230332e312e31312e310417312e332e362e312e342e312e343230332e312e31312e33040b312e332e362e312e312e38301b0414737570706f727465644c44415056657273696f6e3103040133304b0417737570706f727465645341534c4d656368616e69736d733130040b534352414d2d5348412d310406475353415049040a4449474553542d4d443504034f545004084352414d2d4d443530230411737562736368656d61537562656e747279310e040c636e3d537562736368656d61300c02010265070a010004000400',
           'extra.shodan.event_hash': -991944684,
           'extra.shodan.unique_keys': [],
           'feed.name': 'Test feed',
           'protocol.transport': 'tcp',
           'source.asn': 64509,
           'source.geolocation.cc': 'EE',
           'source.geolocation.latitude': 59.0,
           'source.geolocation.longitude': 26.0,
           'source.ip': '228.162.114.217',
           'source.port': 389,
           'time.source': '2021-01-22T07:55:42.888074+00:00',
           'raw': RAWS[5]
           },
          ]
MINIMAL = [{'__type': 'Event',
            'classification.type': 'other',
            'classification.identifier': 'network-scan',
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
            'classification.identifier': 'network-scan',
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
            'classification.identifier': 'network-scan',
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


def _test(self, indexes):
    for i in indexes:
        self.input_message = REPORTS[i]
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[i])

class TestShodanParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShodanParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShodanParserBot
        cls.default_input_message = REPORTS[0]

    def test_ftp(self):
        _test(self, [0])

    def test_http(self):
        _test(self, [1])

    def test_ike(self):
        _test(self, [2])

    def test_keys_conversion(self):
        _test(self, [3])

    def test_maybe_single_to_list(self):
        # first has a single string for opts.ldap.supportedControl, second has a list of strings
        _test(self, [4, 5])


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
