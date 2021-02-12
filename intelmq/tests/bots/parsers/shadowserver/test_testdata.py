# -*- coding: utf-8 -*-

import csv
import json
import os
import os.path
import unittest
import pathlib

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot
from intelmq.bots.parsers.shadowserver.parser_json import ShadowserverJSONParserBot

def csvtojson(csvfile):
    datalist = []

    with open(csvfile, 'r') as fop:
        reader = csv.DictReader(fop, restval="")

        for row in reader:
            datalist.append(row)

    return json.dumps(datalist, indent=4)

CSVREPORTS = {}
JSONREPORTS = {}
testdata = pathlib.Path(__file__).parent / 'testdata'
for filename in testdata.glob('*.csv'):
    EXAMPLE_FILE = filename.read_text()
    shortname = filename.stem
    CSVREPORTS[shortname] = {"raw": utils.base64_encode(EXAMPLE_FILE),
                          "__type": "Report",
                          "time.observation": "2015-01-01T00:00:00+00:00",
                          "extra.file_name": "2019-01-01-{}-test-test.csv".format(shortname),
                          }
    JSONREPORTS[shortname] = {"raw": utils.base64_encode(csvtojson(filename)),
                          "__type": "Report",
                          "time.observation": "2015-01-01T00:00:00+00:00",
                          "extra.file_name": "2019-01-01-{}-test-test.csv".format(shortname),
                          }


def generate_feed_function(feedname, reports):
    def test_feed(self):
        """ Test if no errors happen for feed %s. """ % feedname
        self.input_message = reports[feedname]
        self.run_bot()
    return test_feed


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot

class TestShadowserverJSONParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverJSONParserBot

for key in CSVREPORTS:
    setattr(TestShadowserverParserBot, 'test_feed_%s' % key, generate_feed_function(key, CSVREPORTS))
for key in JSONREPORTS:
    setattr(TestShadowserverJSONParserBot, 'test_feed_%s' % key, generate_feed_function(key, JSONREPORTS))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
