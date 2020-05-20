# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.cymru.parser_full_bogons import \
    CymruFullBogonsParserBot

REPORT = {'__type': 'Report',
          'feed.url': 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt',
          'raw': 'IyBsYXN0IHVwZGF0ZWQgMTQ1MDE5MzcwMiAoVHVlIERlYyAxNSAxNTozNTowMiAyMDE1IEdNVCkKMC4wLjAuMC84CjIuNTYuMC4wLzE0',
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENT1 = {'__type': 'Event',
          'feed.url': 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt',
          'time.source': '2015-12-15T15:35:02+00:00',
          'source.network': '0.0.0.0/8',
          'classification.type': 'blacklist',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'raw': 'IyBsYXN0IHVwZGF0ZWQgMTQ1MDE5MzcwMiAoVHVlIERlYyAxNSAxNTozNTowMiAyMDE1IEdNVCkKMC4wLjAuMC84',
          }
EVENT2 = {'__type': 'Event',
          'feed.url': 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt',
          'time.source': '2015-12-15T15:35:02+00:00',
          'source.network': '2.56.0.0/14',
          'classification.type': 'blacklist',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'raw': 'IyBsYXN0IHVwZGF0ZWQgMTQ1MDE5MzcwMiAoVHVlIERlYyAxNSAxNTozNTowMiAyMDE1IEdNVCkKMi41Ni4wLjAvMTQ='
          }
V6REPO = {'__type': 'Report',
          'feed.url': 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt',
          'raw': 'IyBsYXN0IHVwZGF0ZWQgMTU4NTE0MDYwMSAoV2VkIE1hciAyNSAxMjo1MDowMSAyMDIwIEdNVCkKOjovOAoxMDA6Oi84Cg==',
          'time.observation': '2020-03-25T16:42:45+00:00',
          }
V6EVEN = {'__type': 'Event',
          'feed.url': 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt',
          'time.source': '2020-03-25T12:50:01+00:00',
          'source.network': '::/8',
          'classification.type': 'blacklist',
          'time.observation': '2020-03-25T16:42:45+00:00',
          'raw': 'IyBsYXN0IHVwZGF0ZWQgMTU4NTE0MDYwMSAoV2VkIE1hciAyNSAxMjo1MDowMSAyMDIwIEdNVCkKOjovOA==',
          }


class TestCymruFullBogonsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CymruFullBogonsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CymruFullBogonsParserBot

    def test_ipv4_events(self):
        """ Test if correct IPv4 Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)

    def test_ipv6_events(self):
        """ Test if correct IPv6 Events have been produced. """
        self.input_message = V6REPO
        self.run_bot()
        self.assertMessageEqual(0, V6EVEN)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
