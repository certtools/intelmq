# SPDX-FileCopyrightText: 2016 Sebastian Wagner, 2025 Ladislav Baco
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Test with reports, based on intelmq/tests/lib/test_collector_bot.py
"""
import unittest

import re
import requests_mock

import intelmq.lib.bot as bot
import intelmq.lib.test as test
from intelmq.bots.collectors.taxii.collector import TaxiiCollectorBot


EXAMPLE_REPORT = {'__type': 'Report',
                  'feed.name': 'Taxii Feed',
                  'feed.code': 'feed stix2.1',
                  'feed.provider': 'Taxii Provider',
                  'feed.documentation': 'Taxii Documentation',
                  'feed.accuracy': 100.0,
                  'feed.url': 'http://localhost/feed',
                  'raw': 'eyJpZCI6ICJpbmRpY2F0b3ItLTAiLCAidHlwZSI6ICJpbmRpY2F0b3IiLCAic3BlY192ZXJzaW9uIjogIjIuMSIsICJjcmVhdGVkIjogIjE5NzAtMDEtMDFUMDA6MDA6MDAuMDAwWiIsICJtb2RpZmllZCI6ICIxOTcwLTAxLTAxVDAwOjAwOjAwLjAwMFoiLCAicGF0dGVybiI6ICJbdXJsOnZhbHVlID0gJ2h0dHA6Ly9leGFtcGxlLm9yZyddIiwgInBhdHRlcm5fdHlwZSI6ICJzdGl4IiwgInZhbGlkX2Zyb20iOiAiMTk3MC0wMS0wMVQwMDowMDowMFoifQ=='
                  }

def prepare_mocker(mocker):
    mocker.get(
        'http://localhost/feed/',
        json={
            'id': 'feed',
            'title': 'feed stix2.1',
            'can_read': True,
            'can_write': False
        },
        headers={'Content-Type': 'application/taxii+json;version=2.1'}
    )
    mocker.get(
        re.compile('http://localhost/feed/objects/.*'),
        json={
            'id': 'feed',
            'title': 'feed stix2.1',
            'can_read': True,
            'can_write': False,
            'more': False,
            'objects': [{
                'id': 'indicator--0',
                'type': 'indicator',
                'spec_version': '2.1',
                'created': '1970-01-01T00:00:00.000Z',
                'modified': '1970-01-01T00:00:00.000Z',
                'pattern': "[url:value = 'http://example.org']",
                'pattern_type': 'stix',
                'valid_from': '1970-01-01T00:00:00Z'
            }]},
            headers={'Content-Type': 'application/taxii+json;version=2.1'}
    )

@test.skip_exotic()
@requests_mock.Mocker()
class TestTaxiiCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a TaxiiCollectorBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TaxiiCollectorBot
        cls.sysconfig = {'name': 'Taxii Feed',
                         'provider': 'Taxii Provider',
                         'documentation': 'Taxii Documentation',
                         'collection': 'http://localhost/feed',
                         'username': 'user',
                         'password': 'pass'
                         }

    def test_event(self, mocker):
        """ Test if correct Event has been produced. """
        prepare_mocker(mocker)
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_REPORT)

    def test_missing_collection(self, mocker):
        """ Test if missing collection is detected. """
        with self.assertRaises(ValueError) as context:
            self.run_bot(parameters={'collection': None})
        exception = context.exception
        self.assertEqual(str(exception), 'No TAXII collection URL provided.')

    def test_missing_username(self, mocker):
        """ Test if missing username is detected. """
        with self.assertRaises(ValueError) as context:
            self.run_bot(parameters={'username': None})
        exception = context.exception
        self.assertEqual(str(exception), 'No TAXII username provided.')

    def test_missing_password(self, mocker):
        """ Test if missing password is detected. """
        with self.assertRaises(ValueError) as context:
            self.run_bot(parameters={'password': None})
        exception = context.exception
        self.assertEqual(str(exception), 'No TAXII password provided.')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
