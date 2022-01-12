# -*- coding: utf-8 -*-
"""
Testing event aggregation

SPDX-FileCopyrightText: 2021 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from datetime import datetime, timedelta
import json
import unittest
import os
from unittest import TestCase
from intelmq.lib.exceptions import MissingDependencyError

try:
    import time_machine
except ImportError:
    time_machine = None

import intelmq.lib.test as test
from intelmq.bots.experts.aggregate.expert import AggregateExpertBot

EXAMPLE_OUTPUT = {'__type': 'Event',
                    'classification.identifier': 'ddos',
                    'classification.type': 'ddos',
                    'destination.ip': '192.0.43.8',
                    'extra.count': 25,
                    'extra.time_end': '2015-01-01T00:59:00+00:00',
                    'source.ip': '192.88.99.28'}


@test.skip_exotic()
class TestAggregateExpertBot(test.BotTestCase, TestCase):
    """
    A TestCase for AggregateExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AggregateExpertBot
        cls.use_cache = True

    def test_cache(self):
        if time_machine is None:
            raise MissingDependencyError("time_machine")
        EVENTS = []
        with open(os.path.join(os.path.dirname(__file__), 'testdata', 'events.txt'), 'rb') as f:
            for line in f.readlines():
                EVENTS.append(json.loads(line))

        self.input_message = EVENTS[0:25]
        self.run_bot(iterations=25, stop_bot=False)

        # forwarding time +1 hour 1 minute
        dt_new = datetime.now() + timedelta(hours=1, minutes=30)
        traveller = time_machine.travel(dt_new.timestamp())
        traveller.start()
        self.input_message = EVENTS[0:25]
        self.prepare_source_queue()
        self.run_bot(iterations=25, prepare=False)
        traveller.stop()

        EXAMPLE_OUTPUT['time.source'] = json.loads(self.get_output_queue()[0])["time.source"]
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
