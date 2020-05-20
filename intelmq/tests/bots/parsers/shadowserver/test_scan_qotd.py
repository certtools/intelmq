# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/scan_qotd.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open QOTD',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_qotd-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open QOTD',
           'classification.identifier': 'open-qotd',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.quote': 'N?s matamos o tempo, mas ele enterra-nos.?? (Machado de Assis)??',
           'extra.tag': 'qotd',
           'extra.sic': 654321,
           'extra.naics': 123456,
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 53006,
           'source.geolocation.cc': 'BR',
           'source.geolocation.city': 'UBERLANDIA',
           'source.geolocation.region': 'MINAS GERAIS',
           'source.ip': '179.126.2.38',
           'source.port': 17,
           'source.reverse_dns': '179-126-002-038.xd-dynamic.ctbcnetsuper.com.br',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:33+00:00'},
          {'__type': 'Event',
           'feed.name': 'Open QOTD',
           'classification.identifier': 'open-qotd',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.tag': 'qotd',
           'extra.quote': 'When a stupid man is doing something he is ashamed of, he always declares?? that it is his duty. George Bernard Shaw (1856-1950)??',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 3786,
           'source.geolocation.cc': 'KR',
           'source.geolocation.city': 'SEOUL',
           'source.geolocation.region': "SEOUL-T'UKPYOLSI",
           'source.ip': '123.140.149.131',
           'source.port': 17,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:33+00:00'},
          {'__type': 'Event',
           'feed.name': 'Open QOTD',
           'classification.identifier': 'open-qotd',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.quote': '_The secret of being miserable is to have leisure to bother about whether?? you are happy or not.  The cure for it is occupation._?? George Bernard Shaw (1856-1950)??',
           'extra.tag': 'qotd',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'source.asn': 8560,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'WAYNE',
           'source.geolocation.region': 'PENNSYLVANIA',
           'source.ip': '74.208.209.45',
           'source.port': 17,
           'source.reverse_dns': 'u15169732.onlinehome-server.com',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:34+00:00'},
          {'__type': 'Event',
           'feed.name': 'Open QOTD',
           'classification.identifier': 'open-qotd',
           'classification.taxonomy': 'vulnerable',
           'classification.type': 'vulnerable service',
           'extra.tag': 'qotd',
           'extra.quote': '_We have no more right to consume happiness without producing it than to?? consume wealth without producing it._ George Bernard Shaw (1856-1950)??',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[4]])),
           'source.asn': 15003,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'PHOENIX',
           'source.geolocation.region': 'ARIZONA',
           'source.ip': '23.19.41.218',
           'source.port': 17,
           'source.reverse_dns': '23.19.41.218.rdns.ubiquity.io',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:34+00:00'}]


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
