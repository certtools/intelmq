# -*- coding: utf-8 -*-

import unittest
import time

import intelmq.lib.test as test
from intelmq.bots.experts.wait.expert import WaitExpertBot


EXAMPLE_INPUT1 = {"__type": "Event",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }


class TestWaitExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for WaitExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = WaitExpertBot

    def test_dummy(self):
        self.input_message = EXAMPLE_INPUT1
        before = time.time()
        self.run_bot()
        after = time.time()
        self.assertMessageEqual(0, EXAMPLE_INPUT1)
        self.assertLess(after-before, 0.5)

    def test_sleep(self):
        self.input_message = EXAMPLE_INPUT1
        self.sysconfig = {'sleep_time': 0.5}
        before = time.time()
        self.run_bot()
        after = time.time()
        self.assertMessageEqual(0, EXAMPLE_INPUT1)
        self.assertGreater(after-before, 0.5)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
