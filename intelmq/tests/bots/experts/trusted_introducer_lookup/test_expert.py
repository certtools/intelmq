# -*- coding: utf-8 -*-
"""
Testing trusted introducer Expert

SPDX-FileCopyrightText: 2021 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import unittest
import os

import requests_mock

import intelmq.lib.test as test
from intelmq.bots.experts.trusted_introducer_lookup.expert import TrustedIntroducerLookupExpertBot

EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://nic.versicherung/something/index.php",
                 "source.fqdn": "nic.versicherung",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "http://nic.versicherung/something/index.php",
                  "source.fqdn": "nic.versicherung",
                  "source.abuse_contact": "team@cert.at",
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }

EXAMPLE_INPUT2 = EXAMPLE_INPUT.copy()
EXAMPLE_INPUT2['source.fqdn'] = 'tuwien.ac.at'
EXAMPLE_INPUT2['source.url'] = 'http://tuwien.ac.at'
EXAMPLE_OUTPUT2 = EXAMPLE_INPUT2.copy()
EXAMPLE_OUTPUT2['source.abuse_contact'] = 'cert@aco.net'

EXAMPLE_INPUT3 = EXAMPLE_INPUT.copy()
del EXAMPLE_INPUT3['source.fqdn']
EXAMPLE_INPUT3['source.asn'] = 679
EXAMPLE_OUTPUT3 = EXAMPLE_INPUT3.copy()
EXAMPLE_OUTPUT3['source.abuse_contact'] = 'cert@aco.net'


def prepare_mocker(mocker):
    with open(os.path.join(os.path.dirname(__file__), 'test_data', 'teams.json'), 'rb') as f:
        mocker.get('https://www.trusted-introducer.org/directory/teams.json', content=f.read())

@test.skip_internet()
@requests_mock.Mocker()
class TestTrustedIntroducerLookupExpert(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for Trusted Introducer Lookup Expert.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = TrustedIntroducerLookupExpertBot

    def test(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)

    def test_subdomains(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT2)

    def test_asn(self, mocker):
        prepare_mocker(mocker)
        self.input_message = EXAMPLE_INPUT3
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_OUTPUT3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
