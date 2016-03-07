# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.dragonresearchgroup.parser_ssh import \
    DragonResearchGroupSSHParserBot


REPORT = {'__type': 'Report',
          'feed.url': 'https://dragonresearchgroup.org/insight/sshpwauth.txt',
          'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgIDQyLjEwMy4xMDMuMTM2ICB8ICAyMDE1LTExLTAzIDA3OjIyOjQ5'
                 'ICB8ICBzc2hwd2F1dGgKMDAgICAgICAgICAgIHwgIFRlc3QtQVMgICAgICAg'
                 'ICAgICAgICAgICAgICAgICAgfCAgIDE4Mi43My4xODIuMjI2ICB8ICAyMDE1'
                 'LTExLTA2IDAwOjM5OjQ2ICB8ICBzc2hwd2F1dGg=',
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENT1 = {'__type': 'Event',
          'feed.url': 'https://dragonresearchgroup.org/insight/sshpwauth.txt',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.ip': '42.103.103.136',
          'destination.port': 22,
          'classification.type': 'brute-force',
          'time.source': '2015-11-03T07:22:49+00:00',
          'protocol.application': 'ssh',
          'protocol.transport': 'tcp',
          'raw': 'TkEgICAgICAgICAgIHwgIE5BICAgICAgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgIDQyLjEwMy4xMDMuMTM2ICB8ICAyMDE1LTExLTAzIDA3OjIyOjQ5'
                 'ICB8ICBzc2hwd2F1dGg=',
          }
EVENT2 = {'__type': 'Event',
          'feed.url': 'https://dragonresearchgroup.org/insight/sshpwauth.txt',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.ip': '182.73.182.226',
          'destination.port': 22,
          'source.asn': 0,
          'source.as_name': 'Test-AS',
          'classification.type': 'brute-force',
          'time.source': '2015-11-06T00:39:46+00:00',
          'protocol.application': 'ssh',
          'protocol.transport': 'tcp',
          'raw': 'MDAgICAgICAgICAgIHwgIFRlc3QtQVMgICAgICAgICAgICAgICAgICAgICAg'
                 'ICAgfCAgIDE4Mi43My4xODIuMjI2ICB8ICAyMDE1LTExLTA2IDAwOjM5OjQ2'
                 'ICB8ICBzc2hwd2F1dGg=',
          }


class TestDragonResearchGroupSSHParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DragonResearchGroupSSHParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DragonResearchGroupSSHParserBot
        cls.default_input_message = {'__type': 'Report'}

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)

if __name__ == '__main__':
    unittest.main()
