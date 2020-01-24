#!/usr/bin/env python3

import unittest
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot


class TestShadowserverMapping(unittest.TestCase):

    def test_filename(self):
        self.assertEqual('scan_chargen',
                         ShadowserverParserBot._ShadowserverParserBot__is_filename_regex.search('2020-01-01-scan_chargen.csv').group(1))
        self.assertEqual('scan_chargen',
                         ShadowserverParserBot._ShadowserverParserBot__is_filename_regex.search('scan_chargen.csv').group(1))
