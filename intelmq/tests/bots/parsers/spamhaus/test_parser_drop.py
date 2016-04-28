# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.spamhaus.parser_drop import SpamhausDropParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'drop.lasso')) as handle:
    EXAMPLE_FILE = handle.read()

REPORT = {'__type': 'Report',
          'feed.name': 'Spamhaus Drop',
          'feed.url': 'https://www.spamhaus.org/drop/drop.lasso',
          'raw': utils.base64_encode(EXAMPLE_FILE),
          'time.observation': '2015-09-14T12:00:00+02:00',
          }
TEMPLATE = {'__type': 'Event',
            'feed.name': 'Spamhaus Drop',
            'feed.url': 'https://www.spamhaus.org/drop/drop.lasso',
            'time.observation': '2015-09-14T12:00:00+02:00',
            'time.source': '2015-09-14T04:39:22+00:00',
            'classification.type': 'spam',
            }
EVENTS = ({'source.network': '1.4.0.0/17',
           'extra': '{"blocklist": "SBL256893"}',
           'raw': 'MS40LjAuMC8xNyA7IFNCTDI1Njg5Mw=='},
          {'source.network': '1.10.16.0/20',
           'extra': '{"blocklist": "SBL256894"}',
           'raw': 'MS4xMC4xNi4wLzIwIDsgU0JMMjU2ODk0'},
          {'source.network': '1.116.0.0/14',
           'extra': '{"blocklist": "SBL216702"}',
           'raw': 'MS4xMTYuMC4wLzE0IDsgU0JMMjE2NzAy'},
          {'source.network': '5.34.242.0/23',
           'extra': '{"blocklist": "SBL194796"}',
           'raw': 'NS4zNC4yNDIuMC8yMyA7IFNCTDE5NDc5Ng=='},
          {'source.network': '5.72.0.0/14',
           'extra': '{"blocklist": "SBL167293"}',
           'raw': 'NS43Mi4wLjAvMTQgOyBTQkwxNjcyOTM='},
          {'source.network': '14.4.0.0/14',
           'extra': '{"blocklist": "SBL187947"}',
           'raw': 'MTQuNC4wLjAvMTQgOyBTQkwxODc5NDc='},
          {'source.network': '14.245.0.0/16',
           'extra': '{"blocklist": "SBL258300"}',
           'raw': 'MTQuMjQ1LjAuMC8xNiA7IFNCTDI1ODMwMA=='},
          {'source.network': '27.122.32.0/20',
           'extra': '{"blocklist": "SBL257062"}',
           'raw': 'MjcuMTIyLjMyLjAvMjAgOyBTQkwyNTcwNjI='},
          {'source.network': '27.126.160.0/20',
           'extra': '{"blocklist": "SBL257064"}',
           'raw': 'MjcuMTI2LjE2MC4wLzIwIDsgU0JMMjU3MDY0'},
          {'source.network': '27.133.208.0/20',
           'extra': '{"blocklist": "SBL257335"}',
           'raw': 'MjcuMTMzLjIwOC4wLzIwIDsgU0JMMjU3MzM1'},
          )


class TestSpamhausDropParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SpamhausDropParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SpamhausDropParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

    def test_from_file(cls):
        cls.input_message = REPORT
        cls.run_bot()
        for count, event in enumerate(EVENTS):
            event.update(TEMPLATE)
            cls.assertMessageEqual(count, event)


if __name__ == '__main__':
    unittest.main()
