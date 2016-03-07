# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.dragonresearchgroup.parser_vnc import \
    DragonResearchGroupVNCParserBot


REPORT = {'__type': 'Report',
          'feed.url': 'https://dragonresearchgroup.org/insight/vncprobe.txt',
          'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgICAgNzguOTMuMjQ3Ljk0ICB8ICAyMDE1LTExLTA5IDIwOjE4OjE3'
                 'ICB8ICB2bmNwcm9iZQowMCAgICAgICAgICAgfCAgVGVzdC1BUyAgICAgICAg'
                 'ICAgICAgICAgICAgICAgICB8ICAgMTQyLjkxLjEwNC4xMDUgIHwgIDIwMTUt'
                 'MTEtMTAgMDI6MDQ6MzQgIHwgIHZuY3Byb2Jl',
          'time.observation': '2015-11-01T00:01:45+00:05'
          }
EVENT1 = {'__type': 'Event',
          'feed.url': 'https://dragonresearchgroup.org/insight/vncprobe.txt',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.ip': '78.93.247.94',
          'classification.type': 'brute-force',
          'time.source': '2015-11-09T20:18:17+00:00',
          'protocol.application': 'vnc',
          'protocol.transport': 'tcp',
          'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgICAgNzguOTMuMjQ3Ljk0ICB8ICAyMDE1LTExLTA5IDIwOjE4OjE3'
                 'ICB8ICB2bmNwcm9iZQ==',
          }
EVENT2 = {'__type': 'Event',
          'feed.url': 'https://dragonresearchgroup.org/insight/vncprobe.txt',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.ip': '142.91.104.105',
          'source.asn': 0,
          'source.as_name': 'Test-AS',
          'classification.type': 'brute-force',
          'time.source': '2015-11-10T02:04:34+00:00',
          'protocol.application': 'vnc',
          'protocol.transport': 'tcp',
          'raw': 'MDAgICAgICAgICAgIHwgIFRlc3QtQVMgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgIDE0Mi45MS4xMDQuMTA1ICB8ICAyMDE1LTExLTEwIDAyOjA0OjM0'
                 'ICB8ICB2bmNwcm9iZQ==',
          }


class TestDragonResearchGroupVNCParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DragonResearchGroupVNCParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DragonResearchGroupVNCParserBot
        cls.default_input_message = {'__type': 'Report'}

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)

if __name__ == '__main__':
    unittest.main()
