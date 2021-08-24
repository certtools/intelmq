# -*- coding: utf-8 -*-
"""
Time based filtering

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.time_filter.expert import TimeFilterExpertBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from freezegun import freeze_time
except ImportError:
    freeze_time = None

EXAMPLE_INPUT_DROP = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    "feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
    "time.observation": "2020-10-13T06:14:49+00:00",
    "raw": "dGVzdA==",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "source.port": 447,
    "extra.lastonline": "2020-08-13T00:00:00+00:00",
    "malware.name": "trickbot",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_PASS = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    "feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
    "time.observation": "2020-10-13T06:14:49+00:00",
    "raw": "dGVzdA==",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "source.port": 447,
    "extra.lastonline1": "2020-09-13T00:00:00+00:00",
    "malware.name": "trickbot",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_PASS_2 = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    "feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
    "time.observation": "2020-10-13T06:14:49+00:00",
    "raw": "dGVzdA==",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "source.port": 447,
    "extra.lastonline": "",
    "malware.name": "trickbot",
    "time.source": "2020-10-13T00:00:00+00:00"
}
EXAMPLE_INPUT_PASS_3 = {
    "__type": "Event",
    "feed.accuracy": 90.0,
    "feed.name": "Feodo Tracker IPs",
    "feed.provider": "abuse.ch",
    "feed.url": "https://feodotracker.abuse.ch/downloads/ipblocklist.csv",
    "time.observation": "2020-10-13T06:14:49+00:00",
    "raw": "dGVzdA==",
    "extra.firstseen": "2020-10-11T02:10:59+00:00",
    "source.port": 447,
    "extra.lastonline": "2020-09-13",
    "malware.name": "trickbot",
    "time.source": "2020-10-13T00:00:00+00:00"
}


@test.skip_exotic()
class TestFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TimeFilterExpertBot handling Reports.
    """

    @classmethod
    def init(cls):
        if freeze_time is None:
            raise MissingDependencyError("freeze_time")

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TimeFilterExpertBot
        cls.input_message = EXAMPLE_INPUT_DROP
        cls.sysconfig = {
            'search_field': 'extra.lastonline',
            'search_from': "1d"
        }

    @test.skip_exotic()
    @freeze_time("2021-05-05")
    def test_expert_drop(self):
        self.run_bot()
        self.assertOutputQueueLen(0)

    @test.skip_exotic()
    @freeze_time("2020-09-09")
    def test_expert_pass(self):
        self.input_message = EXAMPLE_INPUT_PASS
        self.run_bot()
        self.assertOutputQueueLen(1)

    @test.skip_exotic()
    @freeze_time("2020-09-09")
    def test_expert_pass_2(self):
        self.input_message = EXAMPLE_INPUT_PASS_2
        self.run_bot()
        self.assertOutputQueueLen(1)

    @test.skip_exotic()
    @freeze_time("2020-09-09")
    def test_expert_pass_3(self):
        self.input_message = EXAMPLE_INPUT_PASS_3
        self.run_bot()
        self.assertOutputQueueLen(1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
