# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.bambenek.parser_c2dommasterlist import Bambenekc2dommasterlistParserBot

with open(os.path.join(os.path.dirname(__file__), 'c2-dommasterlist.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "Bambenek C2 Domain Feed",
                  "feed.url": "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2016-01-01T00:00:00+00:00",
                  }
EVENTS = [{"feed.name": "Bambenek C2 Domain Feed",
           "feed.url": "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt",
           "__type": "Event",
           "time.source": "2016-11-12T15:02:00+00:00",
           "source.fqdn": "sfkh21okrrnlu.com",
           "classification.type": "c&c",
           "status": "online",
           "time.observation": "2016-01-01T00:00:00+00:00",
           "event_description.text": "Domain used by shiotob/urlzone/bebloh",
           "event_description.url": "http://osint.bambenekconsulting.com/manual/bebloh.txt",
           "raw": "c2ZraDIxb2tycm5sdS5jb20sRG9tYWluIHVzZWQgYnkgc2hpb3RvYi91cmx6b25lL2JlYmxvaCwyMDE2LTExLTEyIDE1OjAyLGh0dHA6Ly9vc2ludC5iYW1iZW5la2NvbnN1bHRpbmcuY29tL21hbnVhbC9iZWJsb2gudHh0",
           }]


class TestBambenekc2dommasterlistParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Bambenekc2dommasterlistParserBot
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Bambenekc2dommasterlistParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EVENTS[0])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
