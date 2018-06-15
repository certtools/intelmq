# -*- coding: utf-8 -*-
import os.path
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.calidog.parser_certstream import CertStreamParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'data.json')) as handle:
    RAW = handle.read()


REPORT = {'__type': 'Report',
          'raw': utils.base64_encode(RAW),
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENTS = [{'__type': 'Event',
           'classification.type': 'other',
           'source.fqdn': 'fishpondcabins.com',
           'time.source': '2018-06-15T16:10:21+00:00',
           'raw': utils.base64_encode(RAW),
           },
          {'__type': 'Event',
           'classification.type': 'other',
           'source.fqdn': 'mail.fishpondcabins.com',
           'time.source': '2018-06-15T16:10:21+00:00',
           'raw': utils.base64_encode(RAW),
           },
          {'__type': 'Event',
           'classification.type': 'other',
           'source.fqdn': 'www.fishpondcabins.com',
           'time.source': '2018-06-15T16:10:21+00:00',
           'raw': utils.base64_encode(RAW),
           },
          ]


class TestCertStreamParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CertStreamParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CertStreamParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        for index, event in enumerate(EVENTS):
            self.assertMessageEqual(index, event)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
