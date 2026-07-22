# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
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

    def test_csv_injection_is_escaped_by_default(self):
        self.input_message = {
            **EXAMPLE_INPUT,
            'event_description.text': '=HYPERLINK("https://example.invalid")',
        }
        self.run_bot(parameters={'fieldnames': 'event_description.text'})
        self.assertEqual(
            '"\'=HYPERLINK(""https://example.invalid"")"',
            json.loads(json.loads(self.get_output_queue()[0])['output']),
        )

    def test_csv_injection_escape_can_be_disabled(self):
        self.input_message = {
            **EXAMPLE_INPUT,
            'event_description.text': '=1+1',
        }
        self.run_bot(parameters={
            'escape_csv_injection': False,
            'fieldnames': 'event_description.text',
        })
        self.assertEqual('=1+1', json.loads(json.loads(self.get_output_queue()[0])['output']))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
