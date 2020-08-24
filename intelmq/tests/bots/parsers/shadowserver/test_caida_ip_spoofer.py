import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), "testdata/caida_ip_spoofer.csv")) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    "feed.name": "CAIDA",
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2020-08-19T00:00:00+00:00",
    "extra.file_name": "2020-08-19-caida_ip_spoofer-test.csv",
}

EVENTS = [
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2019-08-27T00:06:24+00:00",
        "source.ip": "137.97.71.0",

        "source.asn": 55836,

        "source.geolocation.cc": "IN",
        "source.geolocation.region": "KERALA",
        "source.geolocation.city": "THRISSUR",
        "extra.type": "Session",
        "extra.naics": 517312,
        "extra.sic": 0,
        "extra.sector": "Information Technology",
        "source.network": "137.97.71.0/24",
        "extra.routedspoof": "received",
        "extra.session": 739969,
        "extra.nat": True,
        "extra.public_source": "caida",

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[1]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2019-08-27T01:19:47+00:00",
        "source.ip": "103.95.33.0",

        "source.asn": 136749,

        "source.geolocation.cc": "MY",
        "source.geolocation.region": "SELANGOR",
        "source.geolocation.city": "SHAH ALAM",
        "extra.type": "Session",
        "extra.naics": 541990,
        "extra.sic": 0,
        "extra.sector": "Communications",
        "source.network": "103.95.33.0/24",
        "extra.routedspoof": "received",
        "extra.session": 739992,
        "extra.nat": True,
        "extra.public_source": "caida",

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[2]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2019-08-27T02:32:12+00:00",
        "source.ip": "115.78.9.0",

        "source.asn": 7552,

        "source.geolocation.cc": "VN",
        "source.geolocation.region": "HO CHI MINH",
        "source.geolocation.city": "THANH PHO HO CHI MINH",
        "extra.type": "Session",
        "extra.naics": 517312,
        "extra.sic": 0,
        "extra.sector": "Communications",
        "source.network": "115.78.9.0/24",
        "extra.routedspoof": "rewritten",
        "extra.session": 740024,
        "extra.nat": True,
        "extra.public_source": "caida",

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[3]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2019-08-27T03:16:08+00:00",
        "source.ip": "24.237.163.0",

        "source.asn": 8047,
        "source.reverse_dns": "0-163-237-24.gci.net",

        "source.geolocation.cc": "US",
        "source.geolocation.region": "ALASKA",
        "source.geolocation.city": "BETHEL",
        "extra.type": "Session",
        "extra.naics": 517919,
        "extra.sic": 737415,
        "source.network": "24.237.163.0/24",
        "extra.routedspoof": "received",
        "extra.session": 740037,
        "extra.nat": False,
        "extra.public_source": "caida",

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[4]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2019-08-27T04:29:49+00:00",
        "source.ip": "122.255.35.0",

        "source.asn": 18001,

        "extra.type": "Session",
        "source.network": "122.255.35.0/24",
        "extra.routedspoof": "received",
        "extra.session": 740057,
        "extra.nat": False,
        "extra.public_source": "caida",

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[5]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
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
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == "__main__":
    unittest.main()
