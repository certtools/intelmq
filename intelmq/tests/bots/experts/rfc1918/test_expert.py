# -*- coding: utf-8 -*-
"""
Testing rfc 1918 expert bot.
"""
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.rfc1918.expert import RFC1918ExpertBot

INPUT1 = {"__type": "Event",
          "source.ip": "93.184.216.34",  # example.com
          "destination.ip": "192.0.2.9",  # TEST-NET-1
          "time.observation": "2015-01-01T00:00:00+00:00",
          }
OUTPUT1 = {"__type": "Event",
           "source.ip": "93.184.216.34",  # example.com
           "time.observation": "2015-01-01T00:00:00+00:00",
           }
INPUT2 = {"__type": "Event",
          "source.ip": "192.168.0.1",  #
          "time.observation": "2015-01-01T00:00:00+00:00",
          }


class TestRFC1918ExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RFC1918ExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = RFC1918ExpertBot
        self.sysconfig = {'fields': 'destination.ip,source.ip',
                          'policy': 'del,drop',
                          }
        self.default_input_message = {'__type': 'Event'}

    def test_del(self):
        self.input_message = INPUT1
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)

    def test_drop(self):
        self.input_message = INPUT2
        self.run_bot()
        self.assertOutputQueueLen(0)


if __name__ == '__main__':
    unittest.main()
