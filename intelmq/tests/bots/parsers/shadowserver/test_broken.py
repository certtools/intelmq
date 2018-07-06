# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

REPORT1 = {"raw": utils.base64_encode('adasdasdasdasd\nadasdasdafgf'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           }
REPORT2 = {"raw": utils.base64_encode('''timestamp,ip,port
2018-08-01T00:00:00+00,127.0.0.1,80
'''),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           }


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.sysconfig = {'feedname': 'Accessible-CWMP'}

    def test_broken(self):
        """
        Test a report which does not have valid fields
        """
        self.input_message = REPORT1
        self.allowed_error_count = 1
        self.run_bot()
        self.assertLogMatches(pattern="Failed to parse line.")
        self.assertLogMatches(pattern="ValueError: Required column 'timestamp' not found in data. Possible change in data format or misconfiguration.")
        self.assertLogMatches(pattern="Sent 0 events and found 1 error\(s\)\.",
                              levelname="INFO")

    def test_half_broken(self):
        """
        Test a report which does not have an optional field.
        """
        self.input_message = REPORT2
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertLogMatches(pattern="Optional key 'protocol' not found in data. Possible change in data format or misconfiguration.",
                              levelname="WARNING")
        self.assertLogMatches(pattern="Sent 1 events and found 0 error\(s\)\.",
                              levelname="INFO")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
