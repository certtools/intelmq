# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.ripencc_abuse_contact.expert import RIPENCCExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 "destination.ip": "193.238.157.5",  # funkfeuer.at
                 "destination.asn": 35492,
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "source.abuse_contact": "abuse@verizondigitalmedia.com",
                  "destination.ip": "193.238.157.5",
                  "destination.abuse_contact": "abuse@funkfeuer.at",
                  "destination.asn": 35492,
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:62a:4:100:80::8",  # nic.at
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:62a:4:100:80::8",
                   "source.abuse_contact": "security.zid@univie.ac.at",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   }
EMPTY_INPUT = {"__type": "Event",
               "source.ip": "127.0.0.1",
               "source.abuse_contact": "bla@example.com",
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
EMPTY_REPLACED = {"__type": "Event",
                  "source.ip": "127.0.0.1",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


@test.skip_internet()
class TestRIPENCCExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for AbusixExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RIPENCCExpertBot
        cls.sysconfig = {'query_ripe_db_asn': True,
                         'query_ripe_db_ip': True,
                         'query_ripe_stat': True,
                         }

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertLogMatches(pattern="^The parameter 'query_ripe_stat' is deprecated and will be r",
                              levelname="WARNING")
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_empty_lookup(self):
        """ No email is returned, event should be untouched. """
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)

    @test.skip_local_web()
    def test_ripe_stat_errors(self):
        """ Test RIPE stat for errors. """
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_asn': True,
                          'query_ripe_stat_ip': True,
                          }
        self.input_message = EMPTY_INPUT
        self.allowed_error_count = 1
        self.prepare_bot()
        old = self.bot.URL_STAT
        self.bot.URL_STAT = 'https://example.com/index.html?{}'
        self.run_bot(prepare=False)
        # internal json in < and >= 3.5, 3.3 and simplejson
        self.assertLogMatches(pattern='.*(JSONDecodeError|ValueError|Expecting value|No JSON object could be decoded).*',
                              levelname='ERROR')

        self.bot.URL_STAT = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.URL_STAT = old
        self.assertLogMatches(pattern='HTTP status code was 404',
                              levelname='ERROR')

    @test.skip_local_web()
    def test_ripe_db_as_errors(self):
        """ Test RIPE DB AS for errors. """
        self.sysconfig = {'query_ripe_db_asn': True,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat': False,
                          }
        self.input_message = EXAMPLE_INPUT
        self.allowed_error_count = 1
        self.prepare_bot()
        old = self.bot.URL_DB_AS
        self.bot.URL_DB_AS = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.URL_DB_AS = old
        self.assertLogMatches(pattern='HTTP status code was 404',
                              levelname='ERROR')

    @test.skip_local_web()
    def test_ripe_db_ip_errors(self):
        """ Test RIPE DB IP for errors. """
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': True,
                          'query_ripe_stat': False,
                          }
        self.input_message = EXAMPLE_INPUT
        self.allowed_error_count = 1
        self.prepare_bot()
        old = self.bot.URL_DB_IP
        self.bot.URL_DB_IP = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.URL_DB_IP = old
        self.assertLogMatches(pattern='HTTP status code was 404',
                              levelname='ERROR')

    def test_replace(self):
        self.sysconfig = {'mode': 'replace'}
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_REPLACED)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
