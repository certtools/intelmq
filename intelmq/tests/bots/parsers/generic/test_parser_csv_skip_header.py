# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.generic.parser_csv import GenericCsvParserBot

INPUT_1 = """\
11.11.11.11,http://test.com
5.5.5.5,https://example.com
"""

INPUT_2 = """\
source_ip,source_url
11.11.11.11,http://test.com
5.5.5.5,https://example.com
"""

INPUT_3 = """\
another line to be skipped
source_ip,source_url
11.11.11.11,http://test.com
5.5.5.5,https://example.com
"""

OUTPUT_1 = [
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'MTEuMTEuMTEuMTEsaHR0cDovL3Rlc3QuY29tCg==',
        'source.ip': '11.11.11.11',
        'source.url': 'http://test.com'
    },
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'NS41LjUuNSxodHRwczovL2V4YW1wbGUuY29tCg==',
        'source.ip': '5.5.5.5',
        'source.url': 'https://example.com'
    }
]

OUTPUT_2 = [
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'c291cmNlX2lwLHNvdXJjZV91cmwKMTEuMTEuMTEuMTEsaHR0cDovL3Rlc3QuY29tCg==',
        'source.ip': '11.11.11.11',
        'source.url': 'http://test.com'
    },
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'c291cmNlX2lwLHNvdXJjZV91cmwKNS41LjUuNSxodHRwczovL2V4YW1wbGUuY29tCg==',
        'source.ip': '5.5.5.5',
        'source.url': 'https://example.com'
    }
]

OUTPUT_3 = [
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'YW5vdGhlciBsaW5lIHRvIGJlIHNraXBwZWQKc291cmNlX2lwLHNvdXJjZV91cmwKMTEuMTEuMTEuMTEsaHR0cDovL3Rlc3QuY29tCg==',
        'source.ip': '11.11.11.11',
        'source.url': 'http://test.com'
    },
    {
        '__type': 'Event',
        'classification.type': 'blacklist',
        'raw': 'YW5vdGhlciBsaW5lIHRvIGJlIHNraXBwZWQKc291cmNlX2lwLHNvdXJjZV91cmwKNS41LjUuNSxodHRwczovL2V4YW1wbGUuY29tCg==',
        'source.ip': '5.5.5.5',
        'source.url': 'https://example.com'
    }
]


class TestGenericCsvParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for GenericCsvParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = GenericCsvParserBot

    def test_skip_header_false(self):
        self.input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT_1)}
        self.run_bot(parameters={"skip_header": False, "columns": ["source.ip", "source.url"],
                                 "default_fields": {"classification.type": "blacklist"}})
        self.assertMessageEqual(0, OUTPUT_1[0])
        self.assertMessageEqual(1, OUTPUT_1[1])

    def test_skip_header_true(self):
        self.input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT_2)}
        self.run_bot(parameters={"skip_header": True, "columns": ["source.ip", "source.url"],
                                 "default_fields": {"classification.type": "blacklist"}})
        self.assertMessageEqual(0, OUTPUT_2[0])
        self.assertMessageEqual(1, OUTPUT_2[1])

    def test_skip_header_2(self):
        self.input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT_3)}
        self.run_bot(parameters={"skip_header": 2, "columns": ["source.ip", "source.url"],
                                 "default_fields": {"classification.type": "blacklist"}})
        self.assertMessageEqual(0, OUTPUT_3[0])
        self.assertMessageEqual(1, OUTPUT_3[1])
