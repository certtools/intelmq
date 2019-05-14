# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.blocklistde.parser import BlockListDEParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'imap.txt')) as handle:
    EXAMPLE_FILE = handle.read()

REPORT = {'__type': 'Report',
          'feed.name': 'BlockList.de',
          'feed.url': 'https://lists.blocklist.de/lists/imap.txt',
          'raw': utils.base64_encode(EXAMPLE_FILE),
          'time.observation': '2015-09-14T12:00:00+02:00',
          }
TEMPLATE = {'__type': 'Event',
            'feed.name': 'BlockList.de',
            'feed.url': 'https://lists.blocklist.de/lists/imap.txt',
            'time.observation': '2015-09-14T12:00:00+02:00',
            'classification.type': 'ids-alert',
            'protocol.application': 'imap',
            'event_description.text': 'IP reported as having run attacks on '
                                      'the service IMAP, SASL, POP3',
            }
EVENTS = ({'source.ip': '192.0.2.4',
           'raw': 'MTkyLjAuMi40'},
          {'source.ip': '192.0.2.45',
           'raw': 'MTkyLjAuMi40NQ=='},
          {'source.ip': '198.51.100.34',
           'raw': 'MTk4LjUxLjEwMC4zNA=='},
          {'source.ip': '198.51.100.80',
           'raw': 'MTk4LjUxLjEwMC44MA=='},
          {'source.ip': '203.0.113.34',
           'raw': 'MjAzLjAuMTEzLjM0'},
          {'source.ip': '203.0.113.254',
           'raw': 'MjAzLjAuMTEzLjI1NA=='},
          )


class TestBlockListDEParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for BlockListDEParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BlockListDEParserBot

    def test_imap(self):
        self.input_message = REPORT
        self.run_bot()
        for count, event in enumerate(EVENTS):
            event.update(TEMPLATE)
            self.assertMessageEqual(count, event)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
