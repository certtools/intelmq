# SPDX-FileCopyrightText: 2022 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.abusech.parser_feodotracker import AbusechFeodoTrackerParserBot

INPUT = """
[
    {
        "ip_address": "51.178.161.32",
        "port": 4643,
        "status": "online",
        "hostname": "srv-web.ffconsulting.com",
        "as_number": 16276,
        "as_name": "OVH",
        "country": "FR",
        "first_seen": "2021-01-17 07:44:46",
        "last_online": "2022-11-15",
        "malware": "Dridex"
    },
    {
        "ip_address": "142.44.247.57",
        "port": 4043,
        "status": "offline",
        "hostname": "57.ip-142-44-247.net",
        "as_number": 16276,
        "as_name": "OVH",
        "country": "CA",
        "first_seen": "2021-01-26 03:22:41",
        "last_online": "2022-10-17",
        "malware": "Dridex"
    },
    {
        "ip_address": "37.187.115.122",
        "port": 6601,
        "status": "online",
        "hostname": "ns328855.ip-37-187-115.eu",
        "as_number": 16276,
        "as_name": "OVH",
        "country": "FR",
        "first_seen": "2021-02-22 16:57:59",
        "last_online": "2022-11-15",
        "malware": "Dridex"
    },
    {
        "ip_address": "1.234.21.73",
        "port": 6601,
        "status": "online",
        "hostname": null,
        "as_number": 9318,
        "as_name": "SKB-AS SK Broadband Co Ltd",
        "country": "KR",
        "last_online": "2022-11-15",
        "malware": "Dridex"
    }
]
"""

OUTPUT = [
    {
        '__type': 'Event',
        'classification.type': 'c2-server',
        'extra.last_online': '2022-11-15',
        'status': 'online',
        'malware.name': 'dridex',
        'raw': 'W3siaXBfYWRkcmVzcyI6ICI1MS4xNzguMTYxLjMyIiwgInBvcnQiOiA0NjQzLCAic3RhdHVzIjogIm9ubGluZSIsICJob3N0bmFtZSI6ICJzcnYtd2ViLmZmY29uc3VsdGluZy5jb20iLCAiYXNfbnVtYmVyIjogMTYyNzYsICJhc19uYW1lIjogIk9WSCIsICJjb3VudHJ5IjogIkZSIiwgImZpcnN0X3NlZW4iOiAiMjAyMS0wMS0xNyAwNzo0NDo0NiIsICJsYXN0X29ubGluZSI6ICIyMDIyLTExLTE1IiwgIm1hbHdhcmUiOiAiRHJpZGV4In1d',
        'source.as_name': 'OVH',
        'source.asn': 16276,
        'source.geolocation.cc': 'FR',
        'source.ip': '51.178.161.32',
        'source.port': 4643,
        'source.reverse_dns': 'srv-web.ffconsulting.com',
        'time.source': '2021-01-17T07:44:46+00:00'
    },
    {
        '__type': 'Event',
        'classification.type': 'c2-server',
        'extra.last_online': '2022-10-17',
        'status': 'offline',
        'malware.name': 'dridex',
        'raw': 'W3siaXBfYWRkcmVzcyI6ICIxNDIuNDQuMjQ3LjU3IiwgInBvcnQiOiA0MDQzLCAic3RhdHVzIjogIm9mZmxpbmUiLCAiaG9zdG5hbWUiOiAiNTcuaXAtMTQyLTQ0LTI0Ny5uZXQiLCAiYXNfbnVtYmVyIjogMTYyNzYsICJhc19uYW1lIjogIk9WSCIsICJjb3VudHJ5IjogIkNBIiwgImZpcnN0X3NlZW4iOiAiMjAyMS0wMS0yNiAwMzoyMjo0MSIsICJsYXN0X29ubGluZSI6ICIyMDIyLTEwLTE3IiwgIm1hbHdhcmUiOiAiRHJpZGV4In1d',
        'source.as_name': 'OVH',
        'source.asn': 16276,
        'source.geolocation.cc': 'CA',
        'source.ip': '142.44.247.57',
        'source.port': 4043,
        'source.reverse_dns': '57.ip-142-44-247.net',
        'time.source': '2021-01-26T03:22:41+00:00'
    },
    {
        '__type': 'Event',
        'classification.type': 'c2-server',
        'extra.last_online': '2022-11-15',
        'status': 'online',
        'malware.name': 'dridex',
        'raw': 'W3siaXBfYWRkcmVzcyI6ICIzNy4xODcuMTE1LjEyMiIsICJwb3J0IjogNjYwMSwgInN0YXR1cyI6ICJvbmxpbmUiLCAiaG9zdG5hbWUiOiAibnMzMjg4NTUuaXAtMzctMTg3LTExNS5ldSIsICJhc19udW1iZXIiOiAxNjI3NiwgImFzX25hbWUiOiAiT1ZIIiwgImNvdW50cnkiOiAiRlIiLCAiZmlyc3Rfc2VlbiI6ICIyMDIxLTAyLTIyIDE2OjU3OjU5IiwgImxhc3Rfb25saW5lIjogIjIwMjItMTEtMTUiLCAibWFsd2FyZSI6ICJEcmlkZXgifV0=',
        'source.as_name': 'OVH',
        'source.asn': 16276,
        'source.geolocation.cc': 'FR',
        'source.ip': '37.187.115.122',
        'source.port': 6601,
        'source.reverse_dns': 'ns328855.ip-37-187-115.eu',
        'time.source': '2021-02-22T16:57:59+00:00'
    },
    {
        '__type': 'Event',
        'classification.type': 'c2-server',
        'extra.last_online': '2022-11-15',
        'status': 'online',
        'malware.name': 'dridex',
        'raw': 'W3siaXBfYWRkcmVzcyI6ICIxLjIzNC4yMS43MyIsICJwb3J0IjogNjYwMSwgInN0YXR1cyI6ICJvbmxpbmUiLCAiaG9zdG5hbWUiOiBudWxsLCAiYXNfbnVtYmVyIjogOTMxOCwgImFzX25hbWUiOiAiU0tCLUFTIFNLIEJyb2FkYmFuZCBDbyBMdGQiLCAiY291bnRyeSI6ICJLUiIsICJsYXN0X29ubGluZSI6ICIyMDIyLTExLTE1IiwgIm1hbHdhcmUiOiAiRHJpZGV4In1d',
        'source.as_name': 'SKB-AS SK Broadband Co Ltd',
        'source.asn': 9318,
        'source.geolocation.cc': 'KR',
        'source.ip': '1.234.21.73',
        'source.port': 6601,
        'time.source': '2022-11-15T00:00:00+00:00'
    }

]


class TestAbusechFeodoTrackerParserBot(test.BotTestCase, unittest.TestCase):
    """
    TestCase for AbusechFeodoTrackerParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AbusechFeodoTrackerParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT)}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT[0])
        self.assertMessageEqual(1, OUTPUT[1])
        self.assertMessageEqual(2, OUTPUT[2])
        self.assertMessageEqual(3, OUTPUT[3])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
