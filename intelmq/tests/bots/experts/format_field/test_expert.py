# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.format_field.expert import FormatFieldExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "feed.name": "AbuseCh URLHaus Feed",
                  "extra.tags": "ddos,elf,gafgyt"}

EXAMPLE_INPUT2 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "feed.name": "test-feed",
                  "malware.name": " cryptowall ",
                  "extra.abuse": " abuse@iana.org"}

EXAMPLE_INPUT3 = {"__type": "Event",
                  "classification.type": "malware",
                  "time.observation": "2018-07-27T00:00:00+00:00",
                  "feed.name": "test-feed-1",
                  "feed.url": "http://localhost/a.php"}

EXAMPLE_OUTPUT1 = {"__type": "Event",
                   "classification.type": "malware",
                   "time.observation": "2018-07-27T00:00:00+00:00",
                   "feed.name": "AbuseCh URLHaus Feed",
                   "extra.tags": ["ddos", "elf", "gafgyt"]}

EXAMPLE_OUTPUT2 = {"__type": "Event",
                   "classification.type": "malware",
                   "time.observation": "2018-07-27T00:00:00+00:00",
                   "feed.name": "test-feed",
                   "malware.name": "cryptowall",
                   "extra.abuse": "abuse@iana.org"}

EXAMPLE_OUTPUT3 = {"__type": "Event",
                   "classification.type": "malware",
                   "time.observation": "2018-07-27T00:00:00+00:00",
                   "feed.name": "test-feed-1",
                   "feed.url": "http://127.0.0.1/a.php"}


class TestFormatFieldExpertBot(test.BotTestCase, unittest.TestCase):
    """
    TestCases for FormatFieldExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FormatFieldExpertBot

    def test_split(self):
        self.input_message = EXAMPLE_INPUT1
        self.sysconfig = {"split_column": "extra.tags", "split_separator": ","}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_strip(self):
        self.input_message = EXAMPLE_INPUT2
        self.sysconfig = {"strip_columns": "malware.name,extra.abuse"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_replace(self):
        self.input_message = EXAMPLE_INPUT3
        self.sysconfig = {"replace_column": "feed.url", "old_value": "localhost",
                          "new_value": "127.0.0.1"}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
