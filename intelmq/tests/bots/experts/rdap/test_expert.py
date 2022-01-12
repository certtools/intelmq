# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing rdap expert.
"""

import unittest
import os

import requests_mock

import intelmq.lib.test as test
from intelmq.bots.experts.rdap.expert import RDAPExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://nic.versicherung/something/index.php",
                 "source.fqdn": "nic.versicherung",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "http://nic.versicherung/something/index.php",
                  "source.fqdn": "nic.versicherung",
                  "source.abuse_contact": "service@tld-box.at",
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }

EXAMPLE_INPUT2 = EXAMPLE_INPUT.copy()
EXAMPLE_INPUT2['source.fqdn'] = 'example.com'
EXAMPLE_OUTPUT2 = EXAMPLE_OUTPUT.copy()
EXAMPLE_OUTPUT2['source.fqdn'] = 'example.com'
EXAMPLE_OUTPUT2['source.abuse_contact'] = 'service@example.com'
EXAMPLE_404 = {"__type": "Event",
               "source.fqdn": "this-record-does-not-exist.versicherung",
               "time.observation": "2015-01-01T00:00:00+00:00"
               }


def prepare_mocker(mocker):
    with open(os.path.join(os.path.dirname(__file__), 'test_data', 'rdns.json'), 'rb') as f:
        mocker.get('https://data.iana.org/rdap/dns.json', content=f.read())
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'test_data')):
        with open(os.path.join(os.path.dirname(__file__), 'test_data', filename), 'rb') as f:
            mocker.get('http://localhost/rdap/v1/domain/%s' % filename.replace('.json', ''), content=f.read())
    mocker.get('http://localhost/rdap/v1/domain/this-record-does-not-exist.versicherung', status_code=404)


@requests_mock.Mocker()
class TestRDAPExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for RDAPExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = RDAPExpertBot
        cls.sysconfig = {
            'rdap_bootstrapped_servers': {
                'com': 'http://localhost/rdap/v1/',
                'versicherung': 'http://localhost/rdap/v1/',
            }
        }
        cls.use_cache = True

    def test(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_object_validation(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT2
        self.allowed_warning_count = 1
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_404(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_404
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_404)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
