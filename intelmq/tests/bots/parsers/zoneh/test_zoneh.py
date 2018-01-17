# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.zoneh.parser import ZoneHParserBot

with open(
    os.path.join(os.path.dirname(__file__), 'defacement_accepted.csv')
) as handle:
    ACCEPTED_FILE = handle.read()
ACCEPTED_LINES = ACCEPTED_FILE.splitlines(keepends=True)


ACCEPTED_REPORT = {
    "feed.name": "ZoneH Defacements",
    "raw": utils.base64_encode(ACCEPTED_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
}

ACCEPTED_EVENT00 = {
    '__type': 'Event',
    'feed.name': 'ZoneH Defacements',
    'classification.type': 'compromised',
    'classification.identifier': 'compromised-website',
    'extra.accepted_date': "2016-06-01 13:20:21",
    "extra.actor": "L33tz",
    "extra.compromise_method": "known vulnerability (i.e. unpatched system)",
    "extra.http_target": "IIS/7.5",
    "extra.os.name": "Win 2008",
    "extra.zoneh_report_id": "12345678",
    'protocol.application': 'http',
    'raw': utils.base64_encode(ACCEPTED_LINES[0] + ACCEPTED_LINES[1]),
    'source.geolocation.cc': 'ZZ',
    'source.ip': '203.0.113.1',
    'source.url': 'http://defaced.example.com',
    'source.fqdn': 'defaced.example.com',
    'event_description.text': 'defacement',
    'time.observation': '2015-01-01T00:00:00+00:00',
    'time.source': '2016-01-01T11:56:00+00:00'}


ACCEPTED_EVENT01 = {
    '__type': 'Event',
    'feed.name': 'ZoneH Defacements',
    'classification.type': 'compromised',
    'classification.identifier': 'compromised-website',
    'extra.accepted_date': "2017-06-11 10:00:00",
    "extra.actor": "mayhab",
    "extra.compromise_method": "SQL Injection",
    "extra.http_target": "Apache",
    "extra.os.name": "Linux",
    "extra.zoneh_report_id": "12345679",
    'protocol.application': 'http',
    'raw': utils.base64_encode(ACCEPTED_LINES[0] + ACCEPTED_LINES[2].strip()),
    'source.geolocation.cc': 'ZZ',
    'source.ip': '203.0.113.2',
    'source.url': 'http://defaced2.example.com/mayhab.txt',
    'source.fqdn': 'defaced2.example.com',
    'event_description.text': 'defacement',
    'time.observation': '2015-01-01T00:00:00+00:00',
    'time.source': '2017-06-11T09:00:00+00:00'}


with open(
    os.path.join(os.path.dirname(__file__), 'defacement_pending.csv')
) as handle:
    PENDING_FILE = handle.read()
PENDING_LINES = PENDING_FILE.splitlines(keepends=True)

PENDING_REPORT = {
    "feed.name": "ZoneH Defacements",
    "raw": utils.base64_encode(PENDING_FILE),
    "__type": "Report",
    "time.observation": "2015-01-01T00:00:00+00:00",
}

# missing accepted_date in extras
PENDING_EVENT00 = {
    '__type': 'Event',
    'feed.name': 'ZoneH Defacements',
    'classification.type': 'compromised',
    'classification.identifier': 'compromised-website',
    'protocol.application': 'https',
    'extra.actor': "xyz crew",
    "extra.compromise_method": "Not available",
    "extra.http_target": "Apache",
    "extra.os.name": "Linux",
    "extra.zoneh_report_id": "29715024",
    'raw': utils.base64_encode(PENDING_LINES[0] + PENDING_LINES[1].strip()),
    'source.geolocation.cc': 'AU',
    'source.ip': '1.1.1.1',
    'source.url': 'https://www.example.com/defaced.html',
    'source.fqdn': 'www.example.com',
    'event_description.text': 'defacement',
    'time.observation': '2015-01-01T00:00:00+00:00',
    'time.source': '2017-06-13T08:12:48+00:00'}


class TestZoneHParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ZoneHParserBot, where records have been confirmed /
    accepted by ZoneH (includes "accept_date" field).
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ZoneHParserBot
        cls.default_input_message = ACCEPTED_REPORT
        cls.sysconfig = {'feedname': 'Compromised-Website'}
        print(PENDING_LINES)

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, ACCEPTED_EVENT00)
        self.assertMessageEqual(1, ACCEPTED_EVENT01)

    def test_pending_event(self):
        self.input_message = PENDING_REPORT
        self.run_bot()
        self.assertMessageEqual(0, PENDING_EVENT00)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
