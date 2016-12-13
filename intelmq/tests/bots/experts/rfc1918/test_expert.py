# -*- coding: utf-8 -*-
"""
Testing rfc 1918 expert bot.
"""

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
          "source.ip": "192.168.0.1",  # internal
          "time.observation": "2015-01-01T00:00:00+00:00",
          }
INPUT_TLD = {"__type": "Event",
             "source.fqdn": "sub.example.com",
             "time.observation": "2015-01-01T00:00:00+00:00",
             }
INPUT_DOMAIN = {"__type": "Event",
                "destination.fqdn": "sub.example.invalid",
                "time.observation": "2015-01-01T00:00:00+00:00",
                }
OUTPUT_DOMAIN = {"__type": "Event",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
INPUT_URL = {"__type": "Event",
             "source.url": "http://sub.example.com/foo/bar",
             "time.observation": "2015-01-01T00:00:00+00:00",
             }


class TestRFC1918ExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RFC1918ExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RFC1918ExpertBot
        cls.sysconfig = {'fields': 'destination.ip,source.ip,source.fqdn,'
                                   'destination.fqdn,source.url',
                         'policy': 'del,drop,drop,del,drop',
                         }

    def test_del(self):
        self.input_message = INPUT1
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)

    def test_drop(self):
        self.input_message = INPUT2
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_drop_tld(self):
        self.input_message = INPUT_TLD
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_del_domain(self):
        self.input_message = INPUT_DOMAIN
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_DOMAIN)

    def test_drop_url(self):
        self.input_message = INPUT_URL
        self.run_bot()
        self.assertOutputQueueLen(0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
