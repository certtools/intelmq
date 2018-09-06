# -*- coding: utf-8 -*-
"""
Testing RIPE Expert
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.ripe.expert import RIPEExpertBot

EXAMPLE_INPUT1 = {"__type": "Event",
                  "source.ip": "96.30.37.204"
                  }
EXAMPLE_INPUT2 = {"__type": "Event",
                  "source.geolocation.cc": "IN",
                  "source.ip": "96.30.37.204"
                  }
EXAMPLE_OUTPUT1 = {"__type": "Event",
                   "source.ip": "96.30.37.204",
                   "source.geolocation.cc": "US",
                   "source.geolocation.city": "Lansing",
                   "source.geolocation.latitude": 42.7257,
                   "source.geolocation.longitude": -84.636
                   }
EXAMPLE_OUTPUT2 = {"__type": "Event",
                   "source.ip": "96.30.37.204",
                   "source.geolocation.cc": "US",
                   "source.geolocation.city": "Lansing",
                   "source.geolocation.latitude": 42.7257,
                   "source.geolocation.longitude": -84.636
                   }
EXAMPLE_OUTPUT3 = {"__type": "Event",
                   "source.ip": "96.30.37.204",
                   "source.geolocation.cc": "IN",
                   "source.geolocation.city": "Lansing",
                   "source.geolocation.latitude": 42.7257,
                   "source.geolocation.longitude": -84.636
                   }


class TestRIPEExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RIPEExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = RIPEExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)

    def test_overwrite(self):
        self.input_message = EXAMPLE_INPUT2
        self.sysconfig = {"overwrite": True}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_not_overwrite(self):
        self.input_message = EXAMPLE_INPUT2
        self.sysconfig = {"overwrite": False}
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
