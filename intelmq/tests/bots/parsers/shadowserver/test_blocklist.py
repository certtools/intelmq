# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/blocklist.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    'feed.name': 'Blocklist',
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "extra.file_name": "2019-01-01-blocklist-test-geo.csv",
}
EVENTS = [{
    '__type': 'Event',
    'feed.name': 'Blocklist',
    "classification.identifier": "blacklisted-ip",
    "classification.taxonomy": "other",
    "classification.type": "blacklist",
    "extra.naics": 517311,
    "extra.reason": "Malicious Host AA",
    "extra.source": "Alien Vault",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
    "source.asn": 5678,
    "source.geolocation.cc": "XX",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.123.245.134",
    "source.reverse_dns": "host.local",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "time.source": "2019-09-04T07:00:19+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Blocklist',
    "classification.identifier": "blacklisted-ip",
    "classification.taxonomy": "other",
    "classification.type": "blacklist",
    "extra.naics": 517311,
    "extra.reason": "Malicious Host AA",
    "extra.source": "Alien Vault",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                         EXAMPLE_LINES[2]])),
    "source.asn": 5678,
    "source.geolocation.cc": "XX",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.ip": "198.123.245.171",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "time.source": "2019-09-04T07:00:19+00:00"
},
{
    '__type': 'Event',
    'feed.name': 'Blocklist',
    "classification.identifier": "blacklisted-ip",
    "classification.taxonomy": "other",
    "classification.type": "blacklist",
    "extra.naics": 517311,
    "extra.reason": "Malicious Host AA",
    "extra.source": "Alien Vault",
    'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                         EXAMPLE_LINES[3]])),
    "source.asn": 5678,
    "source.geolocation.cc": "XX",
    "source.geolocation.city": "LOCATION",
    "source.geolocation.region": "LOCATION",
    "source.network": "198.123.245.0/24",
    "time.observation": "2015-01-01T00:00:00+00:00",
    "time.source": "2019-09-04T07:00:19+00:00"
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
