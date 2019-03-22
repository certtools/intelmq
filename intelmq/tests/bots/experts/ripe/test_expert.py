# -*- coding: utf-8 -*-
"""
Testing RIPE Expert
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.ripencc_abuse_contact.expert import RIPEExpertBot

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
DB_404_AS = {"__type": "Event",
             "source.asn": 7713,
             "time.observation": "2015-01-01T00:00:00+00:00",
             }
GEOLOCA_INPUT1 = {"__type": "Event",
                  "source.ip": "96.30.37.204"
                  }
GEOLOCA_INPUT2 = {"__type": "Event",
                  "source.geolocation.cc": "IN",
                  "source.ip": "96.30.37.204"
                  }
GEOLOCA_OUTPUT1 = {"__type": "Event",
                   "source.ip": "96.30.37.204",
                   "source.geolocation.cc": "US",
                   "source.geolocation.city": "Lansing",
                   "source.geolocation.latitude": 42.7348,
                   "source.geolocation.longitude": -84.6245
                   }
GEOLOCA_OUTPUT3 = {"__type": "Event",
                   "source.ip": "96.30.37.204",
                   "source.geolocation.cc": "IN",
                   "source.geolocation.city": "Lansing",
                   "source.geolocation.latitude": 42.7348,
                   "source.geolocation.longitude": -84.6245
                   }
INDEX_ERROR = {"__type": "Event",
               "source.ip": "228.66.141.189",
               }
QUESTION_MARK = {"__type": "Event",
               "source.ip": "35.197.157.0",
               }
QUESTION_MARK_OUTPUT = {"__type": "Event",
                        "source.ip": "35.197.157.0",
                        'source.geolocation.latitude': 35.0,
                        'source.geolocation.longitude': 105.0,
                        }

@test.skip_internet()
class TestRIPEExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RIPEExpertBot.
    """

    def tearDown(self):
        if self.bot is not None:
            self.bot.http_session.close()

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RIPEExpertBot
        cls.sysconfig = {'query_ripe_db_asn': True,
                         'query_ripe_db_ip': True,
                         'query_ripe_stat_ip': False,
                         'query_ripe_stat_asn': False,
                         'redis_cache_db': 4,
                         'query_ripe_stat_geolocation': False,
                         }
        cls.use_cache = True

    def test_db_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)
        self.assertEqual(self.cache.get('db_asn:35492'), b'["abuse@funkfeuer.at"]')
        self.assertEqual(self.cache.get('db_ip:93.184.216.34'), b'["abuse@verizondigitalmedia.com"]')
        self.assertEqual(self.cache.get('db_ip:193.238.157.5'), b'["abuse@funkfeuer.at"]')

    def test_db_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)
        self.assertEqual(self.cache.get('db_ip:2001:62a:4:100:80::8'), b'["security.zid@univie.ac.at"]')

    def test_empty_lookup(self):
        """ No email is returned, event should be untouched. """
        self.input_message = EMPTY_INPUT
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)

    @test.skip_local_web()
    def test_ripe_stat_errors(self):
        """ Test RIPE stat for errors. """
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_asn': True,
                          'query_ripe_stat_ip': True,
                          'query_ripe_stat_geolocation': False,
                          }
        self.input_message = EMPTY_INPUT
        self.allowed_error_count = 1
        self.prepare_bot()
        old = self.bot.QUERY['stat']
        self.bot.QUERY['stat'] = 'http://localhost/{}'
        self.run_bot(prepare=False)
        # internal json in < and >= 3.5 and simplejson
        self.assertLogMatches(pattern='.*(JSONDecodeError|ValueError|Expecting value|No JSON object could be decoded).*',
                              levelname='ERROR')

        self.bot.URL_STAT_CONTACT = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.URL_STAT_CONTACT = old
        self.assertLogMatches(pattern='.*HTTP status code was 404.*',
                              levelname='ERROR')
        self.cache.flushdb()  # collides with test_replace

    @test.skip_local_web()
    def test_ripe_db_as_errors(self):
        """ Test RIPE DB AS for errors. """
        self.sysconfig = {'query_ripe_db_asn': True,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': False,
                          'query_ripe_stat_geolocation': False,
                          }
        self.input_message = EXAMPLE_INPUT
        self.allowed_error_count = 1
        self.allowed_warning_count = 1
        self.prepare_bot()
        old = self.bot.QUERY['db_asn']
        self.bot.QUERY['db_asn'] = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.QUERY['db_asn'] = old
        self.assertLogMatches(pattern='.*HTTP status code was 404.*',
                              levelname='ERROR')

    @test.skip_local_web()
    def test_ripe_db_ip_errors(self):
        """ Test RIPE DB IP for errors. """
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': True,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': False,
                          'query_ripe_stat_geolocation': False,
                          }
        self.input_message = EXAMPLE_INPUT
        self.allowed_error_count = 1
        self.allowed_warning_count = 1
        self.prepare_bot()
        old = self.bot.QUERY['db_ip']
        self.bot.QUERY['db_ip'] = 'http://localhost/{}'
        self.run_bot(prepare=False)
        self.bot.QUERY['db_ip'] = old
        self.assertLogMatches(pattern='.*HTTP status code was 404.*',
                              levelname='ERROR')

    def test_replace(self):
        self.sysconfig = {'mode': 'replace',
                          'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': True,
                          'query_ripe_stat_asn': False,
                          'query_ripe_stat_geolocation': False,
                          }
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_REPLACED)
        self.assertEqual(self.cache.get('stat:127.0.0.1'), b'__no_contact')
        self.cache.flushdb()  # collides with test_ripe_stat_errors

    def test_ripe_db_as_404(self):
        """ Server returns a 404 which should not be raised. """
        self.sysconfig = {'query_ripe_db_asn': True,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': False,
                          'query_ripe_stat_geolocation': False,
                          }
        self.input_message = DB_404_AS
        self.run_bot()
        self.assertMessageEqual(0, DB_404_AS)

    def test_geolocation(self):
        self.input_message = GEOLOCA_INPUT1
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': True,
                          }
        self.run_bot()
        self.assertMessageEqual(0, GEOLOCA_OUTPUT1)

    def test_geolocation_overwrite(self):
        self.input_message = GEOLOCA_INPUT2
        self.sysconfig = {'mode': 'replace',
                          'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': True,
                          }
        self.run_bot()
        self.assertMessageEqual(0, GEOLOCA_OUTPUT1)

    def test_geolocation_not_overwrite(self):
        self.input_message = GEOLOCA_INPUT2
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_asn': True,
                          }
        self.run_bot()
        self.assertMessageEqual(0, GEOLOCA_OUTPUT3)

    def test_index_error(self):
        self.input_message = INDEX_ERROR
        self.run_bot()
        self.assertMessageEqual(0, INDEX_ERROR)

    def test_country_question_mark(self):
        """
        Response has '?' as country
        https://stat.ripe.net/data/maxmind-geo-lite/data.json?resource=35.197.157.0
        """
        self.input_message = QUESTION_MARK
        self.sysconfig = {'query_ripe_db_asn': False,
                          'query_ripe_db_ip': False,
                          'query_ripe_stat_asn': False,
                          'query_ripe_stat_ip': False,
                          'query_ripe_stat_geolocation': True,
                          }
        self.run_bot()
        self.assertMessageEqual(0, QUESTION_MARK_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
