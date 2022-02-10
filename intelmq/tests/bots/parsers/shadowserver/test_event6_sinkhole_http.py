# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'testdata/event6_sinkhole_http.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer IPv6 Sinkhole HTTP Drone",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  "extra.file_name": "2019-01-01-event6_sinkhole_http-test-geo.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-http',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : 'serpientesyescaleras.top',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '201:70:1:332::ef',
   'destination.port' : 80,
   'destination.url' : 'http://serpientesyescaleras.top/panel/upload/waztn.cmp',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'feed.name' : 'ShadowServer IPv6 Sinkhole HTTP Drone',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJkc3RfaXAiLCJkc3RfcG9ydCIsImRzdF9hc24iLCJkc3RfZ2VvIiwiZHN0X3JlZ2lvbiIsImRzdF9jaXR5IiwiZHN0X2hvc3RuYW1lIiwiZHN0X25haWNzIiwiZHN0X3NlY3RvciIsInB1YmxpY19zb3VyY2UiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJhcHBsaWNhdGlvbiIsInZlcnNpb24iLCJldmVudF9pZCIsImh0dHBfdXJsIiwiaHR0cF9ob3N0IiwiaHR0cF9hZ2VudCIsImZvcndhcmRlZF9ieSIsInNzbF9jaXBoZXIiLCJodHRwX3JlZmVyZXIiCiIyMDIyLTAxLTA2IDAwOjAwOjAwIiwidGNwIiwiODA2OjAzZTo4OmM2MDo5Zjg6ZDhmOjBkNjo2MjQiLDU2MzU5LDgxNTEsIk1YIiwiSkFMSVNDTyIsIlpBUE9QQU4iLCwsLCwsLCIyMDE6NzA6MTozMzI6OmVmIiw4MCw2OTM5LCJVUyIsIkNBTElGT1JOSUEiLCJGUkVNT05UIiwsNTE4MjEwLCJDb21tdW5pY2F0aW9ucywgU2VydmljZSBQcm92aWRlciwgYW5kIEhvc3RpbmcgU2VydmljZSIsLCwsLCwsLCJHRVQgL3BhbmVsL3VwbG9hZC93YXp0bi5jbXAgSFRUUC8xLjEiLCJzZXJwaWVudGVzeWVzY2FsZXJhcy50b3AiLCwsLA==',
   'source.asn' : 8151,
   'source.geolocation.cc' : 'MX',
   'source.geolocation.city' : 'ZAPOPAN',
   'source.geolocation.region' : 'JALISCO',
   'source.ip' : '806:3e:8:c60:9f8:d8f:d6:624',
   'source.port' : 56359,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:00+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-http',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : '0-0-0-0-0-0-0-0-0-0-0-0-0-5-0-0-0-0-0-0-0-0-0-0-0-0-0.info',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '201:70:1:332::ef',
   'destination.port' : 80,
   'destination.url' : 'http://0-0-0-0-0-0-0-0-0-0-0-0-0-5-0-0-0-0-0-0-0-0-0-0-0-0-0.info/DATA',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.infection' : 'tsifiri',
   'extra.http_agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; Zoom 3.6.0)',
   'extra.source.naics' : 517312,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'feed.name' : 'ShadowServer IPv6 Sinkhole HTTP Drone',
   'malware.name' : 'tsifiri',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJkc3RfaXAiLCJkc3RfcG9ydCIsImRzdF9hc24iLCJkc3RfZ2VvIiwiZHN0X3JlZ2lvbiIsImRzdF9jaXR5IiwiZHN0X2hvc3RuYW1lIiwiZHN0X25haWNzIiwiZHN0X3NlY3RvciIsInB1YmxpY19zb3VyY2UiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJhcHBsaWNhdGlvbiIsInZlcnNpb24iLCJldmVudF9pZCIsImh0dHBfdXJsIiwiaHR0cF9ob3N0IiwiaHR0cF9hZ2VudCIsImZvcndhcmRlZF9ieSIsInNzbF9jaXBoZXIiLCJodHRwX3JlZmVyZXIiCiIyMDIyLTAxLTA2IDAwOjAwOjAwIiwidGNwIiwiNDAyOjAwOjNhNjpmYTY6NTk4OmIzNTplNzE6MjU4Iiw1MjMzMiw3NTUyLCJWTiIsIkhPIENISSBNSU5IIiwiVEhBTkggUEhPIEhPIENISSBNSU5IIiwsNTE3MzEyLCJDb21tdW5pY2F0aW9ucywgU2VydmljZSBQcm92aWRlciwgYW5kIEhvc3RpbmcgU2VydmljZSIsLCwsIjIwMTo3MDoxOjMzMjo6ZWYiLDgwLDY5MzksIlVTIiwiQ0FMSUZPUk5JQSIsIkZSRU1PTlQiLCw1MTgyMTAsIkNvbW11bmljYXRpb25zLCBTZXJ2aWNlIFByb3ZpZGVyLCBhbmQgSG9zdGluZyBTZXJ2aWNlIiwsInRzaWZpcmkiLCJ0c2lmaXJpIiwsLCwsIkdFVCAvREFUQSBIVFRQLzEuMSIsIjAtMC0wLTAtMC0wLTAtMC0wLTAtMC0wLTAtNS0wLTAtMC0wLTAtMC0wLTAtMC0wLTAtMC0wLmluZm8iLCJNb3ppbGxhLzQuMCAoY29tcGF0aWJsZTsgTVNJRSA3LjA7IFdpbmRvd3MgTlQgNi4yOyBXT1c2NDsgVHJpZGVudC83LjA7IC5ORVQ0LjBDOyAuTkVUNC4wRTsgLk5FVCBDTFIgMi4wLjUwNzI3OyAuTkVUIENMUiAzLjAuMzA3Mjk7IC5ORVQgQ0xSIDMuNS4zMDcyOTsgSW5mb1BhdGguMzsgWm9vbSAzLjYuMCkiLCws',
   'source.asn' : 7552,
   'source.geolocation.cc' : 'VN',
   'source.geolocation.city' : 'THANH PHO HO CHI MINH',
   'source.geolocation.region' : 'HO CHI MINH',
   'source.ip' : '402:0:3a6:fa6:598:b35:e71:258',
   'source.port' : 52332,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:00+00:00'
},
{
   '__type' : 'Event',
   'classification.identifier' : 'sinkhole-http',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : 'gaghpaheiafhjefijs.top',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '201:70:1:332::ef',
   'destination.port' : 80,
   'destination.url' : 'http://gaghpaheiafhjefijs.top/7',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.infection' : 'phorpiex',
   'extra.tag': 'trik,phorpiex',
   'extra.http_agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
   'feed.name' : 'ShadowServer IPv6 Sinkhole HTTP Drone',
   'malware.name' : 'phorpiex',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : 'InRpbWVzdGFtcCIsInByb3RvY29sIiwic3JjX2lwIiwic3JjX3BvcnQiLCJzcmNfYXNuIiwic3JjX2dlbyIsInNyY19yZWdpb24iLCJzcmNfY2l0eSIsInNyY19ob3N0bmFtZSIsInNyY19uYWljcyIsInNyY19zZWN0b3IiLCJkZXZpY2VfdmVuZG9yIiwiZGV2aWNlX3R5cGUiLCJkZXZpY2VfbW9kZWwiLCJkc3RfaXAiLCJkc3RfcG9ydCIsImRzdF9hc24iLCJkc3RfZ2VvIiwiZHN0X3JlZ2lvbiIsImRzdF9jaXR5IiwiZHN0X2hvc3RuYW1lIiwiZHN0X25haWNzIiwiZHN0X3NlY3RvciIsInB1YmxpY19zb3VyY2UiLCJpbmZlY3Rpb24iLCJmYW1pbHkiLCJ0YWciLCJhcHBsaWNhdGlvbiIsInZlcnNpb24iLCJldmVudF9pZCIsImh0dHBfdXJsIiwiaHR0cF9ob3N0IiwiaHR0cF9hZ2VudCIsImZvcndhcmRlZF9ieSIsInNzbF9jaXBoZXIiLCJodHRwX3JlZmVyZXIiCiIyMDIyLTAxLTA2IDAwOjAwOjAwIiwidGNwIiwiMDAxOmIxOjRiOjQ5OjVlZDpkYzA6MTA1OjgyMyIsNTM0NDUsMTc1NTIsIlRIIiwiVUJPTiBSQVRDSEFUSEFOSSIsIldBUklOIENIQU1SQVAiLCwsLCwsLCIyMDE6NzA6MTozMzI6OmVmIiw4MCw2OTM5LCJVUyIsIkNBTElGT1JOSUEiLCJGUkVNT05UIiwsNTE4MjEwLCJDb21tdW5pY2F0aW9ucywgU2VydmljZSBQcm92aWRlciwgYW5kIEhvc3RpbmcgU2VydmljZSIsLCJwaG9ycGlleCIsInBob3JwaWV4IiwidHJpayxwaG9ycGlleCIsLCwsIkdFVCAvNyBIVFRQLzEuMSIsImdhZ2hwYWhlaWFmaGplZmlqcy50b3AiLCJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjo2Ny4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzY3LjAiLCws',
   'source.asn' : 17552,
   'source.geolocation.cc' : 'TH',
   'source.geolocation.city' : 'WARIN CHAMRAP',
   'source.geolocation.region' : 'UBON RATCHATHANI',
   'source.ip' : '1:b1:4b:49:5ed:dc0:105:823',
   'source.port' : 53445,
   'time.observation' : '2015-01-01T00:00:00+00:00',
   'time.source' : '2022-01-06T00:00:00+00:00'
}
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
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
