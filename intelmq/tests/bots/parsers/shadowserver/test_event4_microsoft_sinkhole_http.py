# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_microsoft_sinkhole_http.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'HTTP Microsoft Sinkhole IPv4',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event4_microsoft_sinkhole_http.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'HTTP Microsoft Sinkhole IPv4',
           'classification.identifier': 'necurs',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'ASHBURN',
           'destination.geolocation.region': 'VIRGINIA',
           'destination.ip': '40.121.206.97',
           'destination.port': 80,
           'destination.url': 'http://40.121.206.97/locator.php',
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'malware.name': 'necurs',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'source.asn': 8386,
           'source.geolocation.cc': 'TR',
           'source.geolocation.city': 'KEPEZ',
           'source.geolocation.region': 'ANTALYA',
           'source.ip': '31.206.1.2',
           'source.port': 49245,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-06-07T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Microsoft Sinkhole IPv4',
           'classification.identifier': 'caphaw',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.fqdn': '3fo8jrthz3y.rgk.cc',
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'REDMOND',
           'destination.geolocation.region': 'WASHINGTON',
           'destination.ip': '204.95.99.204',
           'destination.port': 443,
           'destination.url': 'http://3fo8jrthz3y.rgk.cc/index.php',
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.http_agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.6103)',
           'extra.http_referer': 'null',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517312,
           'malware.name': 'caphaw',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'source.asn': 28573,
           'source.geolocation.cc': 'BR',
           'source.geolocation.city': 'SAO PAULO',
           'source.geolocation.region': 'SAO PAULO',
           'source.ip': '177.140.3.4',
           'source.port': 35919,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-06-07T00:00:00+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Microsoft Sinkhole IPv4',
           'classification.identifier': 'necurs',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'ASHBURN',
           'destination.geolocation.region': 'VIRGINIA',
           'destination.ip': '40.121.206.97',
           'destination.port': 80,
           'destination.url': 'http://40.121.206.97/locator.php',
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517311,
           'malware.name': 'necurs',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'source.asn': 132199,
           'source.geolocation.cc': 'PH',
           'source.geolocation.city': 'MANDAUE',
           'source.geolocation.region': 'CEBU',
           'source.ip': '180.190.5.6',
           'source.port': 49264,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-06-07T00:00:01+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Microsoft Sinkhole IPv4',
           'classification.identifier': 'necurs',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'US',
           'destination.ip': '40.121.206.97',
           'destination.geolocation.city': 'ASHBURN',
           'destination.geolocation.region': 'VIRGINIA',
           'destination.port': 80,
           'destination.url': 'http://40.121.206.97/news/stream.php',
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'malware.name': 'necurs',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[4]])),
           'source.asn': 37129,
           'source.geolocation.cc': 'KE',
           'source.geolocation.city': 'NAIROBI',
           'source.geolocation.region': 'NAIROBI CITY',
           'source.ip': '197.157.7.8',
           'source.port': 55307,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-06-07T00:00:01+00:00'},
          {'__type': 'Event',
           'feed.name': 'HTTP Microsoft Sinkhole IPv4',
           'classification.identifier': 'necurs',
           'classification.taxonomy': 'malicious-code',
           'classification.type': 'infected-system',
           'destination.asn': 8075,
           'destination.geolocation.cc': 'US',
           'destination.geolocation.city': 'ASHBURN',
           'destination.geolocation.region': 'VIRGINIA',
           'destination.ip': '40.121.206.97',
           'destination.port': 80,
           'destination.url': 'http://40.121.206.97/locator.php',
           'extra.destination.naics': 334111,
           'extra.destination.sector': 'Information',
           'extra.public_source': 'MSDCU',
           'extra.source.naics': 517311,
           'extra.source.sector': 'Communications, Service Provider, and Hosting Service',
           'malware.name': 'necurs',
           'protocol.application': 'http',
           'protocol.transport': 'tcp',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[5]])),
           'source.asn': 812,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'OTTAWA',
           'source.geolocation.region': 'ONTARIO',
           'source.ip': '174.114.9.10',
           'source.port': 59000,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-06-07T00:00:01+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
