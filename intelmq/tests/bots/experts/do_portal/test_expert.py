# -*- coding: utf-8 -*-
"""
TODO: Test on wrong credentials
TODO: Test on wrong URL
"""
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.do_portal.expert import DoPortalExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.network": "83.136.39.0/24",  # nic.at
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.abuse_contact": "reports@cert.at",
                  "source.network": "83.136.39.0/24",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.network": "2001:67c:10b8::/48",  # ipcom/nic.at
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.network": "2001:67c:10b8::/48",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.abuse_contact": "reports@cert.at",
                   }
EMPTY_INPUT = {"__type": "Event",
               "source.network": "127.0.0.0/8",  # no result
               "time.observation": "2015-01-01T00:00:00+00:00",
               }


@test.skip_internet()
@test.skip_travis()
class TestDoPortalExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DoPortalExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DoPortalExpertBot
        cls.sysconfig = {"portal_url": "https://cp-aec-stg.cert.at/",
                         "portal_api_key": os.environ.get('DO_PORTAL_KEY')}

    def test_ipv4_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_ipv6_lookup(self):
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT6)

    def test_empty_result(self):
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
