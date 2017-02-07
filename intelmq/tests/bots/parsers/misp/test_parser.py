# -*- coding: utf-8 -*-

import os
import unittest

from intelmq.bots.parsers.misp.parser import MISPParserBot
from intelmq.lib import test
from intelmq.lib.utils import base64_encode

with open(os.path.join(os.path.dirname(__file__), 'misp_event.json')) as handle:
    EXAMPLE_MISP_EVENT = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'misp_attribute.json')) as handle:
    EXAMPLE_MISP_ATTR = handle.read()

EXAMPLE_REPORT = {
    "__type": "Report",
    "feed.accuracy": 100.0,
    "feed.name": "misp_test",
    "feed.url": "http://192.168.56.102/",
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": base64_encode(EXAMPLE_MISP_EVENT)
}

EXAMPLE_EVENT = {
    "__type": "Event",
    "feed.accuracy": 100.0,
    "feed.name": "misp_test",
    "feed.url": "http://192.168.56.102/",
    "time.observation": "2016-06-15T09:25:26+00:00",
    "time.source": "2016-06-11T21:41:44+00:00",
    "source.url": "http://fake.website.com/malware/is/here",
    "event_description.text": "Payload delivery",
    "event_description.url": "http://192.168.56.102/event/view/2",
    "classification.type": "ransomware",
    "malware.name": "locky",
    'misp.attribute_uuid': '575c8598-f1f0-4c16-a94a-0612c0a83866',
    'misp.event_uuid': '5758ebf5-c898-48e6-9fe9-5665c0a83866',
    "raw": base64_encode(EXAMPLE_MISP_ATTR)
}


class TestMISPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for the MISPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MISPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
