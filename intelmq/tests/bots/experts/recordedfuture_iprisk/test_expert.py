# -*- coding: utf-8 -*-
"""
Testing RF Risk node lookup
"""
import unittest
import pkg_resources
import intelmq.lib.test as test
from intelmq.bots.experts.recordedfuture_iprisk.expert import RecordedFutureIPRiskExpertBot

RFR_DB = pkg_resources.resource_filename('intelmq', 'tests/bots/experts/recordedfuture_iprisk/iprisk.dat')
EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "192.168.0.1",
                 "destination.ip": "192.0.43.8",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "extra.rf_iprisk.source": 65,
                  "destination.ip": "192.0.43.8",
                  "extra.rf_iprisk.destination": 0,
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EMPTY_INPUT = {"__type": "Event",
                       "source.ip": "10.0.0.1",
                       "time.observation": "2015-01-01T00:00:00+00:00",
                       }
EXAMPLE_EMPTY_OUTPUT = {"__type": "Event",
                        "source.ip": "10.0.0.1",
                        "extra.rf_iprisk.source": 0,
                        "time.observation": "2015-01-01T00:00:00+00:00",
                        }
EXISTING_INPUT = {"__type": "Event",
                  "source.ip": "192.168.0.1",
                  "extra.rf_iprisk.source": 10,
                  "destination.ip": "192.0.43.8",
                  "extra.rf_iprisk.destination": 0,
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }


class TestRecordedFutureIPRiskExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RecordedFutureIPRiskExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RecordedFutureIPRiskExpertBot
        cls.sysconfig = {'database': RFR_DB}

    # test one hit and one miss in rfriskdb, both source and destination in event
    def test_lookup(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    # test one miss in rfriskdb, only source present in event
    def test_empty_lookup(self):
        self.input_message = EXAMPLE_EMPTY_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EMPTY_OUTPUT)

    # test presence of rf_iprisk without overwrite
    def test_existing_not_overwrite(self):
        self.input_message = EXISTING_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXISTING_INPUT)

    # test presence of rf_iprisk with overwrite
    def test_existing_overwrite(self):
        self.sysconfig['overwrite'] = True
        self.input_message = EXISTING_INPUT
        self.run_bot()
        self.sysconfig['overwrite'] = False
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
