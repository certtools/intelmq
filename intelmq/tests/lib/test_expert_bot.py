import unittest

import intelmq.lib.test as test
from intelmq.lib.bot import Bot

EXAMPLE = {'feed.name': 'Test', "__type": "Report"}
QUEUES = {"_default", "other-way", "two-way"}

class DummyExpertBot(Bot):

    def process(self):
        event = self.receive_message()
        self.send_message(event, path=event['feed.code'] if 'feed.code' in event else "_default")
        self.acknowledge_message()


class TestDummyExpertBot(test.BotTestCase, unittest.TestCase):
    """ Testing generic functionalities of Bot base class. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyExpertBot
        cls.default_input_message = EXAMPLE.copy()
        cls.allowed_error_count = 1

    def test_pipeline_default(self):
        self.input_message = EXAMPLE
        self.prepare_bot(destination_queues=QUEUES)
        self.run_bot(prepare=False)
        self.assertMessageEqual(0, EXAMPLE)

    def test_pipeline_other(self):
        input_message = EXAMPLE.copy()
        input_message["feed.code"] = "other-way"
        self.input_message = input_message
        self.prepare_bot(destination_queues=QUEUES)
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, path="_default")
        self.assertMessageEqual(0, input_message, path="other-way")

    def test_pipeline_multiple(self):
        input_message = EXAMPLE.copy()
        input_message["feed.code"] = "two-way"
        self.input_message = input_message
        self.prepare_bot(destination_queues=QUEUES)
        self.run_bot(prepare=False)
        self.assertOutputQueueLen(0, path="_default")
        self.assertOutputQueueLen(0, path="other-way")
        self.assertMessageEqual(0, input_message, path="two-way")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
