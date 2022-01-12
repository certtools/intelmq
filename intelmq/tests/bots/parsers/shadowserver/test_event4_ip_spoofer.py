# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), "testdata/event4_ip_spoofer.csv")) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {
    "feed.name": "CAIDA",
    "raw": utils.base64_encode(EXAMPLE_FILE),
    "__type": "Report",
    "time.observation": "2020-08-19T00:00:00+00:00",
    "extra.file_name": "2020-08-19-event4_ip_spoofer.csv",
}

EVENTS = [
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2021-03-28T00:42:59+00:00",
        "source.ip": "98.191.250.0",

        "source.asn": 22898,

        "source.geolocation.cc": "US",
        "source.geolocation.region": "OKLAHOMA",
        "source.geolocation.city": "OKLAHOMA CITY",
        "source.network": "98.191.250.0/24",
        "source.reverse_dns": 'ip-98.191.250.0.atlinkservices.com',
        "extra.routedspoof": "received",
        "extra.session": 1112907,
        "extra.nat": True,
        "extra.public_source": "caida",
        "extra.source.naics": 517311,
        "extra.version": 'ipv4',
        "protocol.transport": 'tcp',

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[1]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2021-03-28T01:36:22+00:00",
        "source.ip": "191.7.16.0",

        "source.asn": 262485,

        "source.geolocation.cc": "BR",
        "source.geolocation.region": "RIO DE JANEIRO",
        "source.geolocation.city": "NOVA IGUACU",
        "source.network": "191.7.16.0/24",
        "extra.routedspoof": "received",
        "extra.session": 1112914,
        "extra.nat": False,
        "extra.public_source": "caida",
        "extra.version": 'ipv4',
        "protocol.transport": 'tcp',

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[2]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2021-03-28T02:10:58+00:00",
        "source.ip": "202.53.160.0",

        "source.asn": 23923,

        "source.geolocation.cc": "BD",
        "source.geolocation.region": "DHAKA",
        "source.geolocation.city": "DHAKA",
        "source.network": "202.53.160.0/24",
        "extra.routedspoof": "received",
        "extra.session": 1112931,
        "extra.nat": True,
        "extra.public_source": "caida",
        "extra.version": 'ipv4',
        "protocol.transport": 'tcp',

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[3]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2021-03-28T03:41:51+00:00",
        "source.ip": "87.121.75.0",

        "source.asn": 134697,

        "source.geolocation.cc": "AU",
        "source.geolocation.region": "QUEENSLAND",
        "source.geolocation.city": "BRISBANE",
        "source.network": "87.121.75.0/24",
        "extra.routedspoof": "received",
        "extra.session": 1112953,
        "extra.nat": True,
        "extra.public_source": "caida",
        "extra.version": 'ipv4',
        "protocol.transport": 'tcp',

        "classification.identifier": "ip-spoofer",
        "classification.taxonomy": "fraud",
        "classification.type": "masquerade",

        "raw": utils.base64_encode("\n".join((EXAMPLE_LINES[0], EXAMPLE_LINES[4]))),
        "time.observation": "2020-08-19T00:00:00+00:00",
    },
    {
        "__type": "Event",
        "feed.name": "CAIDA",
        "time.source": "2021-03-28T06:07:17+00:00",
        "source.ip": "189.201.194.0",

        "source.asn": 262944,

        "source.network": "189.201.194.0/24",
        "source.geolocation.cc": 'MX',
        "source.geolocation.city": 'SALTILLO',
        "source.geolocation.region": 'COAHUILA',
        "source.reverse_dns": 'ip-189-201-194-0.slw.spectro.mx',
        "extra.routedspoof": "received",
        "extra.session": 1113015,
        "extra.nat": True,
        "extra.public_source": "caida",
        "extra.version": 'ipv4',
        "protocol.transport": 'tcp',

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
