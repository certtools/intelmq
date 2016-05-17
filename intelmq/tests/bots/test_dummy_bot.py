# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.bot as bot
import intelmq.lib.test as test
from intelmq.lib.message import Event

EXAMPLE_REPORT = {"source.ip": "192.0.2.3",
                  "time.source": "2015-06-04T13:37:00+00:00",
                  "feed.url": "http://www.example.com/",
                  "source.reverse_dns": "reverse.example.net",
                  "source.url": "http://example.org",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": "MjAxNS8wNi8wNF8xMzozNyxleGFtcGxlLm9yZywxOTIuMC4yLjMs"
                         "cmV2ZXJzZS5leGFtcGxlLm5ldCxleGFtcGxlIGRlc2NyaXB0aW9u"
                         "LHJlcG9ydEBleGFtcGxlLm9yZywwMDAwMAo=",
                  "__type": "Report",
                  "classification.type": "malware",
                  "event_description.text": "example description",
                  "source.asn": 00000,
                  "feed.name": "Example"}
EXAMPLE_EVENT = EXAMPLE_REPORT
EXAMPLE_EVENT['__type'] = 'Event'


class DummyParserBot(bot.Bot):
    """
    A dummy bot only for testing purpose.
    """

    def process(self):
        """
        Passing through all information from Report to Event.

        Also logs a sample line, which will be tested afterwards.
        """
        report = self.receive_message()

        if not report:
            self.acknowledge_message()
            return

        event = Event()
        self.logger.info('Lorem ipsum dolor sit amet')

        for key in report.keys():
            event.add(key, report[key], sanitize=False)

        self.send_message(event)
        self.acknowledge_message()


class TestDummyParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a DummyBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_log_test_line(self):
        """ Test if bot does log example message. """
        self.run_bot()
        self.assertRegexpMatchesLog("INFO - Lorem ipsum dolor sit amet")

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
