# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_ssdp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Open SSDP',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-scan_ssdp-test-geo.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Open SSDP',
           "classification.identifier": "open-ssdp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.cache_control": "max-age=1800",
           "extra.header": "HTTP/1.1 200 OK",
           "extra.location": "http://198.123.245.1:52869/gatedesc.xml",
           "extra.naics": 517311,
           "extra.search_target": "upnp:rootdevice",
           "extra.server": "Linux, UPnP/1.0, Portable SDK for UPnP devices/1.6.6",
           "extra.systime": "Fri, 16 Jan 1970 00:05:23 GMT",
           "extra.tag": "ssdp",
           "extra.unique_service_name": "uuid:20809696-105a-3721-e8b8-2c957f6259fe::upnp:rootdevice",
           "protocol.application": "ssdp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.171",
           "source.port": 32822,
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T07:13:42+00:00"
          },
          {'__type': 'Event',
           'feed.name': 'Open SSDP',
           "classification.identifier": "open-ssdp",
           "classification.taxonomy": "vulnerable",
           "classification.type": "vulnerable service",
           "extra.cache_control": "max-age=1800",
           "extra.header": "HTTP/1.1 200 OK",
           "extra.location": "http://198.123.245.1:52869/gatedesc.xml",
           "extra.naics": 517311,
           "extra.search_target": "upnp:rootdevice",
           "extra.server": "Linux/2.6.20-Amazon_SE, UPnP/1.0, Intel SDK for UPnP devices /1.2",
           "extra.systime": "Thu, 20 Jan 2000 12:14:46 GMT",
           "extra.tag": "ssdp",
           "extra.unique_service_name": "uuid:160a0200-ac91-4b05-8adf-f5ccc5a5ebaa::upnp:rootdevice",
           "protocol.application": "ssdp",
           "protocol.transport": "udp",
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           "source.asn": 5678,
           "source.geolocation.cc": "AA",
           "source.geolocation.city": "LOCATION",
           "source.geolocation.region": "LOCATION",
           "source.ip": "198.123.245.237",
           "source.port": 32818,
           "source.reverse_dns": "localhost.localdomain",
           "time.observation": "2015-01-01T00:00:00+00:00",
           "time.source": "2019-09-04T07:13:50+00:00",
          }]


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
