# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.nothink.parser import NothinkParserBot

with open(os.path.join(os.path.dirname(__file__), 'blacklist_snmp_day.txt')) as handle:
    SNMP_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'blacklist_ssh_day.txt')) as handle:
    SSH_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'blacklist_telnet_day.txt')) as handle:
    TELNET_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'honeypot_dns_attacks.txt')) as handle:
    DNS_ATTACK_FILE = handle.read()

SNMP_REPORT = {'feed.name': 'SNMP Blacklist',
               'feed.url': 'http://www.nothink.org/blacklist/blacklist_snmp_day.txt',
               '__type': 'Report',
               'time.observation': '2016-12-05T09:23:46+00:00',
               'raw': utils.base64_encode(SNMP_FILE)
               }
SNMP_EVENT = {'feed.name': 'SNMP Blacklist',
              'feed.url': 'http://www.nothink.org/blacklist/blacklist_snmp_day.txt',
              '__type': 'Event',
              'time.observation': '2016-12-05T09:23:46+00:00',
              'raw': 'MTg1LjEyOC40MC4xNjI=',
              'time.source': '2016-11-14T23:02:04+00:00',
              'source.ip': '185.128.40.162',
              'classification.type': 'scanner',
              'protocol.application': 'snmp',
              }

SSH_REPORT = {'feed.name': 'SSH Blacklist',
              'feed.url': 'http://www.nothink.org/blacklist/blacklist_ssh_day.txt',
              '__type': 'Report',
              'time.observation': '2016-12-05T09:23:46+00:00',
              'raw': utils.base64_encode(SSH_FILE)
              }
SSH_EVENT = {'feed.name': 'SSH Blacklist',
             'feed.url': 'http://www.nothink.org/blacklist/blacklist_ssh_day.txt',
             '__type': 'Event',
             'time.observation': '2016-12-05T09:23:46+00:00',
             'raw': 'MTg1LjEyOC40MC4xNjI=',
             'time.source': '2016-11-14T23:02:04+00:00',
             'source.ip': '185.128.40.162',
             'classification.type': 'scanner',
             'protocol.application': 'ssh',
             }

TELNET_REPORT = {'feed.name': 'Telnet Blacklist',
                 'feed.url': 'http://www.nothink.org/blacklist/blacklist_telnet_day.txt',
                 '__type': 'Report',
                 'time.observation': '2016-12-05T09:23:46+00:00',
                 'raw': utils.base64_encode(TELNET_FILE)
                 }
TELNET_EVENT = {'feed.name': 'Telnet Blacklist',
                'feed.url': 'http://www.nothink.org/blacklist/blacklist_telnet_day.txt',
                '__type': 'Event',
                'time.observation': '2016-12-05T09:23:46+00:00',
                'raw': 'MTg1LjEyOC40MC4xNjI=',
                'time.source': '2016-11-14T23:02:04+00:00',
                'source.ip': '185.128.40.162',
                'classification.type': 'scanner',
                'protocol.application': 'telnet',
                }

DNS_REPORT = {'feed.name': 'DNS Attack',
              'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
              '__type': 'Report',
              'time.observation': '2016-12-05T09:23:46+00:00',
              'raw': utils.base64_encode(DNS_ATTACK_FILE)
              }
DNS_EVENT = [{'feed.name': 'DNS Attack',
              'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
              '__type': 'Event',
              'time.observation': '2016-12-05T09:23:46+00:00',
              'raw': 'IjIwMTYtMTEtMTEgMTU6MTM6MjAiLCIxODYuMi4xNjcuMTQiLCIyNjIyNTQiLCJEQU5DT00gTFRELCwsIEJaIiwiZGRvcy1ndWFyZC5uZXQiLCJCWiI=',
              'time.source': '2016-11-11T15:13:20+00:00',
              'source.ip': '186.2.167.14',
              'source.asn': 262254,
              'source.as_name': 'DANCOM LTD,,, BZ',
              'source.reverse_dns': 'ddos-guard.net',
              'source.geolocation.cc': 'BZ',
              'protocol.application': 'dns',
              'classification.type': 'ddos',
              'event_description.text': 'On time.source the source.ip was seen performing '
                                        'DNS amplification attacks against honeypots',
              },
             {'feed.name': 'DNS Attack',
              'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
              '__type': 'Event',
              'time.observation': '2016-12-05T09:23:46+00:00',
              'raw': 'IjIwMTYtMDEtMjQgMTY6MjE6MTgiLCIxMzEuMjIxLjQ3LjIxMCIsIjI2NDQwOSIsIllheCBUZWNub2xvZ2lhIGUgSW5mb3JtYcODwqcuLi4iLCJuL2EiLCJVTksi',
              'time.source': '2016-01-24T16:21:18+00:00',
              'source.ip': '131.221.47.210',
              'source.asn': 264409,
              'source.as_name': 'Yax Tecnologia e InformaÃ§...',
              'protocol.application': 'dns',
              'classification.type': 'ddos',
              'event_description.text': 'On time.source the source.ip was seen performing '
                                        'DNS amplification attacks against honeypots',
              }]


class TestNothinkParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase of Nothink Feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = NothinkParserBot
        cls.default_input_message = SNMP_REPORT

    def test_snmp(self):
        """ Test if correct SNMP event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, SNMP_EVENT)

    def test_ssh(self):
        """ Test if correct SSH event has been produced. """
        self.input_message = SSH_REPORT
        self.run_bot()
        self.assertMessageEqual(0, SSH_EVENT)

    def test_telnet(self):
        """ Test if correct TELNET event has been produced. """
        self.input_message = TELNET_REPORT
        self.run_bot()
        self.assertMessageEqual(0, TELNET_EVENT)

    def test_dns(self):
        """ Test if correct DNS event has been produced. """
        self.input_message = DNS_REPORT
        self.run_bot()
        self.assertMessageEqual(0, DNS_EVENT[0])
        self.assertMessageEqual(1, DNS_EVENT[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
