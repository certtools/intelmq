# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.nothink.parser_dns_attacks import NothinkDNSAttackParserBot

with open(os.path.join(os.path.dirname(__file__), 'honeypot_dns_attacks.txt'), encoding='utf-8') as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
                  'feed.name': 'DNS Attacks',
                  '__type': 'Report',
                  'raw': utils.base64_encode(EXAMPLE_FILE),
                  'time.observation': '2016-11-22T08:26:00+00:00'
                  }

EXAMPLE_EVENTS = [{'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
                   'feed.name': 'DNS Attacks',
                   '__type': 'Event',
                   'raw': 'MjAxNi0xMS0xMSAxNToxMzoyMCwxODYuMi4xNjcuMTQsMjYyMjU0LERBTkNPTSBMVEQsLCwgQlosZGRvcy1ndWFyZC5uZXQsQlo=',
                   'time.source': '2016-11-11T15:13:20+00:00',
                   'source.ip': '186.2.167.14',
                   'source.asn': 262254,
                   'source.as_name': 'DANCOM LTD,,, BZ',
                   'source.reverse_dns': 'ddos-guard.net',
                   'source.geolocation.cc': 'BZ',
                   'classification.type': 'ddos',
                   'event_description.text': 'On time.source the source.ip was seen performing '
                                             'DNS amplification attacks against honeypots',
                   'protocol.application': 'dns'
                   },
                  {'feed.url': 'http://www.nothink.org/honeypot_dns_attacks.txt',
                   'feed.name': 'DNS Attacks',
                   '__type': 'Event',
                   'raw': 'MjAxNi0wMS0yNCAxNjoyMToxOCwxMzEuMjIxLjQ3LjIxMCwyNjQ0MDksWWF4IFRlY25vbG9naWEgZSBJbmZvcm1hw4PCpy4uLixuL2EsVU5L',
                   'time.source': '2016-01-24T16:21:18+00:00',
                   'source.ip': '131.221.47.210',
                   'source.asn': 264409,
                   'source.as_name': 'Yax Tecnologia e InformaÃ§...',
                   'classification.type': 'ddos',
                   'event_description.text': 'On time.source the source.ip was seen performing '
                                             'DNS amplification attacks against honeypots',
                   'protocol.application': 'dns'
                   },
                  ]


class TestNothinkDNSAttackParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for NothinkDNSAttackParserBot """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = NothinkDNSAttackParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENTS[0])
        self.assertMessageEqual(1, EXAMPLE_EVENTS[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
