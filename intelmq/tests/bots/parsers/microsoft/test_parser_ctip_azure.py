# SPDX-FileCopyrightText: 2020 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import json
import os
import unittest

from intelmq.bots.parsers.microsoft.parser_ctip import MicrosoftCTIPParserBot
from intelmq.lib import test
from intelmq.lib.utils import base64_encode


with open(os.path.join(os.path.dirname(__file__), 'ctip_azure.txt')) as handle:
    EXAMPLE_DATA = handle.read()
EXAMPLE_LINES = EXAMPLE_DATA.splitlines()
EXAMPLE_PARSED = [json.loads(EXAMPLE_LINES[0]), json.loads(EXAMPLE_LINES[1])]


EXAMPLE_REPORT = {
    "__type": "Report",
    "feed.accuracy": 100.0,
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": base64_encode(EXAMPLE_DATA)
}


EXAMPLE_EVENTS = [{
    "__type": "Event",
    "feed.name": "CTIP-Infected",
    "event_description.text": "SinkHoleMessage",
    "tlp": "AMBER",
    'feed.accuracy': 20.0,
    'classification.type': 'infected-system',
    'destination.ip': '198.18.18.18',
    'destination.port': 80,
    'malware.name': 'b67-ss-tinba',
    'source.asn': 64496,
    'source.ip': '224.0.5.8',
"extra.total_encounters": 3,
    "source.port": 65116,
    "time.source": "2020-05-24T22:45:28.487000+00:00",
    "source.as_name": "Example AS 1",
    "source.geolocation.cc": "AT",
    "source.geolocation.latitude": 48.2,
    "source.geolocation.longitude": 16.3667,
    "extra.custom_field1": "tinba",
    "raw": base64_encode(EXAMPLE_LINES[0]),
    "extra.payload.timestamp": '2020-05-24T22:45:28.487420+00:00',
    "extra.payload.ip": "127.0.0.1",
    "extra.payload.port" :65116,
    "extra.payload.server.ip": "198.18.185.162",
    "extra.payload.server.port": 80,
    "destination.fqdn": "example.com",
    "extra.payload.family":"tinba",
    "extra.payload.response":"Response",
    "extra.payload.handler":"tinba",
    "protocol.application":"http",
    'extra.malware': 'Avalanche',
    }, {
    "__type": "Event",
    "feed.name": "CTIP-Infected",
    "event_description.text": "SinkHoleMessage",
    "tlp": "AMBER",
    'feed.accuracy': 100.0,
    'classification.type': 'infected-system',
    'destination.ip': '198.18.18.18',
    'destination.port': 80,
    'malware.name': 'b67-ss-matsnu',
"extra.total_encounters": 5,
    'source.asn': 64497,
    'source.ip': '224.0.5.8',
    "source.port": 49296,
    "time.source": "2020-05-24T22:47:43.050999+00:00",
    "source.as_name": "Example AS 2",
    "source.geolocation.cc": "AT",
    "source.geolocation.latitude": 48.1951,
    "source.geolocation.longitude": 16.3483,
"extra.source.geolocation.area_code": 9,
"extra.source.geolocation.postal_code": '1060',
"source.geolocation.region": "Vienna",
"source.geolocation.city": "Vienna",
    "extra.custom_field1": "matsnu5",
    "raw": base64_encode(EXAMPLE_LINES[1]),
    "extra.payload.text": 'this is just some text',
    'extra.malware': 'Avalanche',
    }, {
    "__type": "Event",
    "feed.name": "CTIP-Infected",
    "event_description.text": "SinkHoleMessage",
    'feed.accuracy': 100.0,
    'classification.type': 'infected-system',
    'destination.ip': '10.0.0.1',
    'destination.port': 8080,
    'event_description.text': 'Microsoft.DCU.CTIP.Gov.0001',
    'extra.custom_field1': 'bot-id-data',
    'extra.custom_field2': 'comp-name',
    'extra.malware': 'Emotet',
    'extra.payload.bot_id': 'bot-id-data',
    'extra.payload.computer_name': 'comp-name',
    'extra.payload.destination.ip': '10.0.0.1',
    'extra.payload.destination.port': '8080',
    'extra.payload.source.ip': '10.0.0.1',
    'extra.payload.source.port': '33587',
    'extra.payload.timestamp_utc': '2021-04-07T10:59:32',
    'extra.source.geolocation.area_code': 6,
    'extra.source.geolocation.postal_code': '8042',
    'extra.total_encounters': 1,
    'feed.name': 'Microsoft.DCU.CTIP.Infected',
    'malware.name': 'b77-gv',
    "raw": base64_encode(EXAMPLE_LINES[2]),
    'source.as_name': 'Example AS',
    'source.asn': 64496,
    'source.geolocation.city': 'Graz',
    'source.geolocation.latitude': 47.1298,
    'source.geolocation.longitude': 15.466,
    'source.geolocation.region': 'Styria',
    'source.ip': '224.0.5.8',
    'source.port': 33587,
    'time.source': '2021-04-07T10:59:32+00:00',
    'tlp': 'GREEN',
    'source.geolocation.cc': 'AT',
    },
    {
        '__type': 'Event',
        'classification.type': 'infected-system',
        'destination.ip': '10.0.0.1',
        'destination.port': 80,
        'event_description.text': 'Microsoft.DCU.CTIP.Sinkhole',
        'extra.custom_field1': 'andromeda210',
        'extra.malware': 'Avalanche',
        'destination.fqdn': 'example.com',
        'extra.payload.family': 'andromeda',
        'extra.payload.handler': 'handler1',
        'extra.payload.ip': '224.0.5.8',
        'extra.payload.port': 28285,
        'extra.payload.response': 'HttpOk',
        'extra.payload.server.ip': '10.0.0.1',
        'extra.payload.server.port': 80,
        'extra.payload.timestamp': '2021-05-10T15:47:42.242316+00:00',
        'extra.total_encounters': 2,
        'feed.accuracy': 20.0,
        'feed.name': 'Microsoft.DCU.CTIP.Infected',
        'malware.name': 'b67-ss-gamarue',
        'protocol.application': 'http',
        'raw': 'eyJEYXRhRmVlZCI6Ik1pY3Jvc29mdC5EQ1UuQ1RJUC5JbmZlY3RlZCIsIlNvdXJjZWRGcm9tIjoiTWljcm9zb2Z0LkRDVS5DVElQLlNpbmtob2xlIiwiRGF0ZVRpbWVSZWNlaXZlZFV0YyI6MTMyNjUxMzUyNjIyNDIwMDAwLCJEYXRlVGltZVJlY2VpdmVkVXRjVHh0IjoiTW9uZGF5IE1heSAxMCAyMDIxIDE1OjQ3OjQyLjI0MjAiLCJNYWx3YXJlIjoiQXZhbGFuY2hlIiwiVGhyZWF0Q29kZSI6IkI2Ny1TUy1HYW1hcnVlIiwiVGhyZWF0Q29uZmlkZW5jZSI6IkxvdyIsIlRvdGFsRW5jb3VudGVycyI6MiwiVExQIjoiR3JlZW4iLCJTb3VyY2VJcCI6IjIyNC4wLjUuOCIsIlNvdXJjZVBvcnQiOjI4Mjg1LCJEZXN0aW5hdGlvbklwIjoiMTAuMC4wLjEiLCJEZXN0aW5hdGlvblBvcnQiOjgwLCJTb3VyY2VJcEluZm8iOnsiU291cmNlSXBBc25OdW1iZXIiOiI2NDQ5NiIsIlNvdXJjZUlwQXNuT3JnTmFtZSI6IkV4YW1wbGUgQVMiLCJTb3VyY2VJcENvdW50cnlDb2RlIjoiQVQiLCJTb3VyY2VJcFJlZ2lvbiI6IiIsIlNvdXJjZUlwQ2l0eSI6IiIsIlNvdXJjZUlwUG9zdGFsQ29kZSI6IiIsIlNvdXJjZUlwTGF0aXR1ZGUiOjQ4LjIsIlNvdXJjZUlwTG9uZ2l0dWRlIjoxNi4zNjY3LCJTb3VyY2VJcE1ldHJvQ29kZSI6MCwiU291cmNlSXBBcmVhQ29kZSI6MCwiU291cmNlSXBDb25uZWN0aW9uVHlwZSI6IkNlbGx1bGFyIiwiU291cmNlSXB2NEludCI6Mzc1ODA5NzY3Mn0sIkh0dHBJbmZvIjp7Ikh0dHBIb3N0IjoiIiwiSHR0cFJlcXVlc3QiOiIiLCJIdHRwTWV0aG9kIjoiIiwiSHR0cFJlZmVycmVyIjoiIiwiSHR0cFVzZXJBZ2VudCI6IiIsIkh0dHBWZXJzaW9uIjoiIn0sIkN1c3RvbUluZm8iOnsiQ3VzdG9tRmllbGQxIjoiYW5kcm9tZWRhMjEwIiwiQ3VzdG9tRmllbGQyIjoiIiwiQ3VzdG9tRmllbGQzIjoiIiwiQ3VzdG9tRmllbGQ0IjoiIiwiQ3VzdG9tRmllbGQ1IjoiIn0sIlBheWxvYWQiOiJleUowY3lJNk1UWXlNRFkyTVRZMk1pNHlOREl6TVRZc0ltbHdJam9pTWpJMExqQXVOUzQ0SWl3aWNHOXlkQ0k2TWpneU9EVXNJbk5sY25abGNrbHdJam9pTVRBdU1DNHdMakVpTENKelpYSjJaWEpRYjNKMElqbzRNQ3dpWkc5dFlXbHVJam9pWlhoaGJYQnNaUzVqYjIwaUxDSm1ZVzFwYkhraU9pSmhibVJ5YjIxbFpHRWlMQ0p0WVd4M1lYSmxJanA3ZlN3aWNtVnpjRzl1YzJVaU9pSklkSFJ3VDJzaUxDSm9ZVzVrYkdWeUlqb2lhR0Z1Wkd4bGNqRWlMQ0owZVhCbElqb2lTSFIwY0NKOSJ9',
        'source.as_name': 'Example AS',
        'source.asn': 64496,
        'source.geolocation.cc': 'AT',
        'source.geolocation.latitude': 48.2,
        'source.geolocation.longitude': 16.3667,
        'source.ip': '224.0.5.8',
        'source.port': 28285,
        'time.source': '2021-05-10T15:47:42.241999+00:00',
        'tlp': 'GREEN',
        'extra.source.connection_type': 'Cellular',
    },
]


class TestMicrosoftCTIPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for the MicrosoftCTIPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MicrosoftCTIPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test with azure format. """
        self.run_bot()
        for i in range(4):
            self.assertMessageEqual(i, EXAMPLE_EVENTS[i])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
