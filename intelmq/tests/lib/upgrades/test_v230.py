# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v230 import csv_parser_parameter_fix, deprecations, feed_changes


V230_IN = {
    "global": {},
    "urlhaus-parser": {
        "module": "intelmq.bots.parsers.generic.parser_csv",
        "parameters": {
            "delimeter": ","
        }
    }
}
V230_IN_BOTH = {
    "global": {},
    "urlhaus-parser": {
        "module": "intelmq.bots.parsers.generic.parser_csv",
        "parameters": {
            "delimeter": ",",
            "delimiter": ","
        }
    }
}
V230_OUT = {
    "global": {},
    "urlhaus-parser": {
        "module": "intelmq.bots.parsers.generic.parser_csv",
        "parameters": {
            "delimiter": ","
        }
    }
}
V230_MALWAREDOMAINLIST_IN = {
    "global": {},
    "malwaredomainlist-parser": {
        "module": "intelmq.bots.parsers.malwaredomainlist.parser",
        "parameters": {
        }
    },
    "malwaredomainlist-collector": {
        "module": "intelmq.bots.collectors.http.collector_http",
        "parameters": {
            "http_url": "http://www.malwaredomainlist.com/updatescsv.php"
        }
    }
}


class TestUpgradeV230(unittest.TestCase):
    def test_csv_parser_parameter_fix(self):
        """ Test feed_fix """
        result = csv_parser_parameter_fix(V230_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V230_OUT, result[1])

        # with also the new fixed parameter
        result = csv_parser_parameter_fix(V230_IN_BOTH, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V230_OUT, result[1])

        # with new parameter, no change
        result = csv_parser_parameter_fix(V230_OUT, {}, False)
        self.assertIsNone(result[0])
        self.assertEqual(V230_OUT, result[1])

    def test_deprecations(self):
        """ Test deprecations """
        result = deprecations(V230_MALWAREDOMAINLIST_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual('A discontinued bot "Malware Domain List Parser" has been found as bot '
                         'malwaredomainlist-parser. Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V230_MALWAREDOMAINLIST_IN, result[1])

    def test_feed_changes(self):
        """ Test feed_changes """
        result = feed_changes(V230_MALWAREDOMAINLIST_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual('A discontinued feed "Malware Domain List" has been found as bot '
                         'malwaredomainlist-collector. Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V230_MALWAREDOMAINLIST_IN, result[1])
