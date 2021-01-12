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
                 "source.ip": "131.130.254.75",  # nic.at
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 "source.abuse_contact": "something@example.com",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.abuse_contact": "security.zid@univie.ac.at",
                  "source.ip": "131.130.254.75",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT_APPEND = {"__type": "Event",
                         "source.abuse_contact": "something@example.com,security.zid@univie.ac.at",
                         "source.ip": "131.130.254.75",
                         "time.observation": "2015-01-01T00:00:00+00:00",
                         }
EXAMPLE_INPUT6 = {"__type": "Event",
                  "source.ip": "2001:67c:10b8::1",  # ipcom/nic.at
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_OUTPUT6 = {"__type": "Event",
                   "source.ip": "2001:67c:10b8::1",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.abuse_contact": "reports@cert.at",
                   }
EXAMPLE_OUTPUT_APPEND_EMPTY = {"__type": "Event",
                   "source.ip": "2001:67c:10b8::1",
                   "time.observation": "2015-01-01T00:00:00+00:00",
                   "source.abuse_contact": "reports@cert.at",
                   }
EMPTY_INPUT = {"__type": "Event",
               "source.ip": "127.0.0.1",  # no result
               "time.observation": "2015-01-01T00:00:00+00:00",
               "source.abuse_contact": "reports@cert.at",
               }
EMPTY_OUTPUT = {"__type": "Event",
                "source.ip": "127.0.0.1",  # no result
                "time.observation": "2015-01-01T00:00:00+00:00",
                }


@test.skip_internet()
@unittest.skipUnless(os.environ.get('DO_PORTAL_KEY'),
                     'No DO portal key provided.')
@unittest.skipUnless(os.environ.get('DO_PORTAL_URL'),
                     'No DO portal URL provided.')
class TestDoPortalExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DoPortalExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DoPortalExpertBot
        cls.sysconfig = {"portal_url": os.environ.get('DO_PORTAL_URL'),
                         "portal_api_key": os.environ.get('DO_PORTAL_KEY'),
                         "mode": "replace"}

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
        self.assertMessageEqual(0, EMPTY_OUTPUT)

    def test_ipv4_lookup_append(self):
        self.sysconfig["mode"] = "append"
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_APPEND)
        self.sysconfig["mode"] = "replace"

    def test_ipv6_lookup_append_empty(self):
        self.sysconfig["mode"] = "append"
        self.input_message = EXAMPLE_INPUT6
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_APPEND_EMPTY)
        self.sysconfig["mode"] = "replace"

    def test_empty_result_append(self):
        self.sysconfig["mode"] = "append"
        self.input_message = EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EMPTY_INPUT)
        self.sysconfig["mode"] = "replace"


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
