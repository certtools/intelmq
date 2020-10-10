# -*- coding: utf-8 -*-

import unittest
import time

import intelmq.lib.test as test
from intelmq.lib import utils
from intelmq.bots.experts.threshold.expert import ThresholdExpertBot

EVENT_PATTERN = {
    'feed.url': 'file://localhost/test',
    'feed.name': 'Threshold expert test',
    '__type': 'Event',
    'raw': utils.base64_encode('test'),
    'time.observation': '2020-09-11T10:40:18+02:00',
    'source.ip': '192.0.2.0',
    'classification.type': 'test'
}

EVENTS_IN = []
for i in range(30):
    EVENTS_IN += [{**EVENT_PATTERN,
                   **{'destination.ip': '192.0.2.%d' % i}}]
EVENTS_OUT = [msg.copy() for msg in EVENTS_IN]
for msg in EVENTS_OUT:
    msg['extra.count'] = 10


PARAMETERS = {
    'filter_keys': ['source.ip'],
    'filter_type': 'whitelist',
    'redis_cache_db': '11',
    'redis_cache_host': '127.0.0.1',
    'redis_cache_password': None,
    'redis_cache_port': '6379',
    'timeout': 1,
    'threshold': 10
}


@test.skip_redis()
class TestThresholdExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A test case for ThresholdExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ThresholdExpertBot
        cls.use_cache = True

    def test_one(self):
        """
        One message, not enough to reach the threshold.
        """
        time.sleep(2)  # Ensure cache has timed out
        self.input_message = EVENTS_IN[0:1]
        self.run_bot(parameters=PARAMETERS,
                     iterations=len(self.input_message))
        self.assertOutputQueueLen(0)

    def test_threshold_reached(self):
        """
        Ten messages, just enough to reach the threshold.
        """
        time.sleep(2)  # Ensure cache has timed out
        self.input_message = EVENTS_IN[0:10]
        self.run_bot(parameters=PARAMETERS,
                     iterations=len(self.input_message))
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, EVENTS_OUT[PARAMETERS['threshold'] - 1])

    def test_differing_messages(self):
        """
        Thirty messages, looking at fields that differ.
        """
        time.sleep(2)  # Ensure cache has timed out
        self.input_message = EVENTS_IN
        self.run_bot(parameters={**PARAMETERS,
                                 **{'filter_keys':
                                    ['source.ip', 'destination.ip']}},
                     iterations=len(self.input_message))
        self.assertOutputQueueLen(0)

    def test_threshold_exceeded(self):
        """
        Thirty identical messages, within the timeout period.
        """
        time.sleep(2)  # Ensure cache has timed out
        self.input_message = EVENTS_IN
        self.run_bot(parameters=PARAMETERS,
                     iterations=len(self.input_message))
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, EVENTS_OUT[PARAMETERS['threshold'] - 1])

    def test_add_field(self):
        """
        Add a field to the propagated event.
        """
        time.sleep(2)  # Ensure cache has timed out
        self.input_message = EVENTS_IN[0:10]
        self.run_bot(parameters={**PARAMETERS,
                                 **{'add_keys':
                                    {'comment':
                                     'Threshold reached'}}},
                     iterations=len(self.input_message))
        self.assertOutputQueueLen(1)
        self.assertMessageEqual(0, {**EVENTS_OUT[PARAMETERS['threshold'] - 1],
                                    **{'comment': 'Threshold reached'}})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
