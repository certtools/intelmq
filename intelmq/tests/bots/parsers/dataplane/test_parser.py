# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.dataplane.parser import DataplaneParserBot

with open(os.path.join(os.path.dirname(__file__), 'sipinvitation.txt')) as handle:
    SIP_INVITE_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'sipquery.txt')) as handle:
    SIP_QUERY_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'sipregistration.txt')) as handle:
    SIP_REGISTER_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'sshclient.txt')) as handle:
    SSH_CLIENT_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'sshpwauth.txt')) as handle:
    SSH_AUTH_FILE = handle.read()

SIP_INVITE_REPORT = {'feed.url': 'http://dataplane.org/sipinvitation.txt',
                     'feed.name': 'SIP Invitation',
                     '__type': 'Report',
                     'raw': utils.base64_encode(SIP_INVITE_FILE),
                     'time.observation': '2016-12-07T06:27:26+00:00'
                     }

SIP_INVITE_EVENT = {'feed.url': 'http://dataplane.org/sipinvitation.txt',
                    'feed.name': 'SIP Invitation',
                    '__type': 'Event',
                    'time.observation': '2016-12-07T06:27:26+00:00',
                    'raw': 'ODU2MCAgICAgICAgIHwgIE9ORUFORE9ORS1BUyBCcmF1ZXJzdHJhc3NlIDQ4LCAgfCAgIDc0LjIwOC4xNDkuMjMxICB8ICAyMDE2LTEyLTA1IDE2OjA4OjI5ICB8ICBzaXBpbnZpdGF0aW9u',
                    'event_description.text': 'Address has been seen initiating a SIP INVITE operation to a remote host. '
                                              'The source report lists hosts that are suspicious of more than just port '
                                              'scanning. The host may be SIP client cataloging or conducting various forms '
                                              'of telephony abuse.',
                    'source.asn': 8560,
                    'source.ip': '74.208.149.231',
                    'source.as_name': 'ONEANDONE-AS',
                    'time.source': '2016-12-05T16:08:29+00:00',
                    'protocol.application': 'sip',
                    'classification.type': 'brute-force',
                    }

SIP_QUERY_REPORT = {'feed.url': 'http://dataplane.org/sipquery.txt',
                    'feed.name': 'SIP Query',
                    '__type': 'Report',
                    'raw': utils.base64_encode(SIP_QUERY_FILE),
                    'time.observation': '2016-12-07T06:27:26+00:00'
                    }

SIP_QUERY_EVENT = {'feed.url': 'http://dataplane.org/sipquery.txt',
                   'feed.name': 'SIP Query',
                   '__type': 'Event',
                   'time.observation': '2016-12-07T06:27:26+00:00',
                   'raw': 'MjA5ICAgICAgICAgIHwgIENFTlRVUllMSU5LLVVTLUxFR0FDWS1RV0VTVCAtICAgfCAgICAgIDY1LjE1Ny40Mi42ICB8ICAyMDE2LTEyLTA1IDE0OjAxOjIxICB8ICBzaXBxdWVyeQ==',
                   'event_description.text': 'Address has been seen initiating a SIP OPTIONS query to a remote host. '
                                             'The source report lists hosts that are suspicious of more than just port '
                                             'scanning. The host may be SIP server cataloging or conducting various forms '
                                             'of telephony abuse.',
                   'source.asn': 209,
                   'source.ip': '65.157.42.6',
                   'source.as_name': 'CENTURYLINK-US-LEGACY-QWEST',
                   'time.source': '2016-12-05T14:01:21+00:00',
                   'protocol.application': 'sip',
                   'classification.type': 'brute-force',
                   }

SIP_REGISTER_REPORT = {'feed.url': 'http://dataplane.org/sipregistration.txt',
                       'feed.name': 'SIP Registration',
                       '__type': 'Report',
                       'raw': utils.base64_encode(SIP_REGISTER_FILE),
                       'time.observation': '2016-12-07T06:27:26+00:00'
                       }

SIP_REGISTER_EVENT = {'feed.url': 'http://dataplane.org/sipregistration.txt',
                      'feed.name': 'SIP Registration',
                      '__type': 'Event',
                      'time.observation': '2016-12-07T06:27:26+00:00',
                      'raw': 'ODU2MCAgICAgICAgIHwgIE9ORUFORE9ORS1BUyBCcmF1ZXJzdHJhc3NlIDQ4LCAgfCAgIDc0LjIwOC4xNTIuMjA4ICB8ICAyMDE2LTEyLTA0IDIzOjE0OjAxICB8ICBzaXByZWdpc3RyYXRpb24=',
                      'event_description.text': 'Address has been seen initiating a SIP REGISTER operation to a remote host. '
                                                'The source report lists hosts that are suspicious of more than just port '
                                                'scanning. The host may be SIP client cataloging or conducting various forms '
                                                'of telephony abuse.',
                      'source.asn': 8560,
                      'source.ip': '74.208.152.208',
                      'source.as_name': 'ONEANDONE-AS',
                      'time.source': '2016-12-04T23:14:01+00:00',
                      'protocol.application': 'sip',
                      'classification.type': 'brute-force',
                      }

SSH_CLIENT_REPORT = {'feed.url': 'http://dataplane.org/sshclient.txt',
                     'feed.name': 'SSH Client',
                     '__type': 'Report',
                     'raw': utils.base64_encode(SSH_CLIENT_FILE),
                     'time.observation': '2016-12-07T06:27:26+00:00'
                     }

SSH_CLIENT_EVENT = [{'feed.url': 'http://dataplane.org/sshclient.txt',
                     'feed.name': 'SSH Client',
                     '__type': 'Event',
                     'time.observation': '2016-12-07T06:27:26+00:00',
                     'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgICAgICA1LjE1Ny43LjgyICB8ICAyMDE2LTEyLTAxIDIwOjQxOjA5ICB8ICBzc2hjbGllbnQ=',
                     'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                               'report lists hosts that are suspicious of more than just port scanning.  The host '
                                               'may be SSH server cataloging or conducting authentication attack attempts.',
                     'source.ip': '5.157.7.82',
                     'time.source': '2016-12-01T20:41:09+00:00',
                     'protocol.application': 'ssh',
                     'classification.type': 'scanner',
                     },
                    {'feed.url': 'http://dataplane.org/sshclient.txt',
                     'feed.name': 'SSH Client',
                     '__type': 'Event',
                     'time.observation': '2016-12-07T06:27:26+00:00',
                     'raw': 'Mzk0NDcyICAgICAgIHwgIFNXT0ktQVNOIC0gU1dPSSwgVVMgICAgICAgICAgICAgfCAgMTA0LjI0MS4yMzIuMjM4ICB8ICAyMDE2LTEyLTA1IDAxOjQ5OjE5ICB8ICBzc2hjbGllbnQ=',
                     'event_description.text': 'Address has been seen initiating an SSH connection to a remote host. The source '
                                               'report lists hosts that are suspicious of more than just port scanning.  The host '
                                               'may be SSH server cataloging or conducting authentication attack attempts.',
                     'source.asn': 394472,
                     'source.ip': '104.241.232.238',
                     'source.as_name': 'SWOI-ASN',
                     'time.source': '2016-12-05T01:49:19+00:00',
                     'protocol.application': 'ssh',
                     'classification.type': 'scanner',
                     }]

SSH_AUTH_REPORT = {'feed.url': 'http://dataplane.org/sshpwauth.txt',
                   'feed.name': 'SSH Password Authentication',
                   '__type': 'Report',
                   'raw': utils.base64_encode(SSH_AUTH_FILE),
                   'time.observation': '2016-12-07T06:27:26+00:00'
                   }

SSH_AUTH_EVENT = [{'feed.url': 'http://dataplane.org/sshpwauth.txt',
                   'feed.name': 'SSH Password Authentication',
                   '__type': 'Event',
                   'time.observation': '2016-12-07T06:27:26+00:00',
                   'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfCAgMTcwLjIzOS4xMDQuMTgzICB8ICAyMDE2LTEyLTAxIDA0OjI2OjQ4ICB8ICBzc2hwd2F1dGg=',
                   'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                             'authentication. The source report lists hosts that are highly suspicious and '
                                             'are likely conducting malicious SSH password authentication attacks.',
                   'source.ip': '170.239.104.183',
                   'time.source': '2016-12-01T04:26:48+00:00',
                   'protocol.application': 'ssh',
                   'classification.type': 'brute-force',
                   },
                  {'feed.url': 'http://dataplane.org/sshpwauth.txt',
                   'feed.name': 'SSH Password Authentication',
                   '__type': 'Event',
                   'time.observation': '2016-12-07T06:27:26+00:00',
                   'raw': 'NDEzNCAgICAgICAgIHwgIENISU5BTkVULUJBQ0tCT05FIE5vLjMxLEppbi1ybyAgfCAgIDExNy4yMS4yMjQuMTIxICB8ICAyMDE2LTEyLTA2IDAyOjM1OjM4ICB8ICBzc2hwd2F1dGg=',
                   'event_description.text': 'Address has been seen attempting to remotely login to a host using SSH password '
                                             'authentication. The source report lists hosts that are highly suspicious and '
                                             'are likely conducting malicious SSH password authentication attacks.',
                   'source.asn': 4134,
                   'source.ip': '117.21.224.121',
                   'source.as_name': 'CHINANET-BACKBONE',
                   'time.source': '2016-12-06T02:35:38+00:00',
                   'protocol.application': 'ssh',
                   'classification.type': 'brute-force',
                   }]


class TestDataplaneParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for the DataplaneParserBot """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DataplaneParserBot
        cls.default_input_message = SIP_INVITE_REPORT

    def test_sip_invite(self):
        self.run_bot()
        self.assertMessageEqual(0, SIP_INVITE_EVENT)

    def test_sip_query(self):
        self.input_message = SIP_QUERY_REPORT
        self.run_bot()
        self.assertMessageEqual(0, SIP_QUERY_EVENT)

    def test_sip_register(self):
        self.input_message = SIP_REGISTER_REPORT
        self.run_bot()
        self.assertMessageEqual(0, SIP_REGISTER_EVENT)

    def test_ssh_client(self):
        self.input_message = SSH_CLIENT_REPORT
        self.run_bot()
        self.assertMessageEqual(0, SSH_CLIENT_EVENT[0])
        self.assertMessageEqual(1, SSH_CLIENT_EVENT[1])

    def test_ssh_auth(self):
        self.input_message = SSH_AUTH_REPORT
        self.run_bot()
        self.assertMessageEqual(0, SSH_AUTH_EVENT[0])
        self.assertMessageEqual(1, SSH_AUTH_EVENT[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
