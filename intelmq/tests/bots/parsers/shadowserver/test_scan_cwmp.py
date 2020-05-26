# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_cwmp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible CWMP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2018-07-30T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_cwmp-test-test.csv",

                  }
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'Accessible CWMP',
    "classification.identifier": "open-cwmp",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.connection": "keep-alive",
    "extra.content_length": 5678,
    "extra.content_type": "text/html",
    "extra.date": "Wed, 04 Sep 2019 07:42:37 GMT",
    "extra.http": "HTTP/1.1",
    "extra.http_code": 200,
    "extra.http_reason": "OK",
    "extra.naics": 517311,
    "extra.server": "DNVRS-Webs",
    "extra.tag": "cwmp",
    "protocol.application": "cwmp",
    "protocol.transport": "tcp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
    "source.asn": 5678,
    "source.geolocation.cc": "AA",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.123.245.142",
    "source.port": 30005,
    "time.observation": "2018-07-30T00:00:00+00:00",
    "time.source": "2019-09-04T10:44:55+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Accessible CWMP',
    "classification.identifier": "open-cwmp",
    "classification.taxonomy": "vulnerable",
    "classification.type": "vulnerable service",
    "extra.content_type": "text/html",
    "extra.http": "HTTP/1.1",
    "extra.http_code": 404,
    "extra.http_reason": "Not Found",
    "extra.naics": 517311,
    "extra.server": "RomPager/4.07 UPnP/1.0",
    "extra.tag": "cwmp",
    "extra.transfer_encoding": "chunked",
    "protocol.application": "cwmp",
    "protocol.transport": "tcp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
    "source.asn": 5678,
    "source.geolocation.cc": "AA",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.123.245.162",
    "source.port": 5678,
    "source.reverse_dns": "localhost.localdomain",
    "time.observation": "2018-07-30T00:00:00+00:00",
    "time.source": "2019-09-04T11:06:50+00:00"
    },]


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
