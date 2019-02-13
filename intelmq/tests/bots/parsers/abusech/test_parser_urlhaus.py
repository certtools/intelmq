# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_urlhaus import URLhausParserBot

with open(os.path.join(os.path.dirname(__file__), 'urlhaus.txt')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {
    'feed.url': 'https://urlhaus.abuse.ch/feeds/tld/CH/',
    'feed.name': 'AbuseCH URLhaus',
    '__type': 'Report',
    'raw': utils.base64_encode(EXAMPLE_FILE),
    'time.observation': '2019-02-13T13:11:44+00:00'
}

EXAMPLE_EVENTS = [
    {
        '__type': 'Event',
        'feed.url': 'https://urlhaus.abuse.ch/feeds/tld/CH/',
        'feed.name': 'AbuseCH URLhaus',
        'time.observation': '2019-02-13T13:11:44+00:00',
        'time.source': '2019-02-13T00:34:42+00:00',
        'source.url': 'http://marconuenlist.ch/verif.accounts.docs.net/',
        'source.fqdn': 'marconuenlist.ch',
        'extra.status': 'offline',
        'classification.identifier': 'malware_download',
        'source.ip': '62.241.37.242',
        'source.asn': 29083,
        'source.geolocation.cc': 'DE',
        'classification.type': 'malware',
        'raw': 'MjAxOS0wMi0xMyAwMDozNDo0MixodHRwOi8vbWFyY29udWVubGlzdC5jaC92ZXJpZi5hY2NvdW50cy5kb2NzLm5ldC8sb2ZmbGluZSx'
               'tYWx3YXJlX2Rvd25sb2FkLG1hcmNvbnVlbmxpc3QuY2gsNjIuMjQxLjM3LjI0MiwyOTA4MyxERQ0K'
    },
    {
        '__type': 'Event',
        'feed.url': 'https://urlhaus.abuse.ch/feeds/tld/CH/',
        'feed.name': 'AbuseCH URLhaus',
        'time.observation': '2019-02-13T13:11:44+00:00',
        'time.source': '2019-02-12T14:27:03+00:00',
        'source.url': 'http://cbd-planet.ch/sec.myacc.send.com/',
        'source.fqdn': 'cbd-planet.ch',
        'extra.status': 'online',
        'classification.identifier': 'malware_download',
        'source.ip': '83.166.138.63',
        'source.asn': 29222,
        'source.geolocation.cc': 'CH',
        'classification.type': 'malware',
        'raw': 'MjAxOS0wMi0xMiAxNDoyNzowMyxodHRwOi8vY2JkLXBsYW5ldC5jaC9zZWMubXlhY2Muc2VuZC5jb20vLG9ubGluZSxtYWx3YXJlX2R'
               'vd25sb2FkLGNiZC1wbGFuZXQuY2gsODMuMTY2LjEzOC42MywyOTIyMixDSA0K'
    }
]


class TestURLhausParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLhausParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event1(self):
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENTS[0])

    def test_event2(self):
        self.run_bot()
        self.assertMessageEqual(1, EXAMPLE_EVENTS[1])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
