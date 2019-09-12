# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/botnet_drone.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    'feed.name': 'Drone',
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.file_name": "2019-01-01-botnet_drone-test-geo.csv",
}
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'Drone',
    "classification.taxonomy": "malicious code",
    "classification.type": "infected-system",
    "destination.asn": 8560,
    "destination.geolocation.cc": "US",
    "destination.ip": "74.208.164.166",
    "destination.port": 80,
    "extra.connection_count": 1,
    "extra.family": "dorkbot",
    "extra.naics": 541690,
    "extra.os.name": "Windows",
    "extra.os.version": "2000 SP4, XP SP1+",
    "extra.public_source": "AnubisNetworks",
    "extra.sic": 874899,
    "extra.tag": "sinkhole",
    "malware.name": "dorkbot",
    "protocol.transport": "tcp",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
    "source.asn": 7543,
    "source.geolocation.cc": "AU",
    "source.geolocation.city": "MELBOURNE",
    "source.geolocation.region": "VICTORIA",
    "source.ip": "210.23.139.130",
    "source.port": 3218,
    "time.observation": "2015-01-01T00:00:00+00:00",
    "time.source": "2011-04-23T00:00:05+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Drone',
    "classification.taxonomy": "malicious code",
    "classification.type": "infected-system",
    "destination.asn": 16265,
    "destination.fqdn": "015.example.com",
    "destination.geolocation.cc": "NL",
    "destination.ip": "94.75.228.147",
    "extra.connection_count": 1,
    "extra.destination.naics": 517510,
    "extra.destination.sector": "Commercial Facilities",
    "extra.destination.sic": 737415,
    "extra.os.name": "WINXP",
    "malware.name": "spyeye",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                         EXAMPLE_LINES[2]])),
    "source.asn": 9556,
    "source.geolocation.cc": "AU",
    "source.geolocation.city": "ADELAIDE",
    "source.geolocation.region": "SOUTH AUSTRALIA",
    "source.ip": "115.166.54.44",
    "source.reverse_dns": "115-166-54-44.ip.adam.com.au",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "time.source": "2011-04-23T00:00:08+00:00"
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
