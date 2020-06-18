# -*- coding: utf-8 -*-
"""
Test OutputBot specifics
"""

from intelmq.lib.bot import OutputBot
from intelmq.lib.test import BotTestCase

from unittest import TestCase
from json import dumps

RAW = {"__type": "Event", "raw": "Cg=="}
DICT = {"foo": "bar", "foobar": 1}
OUTPUT_DICT = {"__type": "Event", "output": dumps(DICT, sort_keys=True)}
STRING = "foobar!"
OUTPUT_STRING = {"__type": "Event", "output": dumps(STRING)}
INT = 123
OUTPUT_INT = {"__type": "Event", "output": dumps(INT)}
INPUT = {"__type": "Event", "raw": "Cg==", "source.ip": "127.0.0.1"}
RAW_HIERARCHICAL = {"raw": "Cg==", "source": {"ip": "127.0.0.1"}}
NO_RAW_TYPE = {"__type": "Event", "source.ip": "127.0.0.1"}

class DummyOutputBot(OutputBot):

    def process(self):
        event = self.receive_message()
        self.result = self.export_event(event, return_type=self.parameters.return_type)


class TestDummyOutputBot(BotTestCase, TestCase):
    @classmethod
    def set_bot(cls):
        cls.sysconfig = {"return_type": None}
        cls.bot_reference = DummyOutputBot
        cls.default_input_message = RAW
        cls.allowed_error_count = 1

    def test_export_raw(self):
        self.run_bot(parameters={"single_key": "raw"})
        self.assertEqual(self.bot.result, "\n")

    def test_export_output_dict(self):
        self.input_message = OUTPUT_DICT
        self.run_bot(parameters={"single_key": "output"})
        self.assertEqual(self.bot.result, DICT)

    def test_export_output_dict_string(self):
        self.input_message = OUTPUT_DICT
        self.run_bot(parameters={"single_key": "output", "return_type": str})
        self.assertEqual(self.bot.result, OUTPUT_DICT['output'])

    def test_export_output_string(self):
        self.input_message = OUTPUT_STRING
        self.run_bot(parameters={"single_key": "output"})
        self.assertEqual(self.bot.result, STRING)

    def test_export_output_string_string(self):
        self.input_message = OUTPUT_STRING
        self.run_bot(parameters={"single_key": "output", "return_type": str})
        self.assertEqual(self.bot.result, STRING)

    def test_export_output_int(self):
        self.input_message = OUTPUT_INT
        self.run_bot(parameters={"single_key": "output"})
        self.assertEqual(self.bot.result, INT)

    def test_export_output_int_string(self):
        self.input_message = OUTPUT_INT
        self.run_bot(parameters={"single_key": "output", "return_type": str})
        self.assertEqual(self.bot.result, OUTPUT_INT['output'])

    def test_export_keep_raw_hierarchical(self):
        self.input_message = INPUT
        self.run_bot(parameters={"keep_raw_field": True,
                                 "message_hierarchical": True,
                                 "message_with_type": False,
                                 })
        self.assertEqual(self.bot.result, RAW_HIERARCHICAL)

    def test_export_keep_raw_hierarchical_string(self):
        self.input_message = INPUT
        self.run_bot(parameters={"keep_raw_field": True,
                                 "message_hierarchical": True,
                                 "message_with_type": False,
                                 "return_type": str,
                                 })
        self.assertEqual(self.bot.result, dumps(RAW_HIERARCHICAL,
                                                sort_keys=True))

    def test_export_now_raw_type(self):
        self.input_message = INPUT
        self.run_bot(parameters={"keep_raw_field": False,
                                 "message_with_type": True,
                                 })
        self.assertEqual(self.bot.result, NO_RAW_TYPE)
