# SPDX-FileCopyrightText: 2025 Ladislav Baco
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Test with example reports (STIX objects usually collected from TAXII server)
"""
import unittest

import re
import requests_mock

import intelmq.lib.bot as bot
import intelmq.lib.test as test
from intelmq.bots.parsers.stix.parser_eset import ESETStixParserBot


EXAMPLE_REPORT = {'__type': 'Report',
                  'feed.name': 'Botnet feed',
                  'feed.code': 'botnet stix 2.1',
                  'feed.provider': 'ESET',
                  'feed.documentation': 'https://help.eset.com/eti_portal/en-US/botnet-feed.',
                  'feed.accuracy': 100.0,
                  'feed.url': 'https://taxii.eset.com/taxii2/643f4eb5-f8b7-46a3-a606-6d61d5ce223a/collections/0abb06690b0b47e49cd7794396b76b20/',
                  'raw': 'eyJpZCI6ICJpbmRpY2F0b3ItLTAiLCAidHlwZSI6ICJpbmRpY2F0b3IiLCAic3BlY192ZXJzaW9uIjogIjIuMSIsICJjcmVhdGVkIjogIjE5NzAtMDEtMDFUMDA6MDA6MDAuMDAwWiIsICJtb2RpZmllZCI6ICIxOTcwLTAxLTAxVDAwOjAwOjAwLjAwMFoiLCAicGF0dGVybiI6ICJbdXJsOnZhbHVlID0gJ2h0dHA6Ly9leGFtcGxlLm9yZyddIiwgInBhdHRlcm5fdHlwZSI6ICJzdGl4IiwgInZhbGlkX2Zyb20iOiAiMTk3MC0wMS0wMVQwMDowMDowMFoiLCAiZGVzY3JpcHRpb24iOiAiQyZDIGluZGljYXRlcyB0aGF0IGEgYm90bmV0IFdpbjMyL1NweS5MdW1tYVN0ZWFsZXIuQiB0cm9qYW4gaXMgcHJlc2VudC4iLCAibGFiZWxzIjogWyJtYWxpY2lvdXMtYWN0aXZpdHkiXX0='
                  }

EXAMPLE_EVENT = {'__type': 'Event',
                 'feed.name': 'Botnet feed',
                 'feed.code': 'botnet stix 2.1',
                 'feed.provider': 'ESET',
                 'feed.documentation': 'https://help.eset.com/eti_portal/en-US/botnet-feed.',
                 'feed.accuracy': 100.0,
                 'feed.url': 'https://taxii.eset.com/taxii2/643f4eb5-f8b7-46a3-a606-6d61d5ce223a/collections/0abb06690b0b47e49cd7794396b76b20/',
                 'source.url': 'http://example.org',
                 'time.source': '1970-01-01T00:00:00+00:00',
                 'classification.type': 'c2-server',
                 'malware.name': 'lummastealer',
                 'comment': 'C&C indicates that a botnet Win32/Spy.LummaStealer.B trojan is present.',
                 'extra.labels': ['malicious-activity'],
                 'raw': 'eyJpZCI6ICJpbmRpY2F0b3ItLTAiLCAidHlwZSI6ICJpbmRpY2F0b3IiLCAic3BlY192ZXJzaW9uIjogIjIuMSIsICJjcmVhdGVkIjogIjE5NzAtMDEtMDFUMDA6MDA6MDAuMDAwWiIsICJtb2RpZmllZCI6ICIxOTcwLTAxLTAxVDAwOjAwOjAwLjAwMFoiLCAicGF0dGVybiI6ICJbdXJsOnZhbHVlID0gJ2h0dHA6Ly9leGFtcGxlLm9yZyddIiwgInBhdHRlcm5fdHlwZSI6ICJzdGl4IiwgInZhbGlkX2Zyb20iOiAiMTk3MC0wMS0wMVQwMDowMDowMFoiLCAiZGVzY3JpcHRpb24iOiAiQyZDIGluZGljYXRlcyB0aGF0IGEgYm90bmV0IFdpbjMyL1NweS5MdW1tYVN0ZWFsZXIuQiB0cm9qYW4gaXMgcHJlc2VudC4iLCAibGFiZWxzIjogWyJtYWxpY2lvdXMtYWN0aXZpdHkiXX0='
                 }

@test.skip_exotic()
class TestESETStixParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for an ESETStixParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ESETStixParserBot
        cls.sysconfig = {}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.input_message = EXAMPLE_REPORT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_classification_by_string(self):
        """ Test if correct classification based on string is returned. """
        classification_type, malware_name = self.bot_reference.classify('Host actively distributes high-severity malicious content in the form of executable code.')
        self.assertEqual(str(classification_type), 'malware-distribution')
        self.assertEqual(malware_name, None)

        classification_type, malware_name = self.bot_reference.classify('Host is known source of phishing or other fraudulent content.')
        self.assertEqual(str(classification_type), 'phishing')
        self.assertEqual(malware_name, None)

        classification_type, malware_name = self.bot_reference.classify('Host is used as command and control server.')
        self.assertEqual(str(classification_type), 'c2-server')
        self.assertEqual(malware_name, None)

        classification_type, malware_name = self.bot_reference.classify('Web services scanning and attacks')
        self.assertEqual(str(classification_type), 'scanner')
        self.assertEqual(malware_name, None)

        classification_type, malware_name = self.bot_reference.classify('RDP bruteforce IP')
        self.assertEqual(str(classification_type), 'brute-force')
        self.assertEqual(malware_name, None)

    def test_classification_by_regex(self):
        """ Test if correct classification based on regex is returned. """
        classification_type, malware_name = self.bot_reference.classify('C&C indicates that a botnet Win32/Spy.LummaStealer.B trojan is present.')
        self.assertEqual(str(classification_type), 'c2-server')
        self.assertEqual(str(malware_name), 'lummastealer')

        classification_type, malware_name = self.bot_reference.classify('C&C of Win32/Spy.LummaStealer.B trojan')
        self.assertEqual(str(classification_type), 'c2-server')
        self.assertEqual(str(malware_name), 'lummastealer')

        classification_type, malware_name = self.bot_reference.classify('Host is used as command and control server of Win32/Emotet.BN trojan malware family.')
        self.assertEqual(str(classification_type), 'c2-server')
        self.assertEqual(str(malware_name), 'emotet')

        classification_type, malware_name = self.bot_reference.classify('WizardNet backdoor.')
        self.assertEqual(str(classification_type), 'malware')
        self.assertEqual(str(malware_name), 'wizardnet')

        classification_type, malware_name = self.bot_reference.classify('Loader for Emotet')
        self.assertEqual(str(classification_type), 'malware')
        self.assertEqual(str(malware_name), 'emotet')

    def test_unknown_classification(self):
        """ Test if undetermined classification is returned when comment contains something unexpected. """
        classification_type, malware_name = self.bot_reference.classify('Example of unexpected comment.')
        self.assertEqual(str(classification_type), 'undetermined')
        self.assertEqual(malware_name, None)

    def test_malware_family_name_extraction(self):
        """ Test if correct malwae family name is extracted from the given malware string. """
        malware_name = self.bot_reference.extract_malware_family('Win32/Spy.LummaStealer.B')
        self.assertEqual(str(malware_name), 'lummastealer')

        malware_name = self.bot_reference.extract_malware_family('Win32/Rescoms.B')
        self.assertEqual(str(malware_name), 'rescoms')

        malware_name = self.bot_reference.extract_malware_family('Emotet')
        self.assertEqual(str(malware_name), 'emotet')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
