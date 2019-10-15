# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.geohash.expert import GeohashExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.geolocation.latitude": 48.2,  # Vienna
                 "source.geolocation.longitude": 16.366666666666666,
                 "destination.geolocation.latitude": -22.908333,  # Rio de Janeiro
                 "destination.geolocation.longitude": -43.196389,
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                 "source.geolocation.latitude": 48.2,  # Vienna
                 "source.geolocation.longitude": 16.366666666666666,
                 "extra.source.geolocation.geohash": "u2edhqt",
                 "destination.geolocation.latitude": -22.908333,  # Rio de Janeiro
                 "destination.geolocation.longitude": -43.196389,
                 "extra.destination.geolocation.geohash": "75cm9j9",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                  }


@test.skip_exotic()
class TestGeohashExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GeohashExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GeohashExpertBot
        cls.sysconfig = {'overwrite': True, 'precision': 7}

    def test_source_destination(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
