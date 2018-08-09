# -*- coding: utf-8 -*-
from intelmq.bots.experts.custom_filter.expert import CustomFilterExpertBot
import intelmq.lib.test as test
import unittest
import os
import inspect

EXAMPLE_MESSAGE = {
                  "__type": "Event",
                  "source.ip": "10.0.0.1",
                  "feed.name": "good-feed",                  
                  "time.source": "2015-06-04T13:37:00+00:00",
                  "feed.url": "http://www.example.com/",
                  "source.reverse_dns": "reverse.example.net",
                  "source.url": "http://example.org",
                  "time.observation": "2015-08-11T13:03:40+00:00",
                  "raw": "MjAxNS8wNi8wNF8xMzozNyxleGFtcGxlLm9yZywxOTIuMC4yLjMs"
                         "cmV2ZXJzZS5leGFtcGxlLm5ldCxleGFtcGxlIGRlc2NyaXB0aW9u"
                         "LHJlcG9ydEBleGFtcGxlLm9yZywwMDAwMAo=",                  
                  "classification.type": "malware",
                  "event_description.text": "example description",
                  "source.abuse_contact": "good-mail@example.com",
                  "source.asn": 00000
                  }

class TestCustomFilterExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CustomFilterExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = CustomFilterExpertBot
        self.default_input_message = {'__type': 'Report'}        
        self.sysconfig = {'rules_dir': os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"}
            
    def test_filter_pass(self):
        """ Test if certain messages pass filter. """
        msg = self.input_message = EXAMPLE_MESSAGE.copy()
        self.run_bot()
        self.assertMessageEqual(0, msg)

    def test_filter_out(self):
        """ Test if certain messages do not pass filter. """
        self.input_message = EXAMPLE_MESSAGE.copy()
        self.input_message["feed.name"] = "bad-feed"        
        self.run_bot()
        self.assertOutputQueueLen(0)
        
    def test_filter_masked_ip_excluded(self):
        """ Test if certain messages are excluded by a filter defining network mask. """
        self.input_message = EXAMPLE_MESSAGE.copy()
        self.input_message["source.ip"] = "10.0.1.3"
        self.run_bot()
        self.assertOutputQueueLen(0)
        
    def test_filter_static_ip_exluded(self):
        """ Test if certain messages are excluded by a filter defining network mask. """
        self.input_message = EXAMPLE_MESSAGE.copy()
        self.input_message["source.ip"] = "10.0.2.2"
        self.run_bot()
        self.assertOutputQueueLen(0)
        
    def test_filter_static_ip_passed(self):
        """ Test if certain messages are excluded by a filter defining network mask. """
        msg = self.input_message = EXAMPLE_MESSAGE.copy()
        self.input_message["source.ip"] = "10.0.2.3"
        self.run_bot()
        self.assertMessageEqual(0, msg)

if __name__ == '__main__':
    unittest.main()
