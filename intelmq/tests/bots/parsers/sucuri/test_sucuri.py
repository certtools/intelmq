# -*- coding: utf-8 -*-
import codecs
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.sucuri.parser import SucuriParserBot
from intelmq.lib import utils

with codecs.open(os.path.join(os.path.dirname(__file__), 'test_sucuri.data'), encoding='UTF-8') as handle:
    REPORT_DATA = handle.read()
    REPORT_DATA_SPLIT = REPORT_DATA.splitlines()

REPORT = {"__type": "Report",
          "feed.name": "Sucuri Hidden Iframes",
          "feed.url": "http://labs.sucuri.net/?malware",
          "raw": utils.base64_encode(REPORT_DATA),
          "time.observation": "2018-01-22T14:38:24+00:00",
          }
EVENT1 = {"__type": "Event",
          "classification.identifier": "hidden-iframe",
          "classification.type": "blacklist",
          "feed.name": "Sucuri Hidden Iframes",
          "feed.url": "http://labs.sucuri.net/?malware",
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[616]),
          "source.url": "http://poseyhumane.org/stats.php",
          "time.observation": "2018-01-24T14:23:34+00:00",
          }
EVENT2 = {"classification.identifier": "hidden-iframe",
          "feed.url": "http://labs.sucuri.net/?malware",
          "time.observation": "2018-01-24T15:58:48+00:00",
          "__type": "Event",
          "feed.name": "Sucuri Hidden Iframes",
          "source.url": "http://zumobtr.ru/gate.php?f=1041671",
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[617]),
          "classification.type": "blacklist",
          }
EVENT3 = {'__type': 'Event',
          'classification.identifier': 'conditional-redirection',
          'classification.type': 'blacklist',
          'feed.name': 'Sucuri Hidden Iframes',
          'feed.url': 'http://labs.sucuri.net/?malware',
          "raw": utils.base64_encode(REPORT_DATA_SPLIT[624]),
          'source.url': 'http://goodhotwebmart.in/',
          }


class TestSucuriParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SucuriParserBot
        cls.default_input_message = REPORT

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, EVENT1)
        self.assertMessageEqual(1, EVENT2)
        self.assertMessageEqual(2, EVENT3)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
