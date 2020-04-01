# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

REPORT1 = {"raw": utils.base64_encode('adasdasdasdasd\nadasdasdafgf'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2019-01-01-scan_http-test-test.csv",
           }
REPORT2 = {"raw": utils.base64_encode('''timestamp,ip,port
2018-08-01T00:00:00+00,127.0.0.1,80
'''),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2019-01-01-scan_ftp-test-test.csv",
           }
REPORT3 = {"raw": utils.base64_encode('adasdasdasdasd\nadasdasdafgf'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2019-01-01-some_string-test-test.csv",
}
REPORT4 = {"raw": utils.base64_encode('adasdasdasdasd\nadasdasdafgf'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2020.wrong-filename.csv",
}


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.sysconfig = {"logging_level": "DEBUG"}

    def test_broken(self):
        """
        Test a report which does not have valid fields
        """
        self.input_message = REPORT1
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="Detected report's file name: 'scan_http'.",
                              levelname="DEBUG")
        self.assertLogMatches(pattern="Failed to parse line.")
        self.assertLogMatches(pattern="ValueError: Required column 'timestamp' not found in feed 'Accessible-HTTP'. Possible change in data format or misconfiguration.")
        self.assertLogMatches(pattern="Sent 0 events and found 1 problem\(s\)\.",
                              levelname="INFO")

    def test_half_broken(self):
        """
        Test a report which does not have an optional field.
        """
        self.input_message = REPORT2
        self.run_bot(allowed_warning_count=54)
        self.assertLogMatches(pattern="Detected report's file name: 'scan_ftp'.",
                              levelname="DEBUG")
        self.assertLogMatches(pattern="Optional key 'protocol' not found in feed 'Accessible-FTP'. Possible change in data format or misconfiguration.",
                              levelname="WARNING")
        self.assertLogMatches(pattern="Sent 1 events and found 0 problem\(s\)\.",
                              levelname="INFO")

    def test_no_config(self):
        """
        Test a report which does not have a valid extra.file_name
        """
        self.input_message = REPORT3
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: Could not get a config for 'some_string', check the documentation." )

    def test_invalid_filename(self):
        """
        Test a report which does not have a valid extra.file_name
        """
        self.input_message = REPORT4
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: Report's 'extra.file_name' '2020.wrong-filename.csv' is not valid." )

    def test_no_report_name(self):
        """
        Test a report without file_name and no given feedname as parameter.
        Error message should be verbose.
        """
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: No feedname given as parameter and the "
                                      "processed report has no 'extra.file_name'. "
                                      "Ensure that at least one is given. "
                                      "Also have a look at the documentation of the bot.")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
