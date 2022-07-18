# SPDX-FileCopyrightText: 2022 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
import unittest

from intelmq.lib.upgrade.v220 import configuration, feed_changes


V220_MISP_VERIFY_FALSE = {
    "global": {"http_verify_cert": True},
    "misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
            "misp_verify": False}}}
V220_MISP_VERIFY_NULL = {
    "global": {"http_verify_cert": True},
    "misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {}}}
V220_MISP_VERIFY_TRUE = {
    "global": {"http_verify_cert": True},
    "misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
            "misp_verify": True}}}
V220_HTTP_VERIFY_FALSE = {
    "global": {"http_verify_cert": True},
    "misp-collector": {
        "module": "intelmq.bots.collectors.misp.collector",
        "parameters": {
            "http_verify_cert": False}}}
V220_FEED = {"global": {},
             "urlvir-hosts-collector": {
    "group": "Collector",
    "module": "intelmq.bots.collectors.http.collector_http",
    "parameters": {
        "http_url": "http://www.urlvir.com/export-hosts/",
    },
},
    "urlvir-parser": {
    "group": "Parser",
    "module": "intelmq.bots.parsers.urlvir.parser",
},
}


class TestUpgradeV220(unittest.TestCase):
    def test_configuration(self):
        """ Test configuration. """
        result = configuration(V220_MISP_VERIFY_TRUE, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V220_MISP_VERIFY_NULL, result[1])
        result = configuration(V220_MISP_VERIFY_FALSE, {}, False)
        self.assertTrue(result[0])
        self.assertEqual(V220_HTTP_VERIFY_FALSE, result[1])

    def test_feed_changes(self):
        """ Test feed_changes """
        result = feed_changes(V220_FEED, {}, False)
        self.assertEqual('A discontinued feed "URLVir" has been found '
                         'as bot urlvir-hosts-collector. '
                         'The removed parser "URLVir" has been found '
                         'as bot urlvir-parser. '
                         'Remove affected bots yourself.',
                         result[0])
        self.assertEqual(V220_FEED, result[1])
