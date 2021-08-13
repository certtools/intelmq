# -*- coding: utf-8 -*-
"""
Testing truncate by delimiter bot

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import unittest
import intelmq.lib.test as test
from intelmq.bots.experts.truncate_by_delimiter.expert import TruncateByDelimiterExpertBot

EXAMPLE_INPUT = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'bing.com.google.com.digikala.com.myket.com.divar.ir.varzesh3.pw.aparat.com.torojoonemadaretkarkonkhasteshodamdigeenqadtestzadam.filterchipedaramodarovordibekeshbiroon.dollarshode20000tomanbaskondigeh.salavatemohammadibefres.soltane-tel-injas-heh.digital',
    'extra.elastic_index': 'cti-2020-10',
    'extra.elastic_id': 'VwVnSnUBXjJtaqsUSw8T'}

EXAMPLE_OUTPUT = {
    '__type': 'Event',
    'feed.accuracy': 100.0,
    'feed.name': 'MISP events',
    'feed.provider': 'MISP BAE',
    'time.observation': '2020-10-20T12:57:33+00:00',
    'feed.url': 'https://sig01.threatreveal.com',
    'source.fqdn': 'pw.aparat.com.torojoonemadaretkarkonkhasteshodamdigeenqadtestzadam.filterchipedaramodarovordibekeshbiroon.dollarshode20000tomanbaskondigeh.salavatemohammadibefres.soltane-tel-injas-heh.digital',
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


class TestTruncateByDelimiterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TestTruncateByDelimiterExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TruncateByDelimiterExpertBot

    def test_event_cut(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_event_cut_without_field(self):
        self.input_message = EXAMPLE_INPUT_2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT_2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
