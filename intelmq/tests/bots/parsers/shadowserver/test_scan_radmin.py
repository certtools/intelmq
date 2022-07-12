# SPDX-FileCopyrightText: 2020 sinus-x
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), "testdata/scan_radmin.csv")) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    "feed.name": "Accessible Radmin",
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2020-08-19T00:00:00+00:00",
    "extra.file_name": "2020-08-19-scan_radmin-test-test.csv",
}

EVENTS = [
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517312,
        "extra.tag": "radmin",
        "extra.version": "Radmin (Details Unknown)",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.asn": 701,
        "source.geolocation.cc": "US",
        "source.geolocation.city": "BROOKLYN",
        "source.geolocation.region": "NEW YORK",
        "source.ip": "74.101.218.75",
        "source.port": 4899,
        "source.reverse_dns": "static-74-101-218-75.nycmny.fios.verizon.net",
        "time.source": "2020-07-06T13:55:26+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[1]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.asn": 56618,
        "source.geolocation.cc": "RU",
        "source.geolocation.city": "MURMANSK",
        "source.geolocation.region": "MURMANSKAYA OBLAST",
        "source.ip": "192.162.189.171",
        "source.port": 4899,
        "source.reverse_dns": "rubin.an.ru",
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[2]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517311,
        "extra.tag": "radmin",
        "extra.version": "Radmin (Details Unknown)",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "CN",
        "source.geolocation.city": "BEIJING",
        "source.geolocation.region": "BEIJING SHI",
        "source.asn": 4808,
        "source.ip": "111.197.143.69",
        "source.port": 4899,
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[3]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517311,
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "KR",
        "source.geolocation.city": "DAEIN-DONG",
        "source.geolocation.region": "GWANGJU-GWANGYEOKSI",
        "source.asn": 4766,
        "source.ip": "121.147.215.220",
        "source.port": 4899,
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[4]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517311,
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "KR",
        "source.geolocation.city": "DAEIN-DONG",
        "source.geolocation.region": "GWANGJU-GWANGYEOKSI",
        "source.asn": 4766,
        "source.ip": "121.147.215.178",
        "source.port": 4899,
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[5]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517312,
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "CN",
        "source.geolocation.city": "CHONGQING",
        "source.geolocation.region": "CHONGQING SHI",
        "source.asn": 9808,
        "source.ip": "183.230.5.219",
        "source.port": 4899,
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[6]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "RU",
        "source.geolocation.city": "MOSCOW",
        "source.geolocation.region": "MOSKVA",
        "source.asn": 34300,
        "source.ip": "85.93.154.74",
        "source.port": 4899,
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[7]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517311,
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "BE",
        "source.geolocation.city": "BRASSCHAAT",
        "source.geolocation.region": "ANTWERPEN",
        "source.asn": 5432,
        "source.ip": "81.246.135.247",
        "source.port": 4899,
        "source.reverse_dns": "247.135-246-81.adsl-dyn.isp.belgacom.be",
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[8]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "Accessible Radmin",
        "classification.identifier": "accessible-radmin",
        "classification.taxonomy": "vulnerable",
        "classification.type": "vulnerable-system",
        "extra.naics": 517312,
        "extra.tag": "radmin",
        "extra.version": "Radmin v3.X Radmin Authentication",
        "feed.name": "Accessible Radmin",
        "protocol.transport": "tcp",
        "source.geolocation.cc": "ES",
        "source.geolocation.city": "LAS PALMAS DE GRAN CANARIA",
        "source.geolocation.region": "LAS PALMAS",
        "source.asn": 12430,
        "source.ip": "46.27.146.22",
        "source.port": 4899,
        "source.reverse_dns": "static-22-146-27-46.ipcom.comunitel.net",
        "time.source": "2020-07-06T13:55:27+00:00",
        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[9]))),
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
