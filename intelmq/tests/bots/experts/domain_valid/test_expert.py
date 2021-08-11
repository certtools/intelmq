# -*- coding: utf-8 -*-
"""
Domain validator

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import unittest
import intelmq.lib.test as test
from intelmq.bots.experts.domain_valid.expert import DomainValidExpertBot
import os.path

EXAMPLE_INPUT_DROP = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    'source.fqdn': '-soltane-tel-injas-heh.digital',
    "time.observation": "2020-10-13T06:14:49+00:00",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_DROP_2 = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    'source.fqdn': 'so6_ltane-tel-injas-heh.digital',
    "time.observation": "2020-10-13T06:14:49+00:00",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_DROP_3 = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    'source.fqdn': '-apk.info',
    "time.observation": "2020-10-13T06:14:49+00:00",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_PASS = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    'source.fqdn': 'soltane-tel-injas-heh.digital',
    "time.observation": "2020-10-13T06:14:49+00:00",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_PASS_2 = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    'source.fqdn': 'apk.info',
    "time.observation": "2020-10-13T06:14:49+00:00",
    "time.source": "2020-10-13T00:00:00+00:00"
}


@test.skip_exotic()
class TestDomainValidExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DomainValidExpertBot handling Reports.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DomainValidExpertBot
        cls.input_message = EXAMPLE_INPUT_DROP
        cls.sysconfig = {'domain_field': 'source.fqdn',
                         'tlds_domains_list': str(os.path.join(os.path.dirname(__file__), 'tlds-alpha-by-domain.txt'))}

    def test_expert_drop(self):
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_expert_drop_2(self):
        self.input_message = EXAMPLE_INPUT_DROP_2
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_expert_drop_3(self):
        self.input_message = EXAMPLE_INPUT_DROP_3
        self.run_bot()
        self.assertOutputQueueLen(0)

    def test_expert_pass(self):
        self.input_message = EXAMPLE_INPUT_PASS
        self.run_bot()
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, EXAMPLE_INPUT_PASS)

    def test_expert_pass_2(self):
        self.input_message = EXAMPLE_INPUT_PASS_2
        self.run_bot()
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, EXAMPLE_INPUT_PASS_2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
