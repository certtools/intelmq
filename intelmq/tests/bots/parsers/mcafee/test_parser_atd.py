# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.mcafee.parser_atd import ATDParserBot

with open(os.path.join(os.path.dirname(__file__), 'atdreport.txt')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.name": "ATD",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "time.observation": "2015-11-02T13:11:43+00:00"
                  }

EXAMPLE_EVENT = {"feed.name": "ATD",
                 "time.observation": "2015-11-02T13:11:44+00:00",
                 "classification.taxonomy": "malicious code",
                 "classification.type": "infected-system",
                 "raw": utils.base64_encode(EXAMPLE_FILE),
                 'malware.hash.md5': '6C3F06652A4868E005EB42DAAF1CEE43',
                 'malware.hash.sha1': '6B53023EE7E6E336913DEBAD5BAD7E633362407A',
                 'malware.hash.sha256': 'DDBBB3C3141024A17E1F20C09C75D8913809062A3D326E2AC81626E65215C430',
                 'malware.name': 'install-tmetrade-trust-2f9aec.exe',
                 "__type": "Event"
                 }


class TestATDParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ATDParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ATDParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'verdict_severity': 4}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

