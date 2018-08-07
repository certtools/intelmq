# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.cert_eu.parser_csv import CertEUCSVParserBot

with open(os.path.join(os.path.dirname(__file__), 'example.csv')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://www.cert-eu.eu",
                  "feed.name": "CERT-EU Feed",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE)
                  }

EXAMPLE_EVENT1 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "109.125.93.10",
    "raw": "ZGF0YXNvdXJjZSxzb3VyY2UgaXAsb2JzZXJ2YXRpb24gdGltZSx0bHAsZGVzY3JpcHRpb24sdHlwZSxjb3VudCxzb3VyY2UgdGltZSxzb3VyY2UgY291bnRyeSxwcm90b2NvbCxkZXN0aW5hdGlvbiBwb3J0LHNvdXJjZSBsYXRpdHVkZSxzb3VyY2UgY2l0eSxzb3VyY2UgY2Msc291cmNlIGxvbmdpdHVkZSxmaXJzdF9zZWVuLG51bV9zZW5zb3JzLGNvbmZpZGVuY2UgbGV2ZWwsbGFzdF9zZWVuLHRhcmdldCxwaGlzaGluZyxhc24sZG9tYWluIG5hbWUNClNSLDEwOS4xMjUuOTMuMTAsMjAxOC0wNy0wNiAxMDo1OTowNlosZ3JlZW4sQSBVUkwgaXMgdGhlIG1vc3QgY29tbW9uIHJlc291cmNlIHdpdGggcmVmZXJlbmNlIHRvIG1hbHdhcmUgYmluYXJ5IGRpc3RyaWJ1dGlvbi4sbWFsd2FyZSB1cmwsNiwyMDE4LTA3LTA2IDA4OjUyOjE2WixHZXJtYW55LHNtYmQsNDQ1LDQ4LjEzNzQyOCxNdW5pY2gsREUsMTEuNTc1NDksMjAxOC0wNy0wNlQwODozNDo1NS43NTkwMDAsMSw1MCwyMDE4LTA3LTA2VDA4OjUyOjE2LjEwOTAwMCwsLCwNCg==",
    "time.observation": "2018-07-06T10:59:06+00:00",
    "classification.type": "malware",
    "time.source": "2018-07-06T08:52:16+00:00",
    "tlp": "GREEN",
    "event_description.text": "A URL is the most common resource with reference to malware binary distribution.",
    "source.geolocation.country": "Germany",
    "protocol.application": "smbd",
    "destination.port": 445,
    "source.geolocation.latitude": 48.137428,
    "source.geolocation.city": "Munich",
    "source.geolocation.geoip_cc": "DE",
    "source.geolocation.longitude": 11.57549,
    "feed.accuracy": 50.0,
    # "event_description.target": None,
    # "source.url": None,
    # "source.asn": None,
    # "source.asn": None,
    # "source.fqdn": None,
    "__type": "Event"
}

EXAMPLE_EVENT2 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "144.76.221.34",
    "raw": "ZGF0YXNvdXJjZSxzb3VyY2UgaXAsb2JzZXJ2YXRpb24gdGltZSx0bHAsZGVzY3JpcHRpb24sdHlwZSxjb3VudCxzb3VyY2UgdGltZSxzb3VyY2UgY291bnRyeSxwcm90b2NvbCxkZXN0aW5hdGlvbiBwb3J0LHNvdXJjZSBsYXRpdHVkZSxzb3VyY2UgY2l0eSxzb3VyY2UgY2Msc291cmNlIGxvbmdpdHVkZSxmaXJzdF9zZWVuLG51bV9zZW5zb3JzLGNvbmZpZGVuY2UgbGV2ZWwsbGFzdF9zZWVuLHRhcmdldCxwaGlzaGluZyxhc24sZG9tYWluIG5hbWUNClosMTQ0Ljc2LjIyMS4zNCwyMDE4LTA3LTA2IDExOjM0OjUzWixncmVlbixUaGlzIHR5cGUgbW9zdCBvZnRlbiByZWZlcnMgdG8gYSBVUkwgd2hpY2ggaXMgdHJ5aW5nIHRvIGRlZnJhdWQgdGhlIHVzZXJzIG9mIHRoZWlyIGNyZWRlbnRpYWxzLixwaGlzaGluZywsMjAxOC0wNy0wNSAxNDozMjowNlosR2VybWFueSwsLDQ5LjQ0Nzc4MSxOdXJlbWJlcmcsREUsMTEuMDY4MzMsLCw1MCwsT3RoZXIsaHR0cHM6Ly9qYW5hZ2FtZXMuY29tL2RldGFpbHMvcGFja2FnZS12aWV3L2RobC5jb20vLDI0OTQwLGphbmFnYW1lcy5jb20NCg==",
    "time.observation": "2018-07-06T10:59:06+00:00",
    "time.source": "2018-07-05T14:32:06+00:00",
    "tlp": "GREEN",
    "event_description.text": "This type most often refers to a URL which is trying to defraud the users of their credentials.",
    "source.geolocation.country": "Germany",
    "source.geolocation.latitude": 49.447781,
    "source.geolocation.city": "Nuremberg",
    "source.geolocation.geoip_cc": "DE",
    "source.geolocation.longitude": 11.06833,
    "feed.accuracy": 50.0,
    "event_description.target": "Other",
    "source.url": "https://janagames.com/details/package-view/dhl.com/",
    "source.asn": 24940,
    "source.fqdn": "janagames.com",
    "classification.type": "phishing",
    "__type": "Event"
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
