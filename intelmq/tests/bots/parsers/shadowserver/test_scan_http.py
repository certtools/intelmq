# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_http.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible HTTP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-03-25-scan_http-test-test.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Accessible HTTP',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'classification.identifier': 'accessible-http',
           'extra.naics': 518111,
           'extra.sic': 737401,
           'extra.http': 'HTTP/1.1',
           'extra.http_code': 200,
           'extra.http_reason': 'OK',
           'extra.content_type': 'text/html',
           'extra.server': 'lighttpd',
           'extra.transfer_encoding': 'chunked',
           'extra.http_date': '2018-04-19T00:02:28+00:00',
           'extra.tag': 'http',
					 'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.reverse_dns': 'c-75-74-78-113.hsd1.fl.comcast.net',
           'source.asn': 7922,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'MIAMI',
           'source.geolocation.region': 'FLORIDA',
           'source.ip': '75.74.78.113',
           'source.port': 8080,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2018-04-19T00:02:26+00:00'},
          {'__type': 'Event',
           'feed.name': 'Accessible HTTP',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'classification.identifier': 'accessible-http',
           'extra.naics': 518210,
           'extra.sic': 737415,
           'extra.http': 'HTTP/1.1',
           'extra.http_code': 200,
           'extra.http_reason': 'OK',
           'extra.content_type': 'text/html',
           'extra.content_length': 17729,
           'extra.http_date': '2018-04-19T02:02:28+00:00',
           'extra.tag': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.reverse_dns': 'sto95-3-88-162-174-130.fbx.proxad.net',
           'source.asn': 12322,
           'source.geolocation.cc': 'FR',
           'source.geolocation.city': 'SAINT-OUEN-LAUMONE',
           'source.ip': '88.162.174.130',
           'source.port': 8080,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2018-04-19T00:02:26+00:00'},
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
