# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_mongodb.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open MongoDB',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_mongodb-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open MongoDB',
           "classification.identifier": "open-mongodb",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.allocator": "tcmalloc",
           "extra.bits": "64",
           "extra.gitversion": "a2ddc68ba7c9cee17bfe69ed840383ec3506602b",
           "extra.javascriptengine": "V8",
           "extra.maxbsonobjectsize": "16777216",
           "extra.ok": "1",
           "extra.sysinfo": "Linux ip-198-51-100-100 198.51.100.103-2.ec2.v1.2.fc8xen #1 SMP Fri Nov 20 17:48:28 EST 2009 x86_64 BOOST_LIB_VERSION=1_49",
           "extra.tag": "mongodb",
           "extra.version": "2.4.5",
           "extra.visible_databases": "local | countly | admin",
           "protocol.application": "mongodb",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 20773,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "WEEZE",
           "source.geolocation.region": "NORDRHEIN-WESTFALEN",
           "source.ip": "198.51.100.203",
           "source.port": 27017,
           "source.reverse_dns": "198-51-100-203.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:40:07+00:00"
           },
           {'__type': 'Event',
           'feed.name': 'Open MongoDB',
           "classification.identifier": "open-mongodb",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.allocator": "tcmalloc",
           "extra.bits": "64",
           "extra.gitversion": "d73c92b1c85703828b55c2916a5dd4ad46535f6a",
           "extra.javascriptengine": "V8",
           "extra.maxbsonobjectsize": "16777216",
           "extra.ok": "1",
           "extra.sector": "Information Technology",
           "extra.sysinfo": "Linux build5.ny.cbi.10gen.cc 2.6.32-431.3.1.el6.x86_64 #1 SMP Fri Jan 3 21:39:27 UTC 2014 x86_64 BOOST_LIB_VERSION=1_49",
           "extra.tag": "mongodb",
           "extra.version": "2.6.12",
           "extra.visible_databases": "none visible",
           "protocol.application": "mongodb",
           "protocol.transport": "tcp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 24940,
           "source.geolocation.cc": "DE",
           "source.geolocation.city": "GUNZENHAUSEN",
           "source.geolocation.region": "BAYERN",
           "source.ip": "198.51.100.42",
           "source.port": 27017,
           "source.reverse_dns": "198-51-100-208.example.net",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2016-07-24T00:40:07+00:00"
           },
          ]

class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
