# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from intelmq.bots.experts.custom_filter.expert import CustomFilterExpertBot
import intelmq.lib.test as test
import unittest
import os
import inspect

EXAMPLE_FILTER_PASS = {"source.ip": "192.0.2.3",
                  "time.source": "2015-06-04T13:37:00+00:00",
                  "feed.url": "http://www.example.com/",
                  "source.reverse_dns": "reverse.example.net",
                  "source.url": "http://example.org",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": "MjAxNS8wNi8wNF8xMzozNyxleGFtcGxlLm9yZywxOTIuMC4yLjMs"
                         "cmV2ZXJzZS5leGFtcGxlLm5ldCxleGFtcGxlIGRlc2NyaXB0aW9u"
                         "LHJlcG9ydEBleGFtcGxlLm9yZywwMDAwMAo=",
                  "__type": "Report",
                  "classification.type": "malware",
                  "event_description.text": "example description",
                  "source.asn": 00000,
                  "feed.name": "Example"}
EXAMPLE_FILTER_OUT = {"source.ip": "192.0.2.3",
                  "time.source": "2015-06-04T13:37:00+00:00",
                  "feed.url": "http://www.example.com/",
                  "source.reverse_dns": "reverse.example.net",
                  "source.url": "http://example.org",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": "MjAxNS8wNi8wNF8xMzozNyxleGFtcGxlLm9yZywxOTIuMC4yLjMs"
                         "cmV2ZXJzZS5leGFtcGxlLm5ldCxleGFtcGxlIGRlc2NyaXB0aW9u"
                         "LHJlcG9ydEBleGFtcGxlLm9yZywwMDAwMAo=",
                  "__type": "Report",
                  "classification.type": "malware",
                  "event_description.text": "example description",
                  "source.asn": 00000,
                  "feed.name": "Example",
                  "Recipient": "robert.sefr@nic.cz"}



class TestCustomFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CustomFilterExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CustomFilterExpertBot
        self.default_input_message = {'__type': 'Report'}
        
        self.sysconfig = {'rules_dir': os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"}
        

    def test_filter_out(self):
        """ Test if certain messages do not pass filter. """
        self.input_message = EXAMPLE_FILTER_OUT
        self.run_bot()
        self.assertOutputQueueLen(0)
        #self.assertMessageEqual(0, EXAMPLE_ROBERT)

    def test_filter_pass(self):
        """ Test if certain messages pass filter. """
        self.input_message = EXAMPLE_FILTER_PASS
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_FILTER_PASS)


if __name__ == '__main__':
    unittest.main()
