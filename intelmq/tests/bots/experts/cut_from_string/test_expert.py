# -*- coding: utf-8 -*-
"""
Testing cut from string
"""
import unittest
import intelmq.lib.test as test
from intelmq.bots.experts.cut_from_string.expert import CutFromStringExpertBot

EXAMPLE_INPUT = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'www.google.lt',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

EXAMPLE_OUTPUT = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'google.lt',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

EXAMPLE_OUTPUT1 = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'www.google',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

EXAMPLE_INPUT_2 = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

EXAMPLE_OUTPUT_2 = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}


class TestCutFromStringExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TestCutFromStringExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CutFromStringExpertBot

    def test_event_cut_start(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_event_cut_without_field(self):
        self.input_message = EXAMPLE_INPUT_2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_2)

    def test_event_cut_end(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot(parameters={"string_from_start": 0, "string_for_cut": ".lt"})
        self.assertMessageEqual(0, EXAMPLE_OUTPUT1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
