# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

REPORT1 = {"raw": utils.base64_encode('adasdasdasdasd\nadasdasdafgf'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2019-01-01-test_smb-test-test.csv",
           }
REPORT2 = {"raw": utils.base64_encode('timestamp,ip,port\n2018-08-01T00:00:00+00,127.0.0.1,80'),
           "__type": "Report",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "extra.file_name": "2019-01-01-test_telnet-test-test.csv",
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
REPORT5 = {"raw": utils.base64_encode('timestamp,ip,protocol,port,severity\n2018-08-01T00:00:00+00,127.0.0.1,tcp,7000,critical'),
           "__type": "Report",
           "time.observation": "2023-10-16T00:00:00+00:00",
           "extra.file_name": "2023-10-16-test_afs-test-test.csv",
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
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = REPORT1
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="Detected report's file name: 'test_smb'.",
                              levelname="DEBUG")
        self.assertLogMatches(pattern="Failed to parse line.")
        self.assertLogMatches(pattern="ValueError: Required column 'timestamp' not found in feed 'Test-Accessible-SMB'. Possible change in data format or misconfiguration.")
        self.assertLogMatches(pattern=r"Sent 0 events and found 1 problem\(s\)\.",
                              levelname="INFO")

    def test_half_broken(self):
        """
        Test a report which does not have an optional field.
        """
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = REPORT2
        self.run_bot(allowed_warning_count=63)
        self.assertLogMatches(pattern="Detected report's file name: 'test_telnet'.",
                              levelname="DEBUG")
        self.assertLogMatches(pattern="Optional key 'banner' not found in feed 'Test-Accessible-Telnet'.",
                              levelname="WARNING")
        self.assertLogMatches(pattern=r"Sent 1 events and found 0 problem\(s\)\.",
                              levelname="INFO")

    def test_no_config(self):
        """
        Test a report which does not have a valid extra.file_name
        """
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = REPORT3
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: Could not get a config for 'some_string', check the documentation.")

    def test_invalid_filename(self):
        """
        Test a report which does not have a valid extra.file_name
        """
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = REPORT4
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: Report's 'extra.file_name' '2020.wrong-filename.csv' is not valid.")

    def test_no_report_name(self):
        """
        Test a report without file_name and no given feedname as parameter.
        Error message should be verbose.
        """
        self.prepare_bot(parameters={'test_mode': True})
        self.run_bot(allowed_error_count=1)
        self.assertLogMatches(pattern="ValueError: No feedname given as parameter and the "
                                      "processed report has no 'extra.file_name'. "
                                      "Ensure that at least one is given. "
                                      "Also have a look at the documentation of the bot.")

    def test_field_not_in_idf(self):
        """
        Test a report that contains a field mapping not in the IDF.
        Error message should be verbose.
        """
        self.prepare_bot(parameters={'test_mode': True})
        self.input_message = REPORT5
        self.run_bot(allowed_error_count=0, allowed_warning_count=1)
        self.assertLogMatches(pattern="Key not found in IDF", levelname="WARNING")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
