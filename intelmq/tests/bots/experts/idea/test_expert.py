#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import json

import intelmq.lib.test as test
from intelmq.bots.experts.idea.expert import IdeaExpertBot
from intelmq.lib.harmonization import ClassificationType


TEST_INPUT1 = {
    "__type": "Event",
    "classification.type": "malware",
    "destination.ip": "2001:DB8::BB2B:F258",
    "destination.port": 22,
    "event_description.target": "DHL",
    "event_description.text": "Angler EK",
    "event_description.url": "http://www.phishtank.com/phish_detail.php?phish_id=3989866",
    "feed.accuracy": 100.0,
    "feed.name": "Malware Domain List",
    "feed.url": "http://www.malwaredomainlist.com/updatescsv.php",
    "misp.event_uuid": "81494d6a-0341-11e7-a0ef-002564d9514f",
    "protocol.application": "ssh",
    "protocol.transport": "tcp",
    "raw": "MjAxNi8wNC8yMF8xNDoyOCx3Yzl1ai5scnZhMzJ4d2QudG9wL1NIbnhCZEUtck1UWWZwLUNTaHIvVktkdGstOTgz"
           "LUVqcUovLDE4NS4xNDEuMjUuNjAsLSxBbmdsZXIgRUssUmVnaXN0cmFudCBtYXlrb2VAbGlzdC5ydSw2MDExNw==",
    "source.as_name": "PURDUE - Purdue University, US",
    "source.asn": 60117,
    "source.ip": "185.141.25.60",
    "source.network": "0.0.0.0/8",
    "source.reverse_dns": "customer.worldstream.nl",
    "source.url": "http://wc9uj.lrva32xwd.top/SHnxBdE-rMTYfp-CShr/VKdtk-983-EjqJ/",
    "time.observation": "2016-04-20T19:02:35+00:00",
    "time.source": "2016-04-20T14:28:00+00:00",
}

TEST_OUTPUT1 = {
    "Format": "IDEA0",
    "ID": "83561c71-7d01-460b-87ee-0e52de012d4a",
    "Description": "Malware Domain List: Angler EK",
    "Category": ["Malware"],
    "DetectTime": "2016-04-20T19:02:35+00:00",
    "EventTime": "2016-04-20T14:28:00+00:00",
    "Confidence": 1,
    "Ref": ["http://www.phishtank.com/phish_detail.php?phish_id=3989866", "misp_event:81494d6a-0341-11e7-a0ef-002564d9514f"],
    "Target": [
        {
            "IP6": ["2001:DB8::BB2B:F258"],
            "Port": [22],
            "Proto": ["tcp", "ssh"]
        }
    ],
    "Source": [
        {
            "URL": ["http://wc9uj.lrva32xwd.top/SHnxBdE-rMTYfp-CShr/VKdtk-983-EjqJ/"],
            "ASN": [60117],
            "PTR": ["customer.worldstream.nl"],
            "IP4": ["185.141.25.60"],
            "Proto": ["tcp", "ssh"]
        }
    ],
    "Attach": [
        {
            "Content": "2016/04/20_14:28,wc9uj.lrva32xwd.top/SHnxBdE-rMTYfp-CShr/VKdtk-98"
                       "3-EjqJ/,185.141.25.60,-,Angler EK,Registrant maykoe@list.ru,60117",
            "Type": ["OrigData"],
            "Ref": ["http://www.malwaredomainlist.com/updatescsv.php"]
        }
    ]
}


class TestIdeaExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = IdeaExpertBot
        cls.sysconfig = {"test_mode": False}

    def test_conversion(self):
        self.input_message = TEST_INPUT1
        self.run_bot()
        # The ID in the generated Idea event is random, so we have to extract
        # the data from the "output" field and compare after removing ID's
        event = self.get_output_queue()[0]
        self.assertIsInstance(event, str)
        event_dict = json.loads(event)
        self.assertIsInstance(event_dict, dict)
        self.assertTrue("output" in event_dict)
        idea_event = json.loads(event_dict["output"])
        self.assertIsInstance(idea_event, dict)
        del TEST_OUTPUT1["ID"]
        del idea_event["ID"]
        self.assertDictEqual(TEST_OUTPUT1, idea_event)


class TestHarmonization(unittest.TestCase):

    def test_classification_coverage(self):
        intelmq_harmonization = set(ClassificationType.allowed_values)
        idea_expert = set(IdeaExpertBot.type_to_category.keys())
        self.assertSetEqual(intelmq_harmonization, idea_expert)


if __name__ == '__main__':
    unittest.main()
