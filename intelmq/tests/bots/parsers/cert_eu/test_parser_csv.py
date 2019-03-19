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
                  "raw": utils.base64_encode(EXAMPLE_FILE)
                  }

EXAMPLE_EVENT1 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "109.125.93.10",
    "raw": utils.base64_encode('\r\n'.join(EXAMPLE_FILE_SPLIT[:2])),
    "time.observation": "2018-01-01T01:00:00+00:00",
    "extra.cert_eu_time_observation": "2018-07-06T10:59:06+00:00",
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
    "extra.count": 6,
    "extra.datasource": "SR",
    "extra.first_seen": "2018-07-06T08:34:55.759000",
    "extra.last_seen": "2018-07-06T08:52:16.109000",
    "extra.num_sensors": "1",
    "__type": "Event"
}

EXAMPLE_EVENT2 = {
    "feed.url": "https://www.cert-eu.eu",
    "feed.name": "CERT-EU Feed",
    "source.ip": "144.76.221.34",
    "raw": utils.base64_encode('\r\n'.join((EXAMPLE_FILE_SPLIT[0],
                                            EXAMPLE_FILE_SPLIT[2]))),
    "extra.cert_eu_time_observation": "2018-07-06T11:34:53+00:00",
    "time.source": "2018-07-05T14:32:06+00:00",
    "time.observation": "2018-01-01T01:00:00+00:00",
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
    "extra.datasource": "Z",
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
