# -*- coding: utf-8 -*-

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.key_value.parser import KeyValueParserBot
from intelmq.lib import utils

RAW_REPORTS = [
    'srcip=192.0.2.1 type=test',
    'srcip=192.0.2.1 type=test',
    'srcip=192.0.2.1 dstip=192.0.2.2 type=test',
    'header srcip=192.0.2.1 type=test trailer',
    'srcip="192.0.2.1" type="test"',
    'comment="Quoted" srcip=192.0.2.1 type=test',
    'srcip:192.0.2.1 type:test',
    'srcip=192.0.2.1|type=test',
    'srcip=192.0.2.1 type=test timestamp=1234567890',
    'srcip=192.0.2.1 type=test timestamp="2009-02-14T00:31:30+01:00"'
]

REPORTS = [
    {
        'feed.url': 'file://localhost/test',
        'feed.name': 'Key-value parser test',
        '__type': 'Report',
        'raw': utils.base64_encode(raw),
        'time.observation': '2020-09-11T10:40:18+02:00'
    } for raw in RAW_REPORTS]

KEYS = {
    'srcip': 'source.ip',
    'type': 'classification.type'
}

PARAMETERS = [
    {
        'keys': KEYS
    },
    {
        'keys': {**KEYS,
                 **{'dstip': 'destination.ip'}}
    },
    {
        'keys': KEYS
    },
    {
        'keys': KEYS
    },
    {
        'keys': KEYS,
        'strip_quotes': True
    },
    {
        'keys': {**KEYS,
                 **{'comment': 'comment'}},
        'strip_quotes': False
    },
    {
        'keys': KEYS,
        'kv_separator': ':'
    },
    {
        'keys': KEYS,
        'pair_separator': '|'
    },
    {
        'keys': {**KEYS,
                 **{'timestamp': 'time.source'}}
    },
    {
        'keys': {**KEYS,
                 **{'timestamp': 'time.source'}}
    }
]

EVENTS = [
    {
        'feed.url': 'file://localhost/test',
        'feed.name': 'Key-value parser test',
        '__type': 'Event',
        'raw': utils.base64_encode(raw),
        'time.observation': '2020-09-11T10:40:18+02:00',
        'source.ip': '192.0.2.1',
        'classification.type': 'test'
    } for raw in RAW_REPORTS]

EVENTS[5]['comment'] = '"Quoted"'
EVENTS[8]['time.source'] = '2009-02-13T23:31:30+00:00'
EVENTS[9]['time.source'] = '2009-02-13T23:31:30+00:00'


class TestKeyValueParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for KeyValueParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = KeyValueParserBot

    def test_simple(self):
        """
        All fields processed.
        """
        self.input_message = REPORTS[0]
        self.run_bot(parameters=PARAMETERS[0])
        self.assertMessageEqual(0, EVENTS[0])

    def test_extra_field(self):
        """
        Fields that are not propagated.
        """
        self.input_message = REPORTS[1]
        self.run_bot(parameters=PARAMETERS[1])
        self.assertMessageEqual(0, EVENTS[1])

    def test_ignored_field(self):
        """
        Ignore some fields.
        """
        self.input_message = REPORTS[2]
        self.run_bot(parameters=PARAMETERS[2])
        self.assertMessageEqual(0, EVENTS[2])

    def test_header(self):
        """
        Header and trailer tokens which are not key=value pairs.
        """
        self.input_message = REPORTS[3]
        self.run_bot(parameters=PARAMETERS[3])
        self.assertMessageEqual(0, EVENTS[3])

    def test_strip_quotes(self):
        """
        Strip quotes from values.
        """
        self.input_message = REPORTS[4]
        self.run_bot(parameters=PARAMETERS[4])
        self.assertMessageEqual(0, EVENTS[4])

    def test_preserve_quotes(self):
        """
        Preserve quotes.
        """
        self.input_message = REPORTS[5]
        self.run_bot(parameters=PARAMETERS[5])
        self.assertMessageEqual(0, EVENTS[5])

    def test_alternate_key_value_separator(self):
        """
        Separate keys and values with :, not =.
        """
        self.input_message = REPORTS[6]
        self.run_bot(parameters=PARAMETERS[6])
        self.assertMessageEqual(0, EVENTS[6])

    def test_alternate_pair_separator(self):
        """
        Separate key-value pairs with |, not ' '.
        """
        self.input_message = REPORTS[7]
        self.run_bot(parameters=PARAMETERS[7])
        self.assertMessageEqual(0, EVENTS[7])

    def test_timestamp_epoch(self):
        """
        Parse timestamp as ISO 8601.
        """
        self.input_message = REPORTS[8]
        self.run_bot(parameters=PARAMETERS[8])
        self.assertMessageEqual(0, EVENTS[8])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
