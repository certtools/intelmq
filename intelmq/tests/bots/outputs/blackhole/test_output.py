# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.blackhole.output import BlackholeOutputBot


class TestBlackholeOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BlackholeOutputBot

    def test_event(self):
        self.run_bot()
        self.assertOutputQueueLen(0)



if __name__ == '__main__':  # pragma: no cover
    unittest.main()
