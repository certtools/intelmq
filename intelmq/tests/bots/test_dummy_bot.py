# -*- coding: utf-8 -*-
import json
import unittest

import intelmq.lib.test as test
import intelmq.lib.bot as bot
from intelmq.lib.message import Event


EXAMPLE_EVENT = {"source.ip": "104.238.102.226",
                 "time.source": "2015-06-04T05:56:00+00:00",
                 "feed.url": "http://www.malwaredomainlist.com/updatescsv.php",
                 "source.reverse_domain_name": "ip-104-238-102-226.ip.secureserver.net.",
                 "source.url": "http://windows-crash-report.info",
                 "time.observation": "2015-08-11T13:03:40+00:00",
                 "raw": "MjAxNS8wNi8wNF8wNTo1Nix3aW5kb3dzLWNyYXNoLXJlcG9ydC5pbmZvLDEwNC4yMzguMTAyLjIyNixpcC0xMDQtMjM4LTEwMi0yMjYuaXAuc2VjdXJlc2VydmVyLm5ldC4sQnJvd2xvY2ssIEZha2UuVGVjaFN1cHBvcnQsV0lORE9XUy1DUkFTSC1SRVBPUlQuSU5GT0Bkb21haW5zYnlwcm94eS5jb20sMjY0OTY=",
                 "__type": "Event", "classification.type": "malware",
                 "description.text": "Browlock, Fake.TechSupport",
                 "source.asn": "26496",
                 "feed.name": "Malware Domain List"}
EXAMPLE_MESSAGE = json.dumps(EXAMPLE_EVENT)


class DummyBot(bot.Bot):
    """ A dummy bot only for testing porpuse. """

    def process(self):
        """ Passing through all information from report to Event. """
        report = self.receive_message()

        event = Event()
        self.logger.info('Lorem ipsum dolor sit amet')

        for key in report.keys():
            event.add(key, report[key])

        self.send_message(event)
        self.acknowledge_message()
        self.error_retries_counter = 1
        raise KeyboardInterrupt  # TODO: Should not be necessary


class TestDummyBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a DummyBot.
    """

    def reset_bot(self):
        self.bot_id = 'test-bot'
        self.bot_reference = DummyBot
        self.input_message = EXAMPLE_MESSAGE
        super(TestDummyBot, self).reset_bot()

    def test_log_test_line(self):
        """ Test if bot does log example message. """
        self.reset_bot()
        self.run_bot()
        self.assertRegexpMatches(self.loglines_buffer,
                                 "INFO - Lorem ipsum dolor sit amet")

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.reset_bot()
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
