# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.phishtank.parser import PhishTankParserBot

INPUT = """
[
  {
    "phish_id": "7946016",
    "url": "https://ardentig.top/",
    "phish_detail_url": "http://www.phishtank.com/phish_detail.php?phish_id=7946016",
    "submission_time": "2022-11-16T14:08:44+00:00",
    "verified": "yes",
    "verification_time": "2022-11-16T14:12:55+00:00",
    "online": "yes",
    "details": [
      {
        "ip_address": "204.152.210.139",
        "cidr_block": "204.152.192.0/19",
        "announcing_network": "8100",
        "rir": "arin",
        "country": "US",
        "detail_time": "2022-11-16T14:13:00+00:00"
      }
    ],
    "target": "AEON Card"
  },
  {
    "phish_id": "7946015",
    "url": "https://attmailupdateinc2022update.square.site/",
    "phish_detail_url": "http://www.phishtank.com/phish_detail.php?phish_id=7946015",
    "submission_time": "2022-11-16T14:08:10+00:00",
    "verified": "yes",
    "verification_time": "2022-11-16T14:12:55+00:00",
    "online": "yes",
    "details": [
      {
        "ip_address": "199.34.228.40",
        "cidr_block": "199.34.228.0/22",
        "announcing_network": "27647",
        "rir": "arin",
        "country": "US",
        "detail_time": "2022-11-16T14:12:59+00:00"
      }
    ],
    "target": "Other"
  },
  {
    "phish_id": "7946013",
    "url": "https://newlife209.godaddysites.com/",
    "phish_detail_url": "http://www.phishtank.com/phish_detail.php?phish_id=7946013",
    "submission_time": "2022-11-16T14:04:22+00:00",
    "verified": "yes",
    "verification_time": "2022-11-16T14:12:55+00:00",
    "online": "yes",
    "details": [
      {
        "ip_address": "76.223.105.230",
        "cidr_block": "76.223.96.0/20",
        "announcing_network": "16509",
        "rir": "arin",
        "country": "US",
        "detail_time": "2022-11-16T14:10:32+00:00"
      }
    ],
    "target": "Other"
  }
]
"""

OUTPUT = [
    {
        '__type': 'Event',
        'classification.type': 'phishing',
        'status': 'online',
        'event_description.url': 'http://www.phishtank.com/phish_detail.php?phish_id=7946016',
        'extra.phishtank.phish_id': '7946016',
        'event_description.target': 'AEON Card',
        'extra.phishtank.verification_time': '2022-11-16T14:12:55+00:00',
        'extra.phishtank.verified': 'yes',
        'raw': 'W3sicGhpc2hfaWQiOiAiNzk0NjAxNiIsICJ1cmwiOiAiaHR0cHM6Ly9hcmRlbnRpZy50b3AvIiwgInBoaXNoX2RldGFpbF91cmwiOiAiaHR0cDovL3d3dy5waGlzaHRhbmsuY29tL3BoaXNoX2RldGFpbC5waHA/cGhpc2hfaWQ9Nzk0NjAxNiIsICJzdWJtaXNzaW9uX3RpbWUiOiAiMjAyMi0xMS0xNlQxNDowODo0NCswMDowMCIsICJ2ZXJpZmllZCI6ICJ5ZXMiLCAidmVyaWZpY2F0aW9uX3RpbWUiOiAiMjAyMi0xMS0xNlQxNDoxMjo1NSswMDowMCIsICJvbmxpbmUiOiAieWVzIiwgImRldGFpbHMiOiBbeyJpcF9hZGRyZXNzIjogIjIwNC4xNTIuMjEwLjEzOSIsICJjaWRyX2Jsb2NrIjogIjIwNC4xNTIuMTkyLjAvMTkiLCAiYW5ub3VuY2luZ19uZXR3b3JrIjogIjgxMDAiLCAicmlyIjogImFyaW4iLCAiY291bnRyeSI6ICJVUyIsICJkZXRhaWxfdGltZSI6ICIyMDIyLTExLTE2VDE0OjEzOjAwKzAwOjAwIn1dLCAidGFyZ2V0IjogIkFFT04gQ2FyZCJ9XQ==',
        'source.asn': 8100,
        'source.geolocation.cc': 'US',
        'source.ip': '204.152.210.139',
        'source.network': '204.152.192.0/19',
        'source.url': 'https://ardentig.top/',
        'time.source': '2022-11-16T14:08:44+00:00'
    },
    {
        '__type': 'Event',
        'classification.type': 'phishing',
        'status': 'online',
        'event_description.url': 'http://www.phishtank.com/phish_detail.php?phish_id=7946015',
        'extra.phishtank.phish_id': '7946015',
        'event_description.target': 'Other',
        'extra.phishtank.verification_time': '2022-11-16T14:12:55+00:00',
        'extra.phishtank.verified': 'yes',
        'raw': 'W3sicGhpc2hfaWQiOiAiNzk0NjAxNSIsICJ1cmwiOiAiaHR0cHM6Ly9hdHRtYWlsdXBkYXRlaW5jMjAyMnVwZGF0ZS5zcXVhcmUuc2l0ZS8iLCAicGhpc2hfZGV0YWlsX3VybCI6ICJodHRwOi8vd3d3LnBoaXNodGFuay5jb20vcGhpc2hfZGV0YWlsLnBocD9waGlzaF9pZD03OTQ2MDE1IiwgInN1Ym1pc3Npb25fdGltZSI6ICIyMDIyLTExLTE2VDE0OjA4OjEwKzAwOjAwIiwgInZlcmlmaWVkIjogInllcyIsICJ2ZXJpZmljYXRpb25fdGltZSI6ICIyMDIyLTExLTE2VDE0OjEyOjU1KzAwOjAwIiwgIm9ubGluZSI6ICJ5ZXMiLCAiZGV0YWlscyI6IFt7ImlwX2FkZHJlc3MiOiAiMTk5LjM0LjIyOC40MCIsICJjaWRyX2Jsb2NrIjogIjE5OS4zNC4yMjguMC8yMiIsICJhbm5vdW5jaW5nX25ldHdvcmsiOiAiMjc2NDciLCAicmlyIjogImFyaW4iLCAiY291bnRyeSI6ICJVUyIsICJkZXRhaWxfdGltZSI6ICIyMDIyLTExLTE2VDE0OjEyOjU5KzAwOjAwIn1dLCAidGFyZ2V0IjogIk90aGVyIn1d',
        'source.asn': 27647,
        'source.geolocation.cc': 'US',
        'source.ip': '199.34.228.40',
        'source.network': '199.34.228.0/22',
        'source.url': 'https://attmailupdateinc2022update.square.site/',
        'time.source': '2022-11-16T14:08:10+00:00'
    },
    {
        '__type': 'Event',
        'classification.type': 'phishing',
        'status': 'online',
        'event_description.url': 'http://www.phishtank.com/phish_detail.php?phish_id=7946013',
        'extra.phishtank.phish_id': '7946013',
        'event_description.target': 'Other',
        'extra.phishtank.verification_time': '2022-11-16T14:12:55+00:00',
        'extra.phishtank.verified': 'yes',
        'raw': 'W3sicGhpc2hfaWQiOiAiNzk0NjAxMyIsICJ1cmwiOiAiaHR0cHM6Ly9uZXdsaWZlMjA5LmdvZGFkZHlzaXRlcy5jb20vIiwgInBoaXNoX2RldGFpbF91cmwiOiAiaHR0cDovL3d3dy5waGlzaHRhbmsuY29tL3BoaXNoX2RldGFpbC5waHA/cGhpc2hfaWQ9Nzk0NjAxMyIsICJzdWJtaXNzaW9uX3RpbWUiOiAiMjAyMi0xMS0xNlQxNDowNDoyMiswMDowMCIsICJ2ZXJpZmllZCI6ICJ5ZXMiLCAidmVyaWZpY2F0aW9uX3RpbWUiOiAiMjAyMi0xMS0xNlQxNDoxMjo1NSswMDowMCIsICJvbmxpbmUiOiAieWVzIiwgImRldGFpbHMiOiBbeyJpcF9hZGRyZXNzIjogIjc2LjIyMy4xMDUuMjMwIiwgImNpZHJfYmxvY2siOiAiNzYuMjIzLjk2LjAvMjAiLCAiYW5ub3VuY2luZ19uZXR3b3JrIjogIjE2NTA5IiwgInJpciI6ICJhcmluIiwgImNvdW50cnkiOiAiVVMiLCAiZGV0YWlsX3RpbWUiOiAiMjAyMi0xMS0xNlQxNDoxMDozMiswMDowMCJ9XSwgInRhcmdldCI6ICJPdGhlciJ9XQ==',
        'source.asn': 16509,
        'source.geolocation.cc': 'US',
        'source.ip': '76.223.105.230',
        'source.network': '76.223.96.0/20',
        'source.url': 'https://newlife209.godaddysites.com/',
        'time.source': '2022-11-16T14:04:22+00:00'
    }
]


class TestPhishTankParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for PhishTankParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = PhishTankParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT)}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT[0])
        self.assertMessageEqual(1, OUTPUT[1])
        self.assertMessageEqual(2, OUTPUT[2])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
