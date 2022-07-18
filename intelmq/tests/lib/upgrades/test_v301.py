# SPDX-FileCopyrightText: 2022 Birger Schacht
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest
from intelmq.lib.upgrade.v301 import deprecations


V301_MALWAREDOMAINS_IN = {
    "global": {},
    "malwaredomains-parser": {
        "module": "intelmq.bots.parsers.malwaredomains.parser",
        "parameters": {
        }
    },
    "malwaredomains-collector": {
        "module": "intelmq.bots.collectors.http.collector",
        "parameters": {
            "http_url": "http://mirror1.malwaredomains.com/files/domains.txt"
        }
    }
}


class TestUpgradeV301(unittest.TestCase):
    def test_feed_changes(self):
        """ Test feed_changes """
        result = deprecations(V301_MALWAREDOMAINS_IN, {}, False)
        self.assertTrue(result[0])
        self.assertEqual('A discontinued bot "Malware Domains Parser" has been found as bot '
                         'malwaredomains-parser. A discontinued bot "Malware Domains Collector" '
                         'has been found as bot malwaredomains-collector. Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V301_MALWAREDOMAINS_IN, result[1])
