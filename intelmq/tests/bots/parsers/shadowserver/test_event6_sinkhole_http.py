# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[1]])),
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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[2]])),
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
   'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                     EXAMPLE_LINES[3]])),
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
