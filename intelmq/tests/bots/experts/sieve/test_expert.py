# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import os
import intelmq.lib.test as test
from intelmq.bots.experts.sieve.expert import SieveExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "127.0.0.1",
                 "source.abuse_contact": "abuse@example.com",
                 "time.observation": "2017-01-01T00:00:00+00:00",
                 }

EXAMPLE_OUTPUT = {"__type": "Event",
                 "source.ip": "127.0.0.1",
                 "source.abuse_contact": "abuse@example.com",
                 "time.observation": "2017-01-01T00:00:00+00:00",
                 "source.asn": 559
                 }

class TestSieveExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SieveExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SieveExpertBot
        cls.default_input_message = EXAMPLE_INPUT
        cls.sysconfig = {'file': os.path.join(os.path.dirname(__file__), 'test.sieve')}

    # This is an example how to test the log output
#    def test_log_test_line(self):
#        """ Test if bot does log example message. """
#        self.run_bot()
#        self.assertRegexpMatches(self.loglines_buffer, "INFO - Lorem ipsum dolor sit amet")

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        event = self.get_output_queue()[0]
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
