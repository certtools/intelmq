# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.cert_eu.parser_csv import CertEUCSVParserBot

with open(os.path.join(os.path.dirname(__file__), 'example.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_FILE_SPLIT = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.url": "https://www.cert-eu.eu",
                  "feed.name": "CERT-EU Feed",
                  "__type": "Report",
                  "time.observation": "2018-01-01T01:00:00+00:00",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "feed.accuracy": 50,
                  }

EXAMPLE_EVENT1 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "109.125.93.10",
    "raw": utils.base64_encode('\r\n'.join(EXAMPLE_FILE_SPLIT[:2])),
    "time.observation": "2018-01-01T01:00:00+00:00",
    "extra.cert_eu_time_observation": "2019-04-01T10:13:23+00:00",
    "classification.type": "malware",
    "time.source": "2019-04-01T03:13:20+00:00",
    "tlp": "AMBER",
    "event_description.text": "A URL is the most common resource with reference to malware binary distribution.",
    'source.asn': 65536,
    'source.geolocation.city': 'Linz',
    'source.geolocation.country': 'Austria',
    'source.geolocation.geoip_cc': 'AT',
    'source.geolocation.latitude': 48.306389,
    'source.geolocation.longitude': 14.28611,
    "feed.accuracy": 25.5,
    "extra.datasource": "RI",
    "__type": "Event",
    "source.url": "http://example.com/",
    'extra.expiration_date': '2019-05-01 09:27:55Z',
    'extra.first_seen': '2019-04-01 03:13:20Z',
    'extra.last_seen': '2019-04-01 03:13:20Z',
    'extra.source.geolocation.geohash': 'u2d4v1fv47xd',
    'source.as_name': 'EXAMPLE, AT',
}

EXAMPLE_EVENT2 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "144.76.221.34",
    "raw": utils.base64_encode('\r\n'.join((EXAMPLE_FILE_SPLIT[0],
                                            EXAMPLE_FILE_SPLIT[2]))),
    "extra.cert_eu_time_observation": "2019-04-01T00:52:35+00:00",
    "time.source": "2019-03-31T23:05:41+00:00",
    "time.observation": "2018-01-01T01:00:00+00:00",
    "tlp": "GREEN",
    "event_description.text": "This type most often refers to a URL which is trying to defraud the users of their credentials.",
    'source.fqdn': 'example.com',
    'source.geolocation.city': 'Vienna',
    'source.geolocation.country': 'Austria',
    'source.geolocation.geoip_cc': 'AT',
    'source.geolocation.latitude': 48.208488,
    'source.geolocation.longitude': 16.37208,
    'source.ip': '144.76.221.34',
    'source.url': 'http://example.com',
    "feed.accuracy": 25.0,
    "event_description.target": "Other",
    "source.asn": 65536,
    "classification.type": "phishing",
    "extra.datasource": "Z",
    "__type": "Event",
    'extra.source.geolocation.geohash': 'u2edk81fc1e8',
    'source.as_name': 'EXAMPLE, AT',
 }


class TestCertEUCSVParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for TestCertEUCSVParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CertEUCSVParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT1)
        self.assertMessageEqual(1, EXAMPLE_EVENT2)


if __name__ == '__main__':
    unittest.main()
