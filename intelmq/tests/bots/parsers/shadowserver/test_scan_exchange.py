# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), "testdata/scan_exchange.csv")) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    "feed.name": "Shadowserver CVE-2021-26855",
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2020-08-19T00:00:00+00:00",
    "extra.file_name": "2020-08-19-scan_exchange.csv",
}

EVENTS = [
    {
        "__type": "Event",
        "feed.name": "Shadowserver CVE-2021-26855",
        "time.source": "2021-05-14T00:11:30+00:00",
        "source.ip": "12.237.1.2",
        "source.port": 443,
        "source.asn": 7018,
        "source.geolocation.cc": "US",
        "source.geolocation.region": "CALIFORNIA",
        "source.geolocation.city": "TURLOCK",
        "source.reverse_dns": 'afs-exch-cas2.xxx.com',
        "extra.version": '15.2.721',
        "extra.source.sector": "Communications, Service Provider, and Hosting Service",
        "extra.source.naics": 517311,
        "classification.identifier": "vulnerable-exchange-server",
        "extra.tag": "exchange;cve-2021-26855",
        "classification.taxonomy": "vulnerable",
        "classification.type": "infected-system",
        "extra.servername": "AFS-EXCH2019",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[1]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Shadowserver CVE-2021-26855",
        "time.source": "2021-05-14T00:11:37+00:00",
        "source.ip": "98.153.3.4",
        "source.port": 443,
        "source.asn": 20001,
        "source.geolocation.cc": "US",
        "source.geolocation.region": "CALIFORNIA",
        "source.geolocation.city": "LOS ANGELES",
        "source.reverse_dns": 'rrcs-98-153-x-x.west.biz.rr.com',
        "extra.version": '15.0.847',
        "extra.source.sector": "Communications, Service Provider, and Hosting Service",
        "extra.source.naics": 517311,
        "extra.tag": "exchange;webshell",
        "classification.taxonomy": "intrusions",
        "classification.type": "system-compromise",
        "classification.identifier": "exchange-server-webshell",
        "extra.servername": "SSAMAIL",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[2]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Shadowserver CVE-2021-26855",
        "time.source": "2021-05-14T00:11:38+00:00",
        "source.ip": "206.210.5.6",
        "source.port": 443,
        "source.asn": 17054,
        "source.geolocation.cc": "US",
        "source.geolocation.region": "PENNSYLVANIA",
        "source.geolocation.city": "PITTSBURGH",
        "source.reverse_dns": 'webmail.xxx.com',
        "extra.source.naics": 518210,
        "extra.version": '15.0.1178',
        "extra.servername": "OMNYXEXCH02",
        "extra.tag": "exchange;webshell",
        "classification.taxonomy": "intrusions",
        "classification.type": "system-compromise",
        "classification.identifier": "exchange-server-webshell",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[3]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Shadowserver CVE-2021-26855",
        "time.source": "2021-05-14T00:11:38+00:00",
        "source.ip": "12.33.7.8",
        "source.port": 443,
        "source.asn": 7018,
        "source.geolocation.cc": "US",
        "source.geolocation.region": "ARKANSAS",
        "source.geolocation.city": "LITTLE ROCK",
        "source.reverse_dns": 'mail.xxx.org',
        "extra.version": '15.1.2176',
        "extra.source.sector": "Communications, Service Provider, and Hosting Service",
        "extra.source.naics": 921120,
        "extra.servername": "MHASVR02",
        "classification.identifier": "vulnerable-exchange-server",
        "extra.tag": "exchange;cve-2021-26855",
        "classification.taxonomy": "vulnerable",
        "classification.type": "infected-system",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[4]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Shadowserver CVE-2021-26855",
        "time.source": "2021-05-14T00:11:38+00:00",
        "source.ip": "41.204.9.10",
        "source.port": 443,
        "source.asn": 21042,
        "source.geolocation.cc": 'MG',
        "source.geolocation.city": 'ANTANANARIVO',
        "source.geolocation.region": 'ANTANANARIVO',
        "source.reverse_dns": 'mail.xxx.mg',
        "extra.servername": "SABMHQE0232",
        "classification.identifier": "vulnerable-exchange-server",
        "extra.tag": "exchange;cve-2021-26855",
        "classification.taxonomy": "vulnerable",
        "classification.type": "infected-system",
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
