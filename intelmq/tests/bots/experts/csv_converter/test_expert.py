# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.csv_converter.expert import BOT

EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",
                 "destination.ip": "192.0.43.8",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.ip": "93.184.216.34",
                  "destination.ip": "192.0.43.8",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "output": '"2015-01-01T00:00:00+00:00,93.184.216.34"',
                  }
DELIMITER_OUT = EXAMPLE_OUTPUT.copy()
DELIMITER_OUT['output'] = EXAMPLE_OUTPUT['output'].replace(',', ';')


class TestCSVConverterExpertBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = BOT
        cls.sysconfig = {'fieldnames': 'time.observation,source.ip'}

    def test_default(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_delimiter(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot(parameters={'delimiter': ';'})
        self.assertMessageEqual(0, DELIMITER_OUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
