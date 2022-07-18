# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v222 import feed_changes


V222 = {
    "global": {},
    "shadowserver-parser": {
        "module": "intelmq.bots.parsers.shadowserver.parser",
        "parameters": {
            "feedname": "Blacklisted-IP"}}}
V222_OUT = {
    "global": {},
    "shadowserver-parser": {
        "module": "intelmq.bots.parsers.shadowserver.parser",
        "parameters": {
            "feedname": "Blocklist"}}}


class TestUpgradeV222(unittest.TestCase):
    def test_feed_changes(self):
        """ Test v222_feed_changes """
        result = feed_changes(V222, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V222_OUT, result[1])
