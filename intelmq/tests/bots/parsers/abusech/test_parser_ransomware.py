# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_ransomware import AbuseCHRansomwaretrackerParserBot

with open(os.path.join(os.path.dirname(__file__), 'ransomwaretracker.csv')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {'feed.url': 'https://ransomwaretracker.abuse.ch/feeds/csv',
                  'feed.name': 'AbuseCH Ransomwaretracker',
                  '__type': 'Report',
                  'raw': utils.base64_encode(EXAMPLE_FILE),
                  'time.observation': '2016-11-16T10:18:00+00:00'
                  }

EXAMPLE_EVENT = [{'feed.url': 'https://ransomwaretracker.abuse.ch/feeds/csv',
                 'feed.name': 'AbuseCH Ransomwaretracker',
                 '__type': 'Event',
                 'time.observation': '2016-11-16T10:18:00+00:00',
                 'raw': 'MjAxNi0xMS0xMSAxNjowNjowMCxEaXN0cmlidXRpb24gU2l0ZSxMb2NreSxtb3RlZnVndWUuY29tLGh0dHA6Ly9tb3RlZnVndWUuY29tLzY0NWQ1LG9ubGluZSxQQUtOSUMgKFBSSVZBVEUpIExJTUlURUQsMjEzLjE3Ni4yNDEuMjMwLDEzMDU1fDc5MjIsUlV8VVM=',
                 'classification.identifier': 'locky',
                 'classification.type': 'c&c',
                 'time.source': '2016-11-11T16:06:00+00:00',
                 'status': 'online',
                 'source.ip': '213.176.241.230',
                 'source.fqdn': 'motefugue.com',
                 'source.url': 'http://motefugue.com/645d5',
                 },
                 {'feed.url': 'https://ransomwaretracker.abuse.ch/feeds/csv',
                 'feed.name': 'AbuseCH Ransomwaretracker',
                 '__type': 'Event',
                 'time.observation': '2016-11-16T10:18:00+00:00',
                 'raw': 'MjAxNi0xMS0xMSAxNjowNjowMCxEaXN0cmlidXRpb24gU2l0ZSxMb2NreSxtb3RlZnVndWUuY29tLGh0dHA6Ly9tb3RlZnVndWUuY29tLzY0NWQ1LG9ubGluZSxQQUtOSUMgKFBSSVZBVEUpIExJTUlURUQsNjcuMTcxLjY1LjY0LDEzMDU1fDc5MjIsUlV8VVM=',
                 'classification.identifier': 'locky',
                 'classification.type': 'c&c',
                 'time.source': '2016-11-11T16:06:00+00:00',
                 'status': 'online',
                 'source.ip': '67.171.65.64',
                 'source.fqdn': 'motefugue.com',
                 'source.url': 'http://motefugue.com/645d5',
                 },
                 {'feed.url': 'https://ransomwaretracker.abuse.ch/feeds/csv',
                 'feed.name': 'AbuseCH Ransomwaretracker',
                 '__type': 'Event',
                 'time.observation': '2016-11-16T10:18:00+00:00',
                 'raw': 'MjAxNi0xMS0xNSAxMDowNzo1OSxQYXltZW50IFNpdGUsVG9ycmVudExvY2tlcixvam1la3p3NG11anZxZWp1Lm1pbml0aWxpLmF0LGh0dHA6Ly9vam1la3p3NG11anZxZWp1Lm1pbml0aWxpLmF0LyxvbmxpbmUsLDUuNzkuOTYuMzMsNjA3ODF8MjkxODJ8MjA3MDI3fDEyNjk1LE5M',
                 'classification.identifier': 'torrentlocker',
                 'classification.type': 'c&c',
                 'time.source': '2016-11-15T10:07:59+00:00',
                 'status': 'online',
                 'source.ip': '5.79.96.33',
                 'source.fqdn': 'ojmekzw4mujvqeju.minitili.at',
                 'source.url': 'http://ojmekzw4mujvqeju.minitili.at/',
                  }]


class TestAbuseCHRansomwaretrackerParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for AbuseCHRansomwaretrackerParserBot. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbuseCHRansomwaretrackerParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event hs been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT[0])
        self.assertMessageEqual(1, EXAMPLE_EVENT[1])
        self.assertMessageEqual(2, EXAMPLE_EVENT[2])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
