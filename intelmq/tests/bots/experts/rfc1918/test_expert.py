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
INPUT_URL1 = {"__type": "Event",
             "source.url": "http://sub.example.com/foo/bar",
             "time.observation": "2015-01-01T00:00:00+00:00",
             }
INPUT_URL2 = {"__type": "Event",
             "source.url": "http://192.168.0.1/foo/bar",
             "time.observation": "2015-01-01T00:00:00+00:00",
             }
INPUT_ASN = {"__type": "Event",
             "source.asn": 64496,
             "time.observation": "2015-01-01T00:00:00+00:00",
             }
INPUT_DIFFERENT_DOMAIN = {"__type": "Event",
                          "destination.fqdn": "fooexample.com",
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
                                   'destination.fqdn,source.url,source.url,source.asn',
                         'policy': 'del,drop,drop,del,drop,drop,drop',
                         }
        cls.default_input_message = INPUT1

    def test_del(self):
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

    def test_drop_url1(self):
        self.input_message = INPUT_URL1
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_drop_url2(self):
        self.input_message = INPUT_URL2
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_drop_asn(self):
        self.input_message = INPUT_ASN
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_empty_parameters(self):
        self.run_bot(parameters={"fields": "",
                                 "policy": ""})

    def test_different_domain(self):
        """ Check that fooexample.com is not falsely recognized """
        self.input_message = INPUT_DIFFERENT_DOMAIN
        self.run_bot()
        self.assertMessageEqual(0, INPUT_DIFFERENT_DOMAIN)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
