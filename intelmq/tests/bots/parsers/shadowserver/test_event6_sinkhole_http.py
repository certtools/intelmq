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

EXAMPLE_REPORT = {"feed.name": "Sinkhole-Events-HTTP IPv6",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-event6_sinkhole_http-test-geo.csv",
                  }
EVENTS = [
{
   '__type' : 'Event',
   'classification.identifier' : '3ve',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : 'devps.net',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '2001:470:1:332::fe',
   'destination.port' : 80,
   'destination.url' : 'http://devps.net/QKMSvF2hl11j%2fbMkyPbF5EpHYhd6VWTG4u19K3Rt7JGU3lMYRqpq8wPYEuOGKKeidKW3pefVfKSjBnL0cXizZbmuWWu8AQNRqw5g9Ny5vZtiv638XKoWwCLuUOTISTV%2fLcpcS1%2f22NjWqgXkHGISAuyVtafqyCC%2f5cA0eYg9Me8VzAIFDdTArogQOdYhElf2xluhEFPsstGQ%2bwrM4VmKHJpzyjD7Y%2fN%2bQV3wnZNdVkEVk1k2iKBJkotYv3ajgYWr56xxCbY5vE1IpZBRNhhaUDNZo0kJgi%2b6knXZ4m7JHt%2fGtJeP%2bNTxHSUL2ELlTIiT3ENlPYD6FdH6ZBxT1OneW%2f0ih%2fcN7vctb5B5Qwa1ez7ZjN2QxgBYkFDDHHTs42ej5eF2BysWAQDSUr%2fcySyGxcfPveIpfQEdrynGKR6z3OYqkFnP%2bYRDQp2rt1qt0FwCB4L9cg05TQlSSTJVGfPDrtcqjvKY4c9hWwSHtE8jMRpeCYO4Es%2bWgwr5DjzMicmuZo%2f4Ycr16jpN7xlDJdJ8iCFZxbSGgVC7ksVlGE8wlfWPI4KTuX5U5s61eNWPTlAC%2fOGb8grtw%2ffzizoIX9D6ZUMvslGLQIp%2fvNmNQkZy8HhNoV6Lns%2figITP%2fpN0H8h9HjUTl9qn65xFOEVpc0motSy8alcTPtTRKq5Jvc4Ao0x3N%2fvCB1v4Epx7XC0UpFbw8TrYEvAczEfGsGM',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.http_agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
   'extra.infection' : 'boaxxe',
   'extra.tag' : '3ve',
   'feed.name' : 'Sinkhole-Events-HTTP IPv6',
   'malware.name' : 'boaxxe',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 7713,
   'source.geolocation.cc' : 'ID',
   'source.geolocation.city' : 'JAKARTA',
   'source.geolocation.region' : 'JAKARTA RAYA',
   'source.ip' : '2001:448a:1082:4d9b:7491:bf9e:3d5f:a634',
   'source.port' : 49431,
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2022-03-02T09:14:19+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : '3ve',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : 'devps.net',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '2001:470:1:332::ef',
   'destination.port' : 80,
   'destination.url' : 'http://devps.net/QKMSvF2hl11j%2fbMkyPbF5EpHYhd6VWTG4u19K3Rt7JGU3lMYRqpq8wPYEuOGKKeidKW3pefVfKSjBnL0cXizZbmuWWu8AQNRqw5g9Ny5vZtiv638XKoWwCLuUOTISTV%2fLcpcS1%2f22NjWqgXkHGISAuyVtafqyCC%2f5cA0eYg9Me8VzAIFDdTArogQOdYhElf2xluhEFPsstGQ%2bwrM4VmKHJpzyjD7Y%2fN%2bQV3wnZNdVkEVk1k2iKBJkotYv3ajgYWr56xxCbY5vE1IpZBRNhhaUDNZo0kJgi%2b6knXZ4m7JHt%2fGtJeP%2bNTxHSUL2ELlTIiT3ENlPYD6FdH6ZBxT1OneW%2f0ih%2fcN7vctb5B5Qwa1ez7ZjN2QxgBYkFDDHHTs42ej5eF2BysWAQDSUr%2fcySyGxcfPveIpfQEdrynGKR6z3OYqkFnP%2bYRDQp2rt1qt0FwCB4L9cg05TQlSSTJVGfPDrtcqjvKY4c9hWwSHtE8jMRpeCYO4Es%2bWgwr5DjzMicmuZo%2f4Ycr16jpN7xlDJdJ8iCFZxbSGgVC7ksVlGE8wlfWPI4KTuX5U5s61eNWPTlAC%2fOGb8grtw%2ffzizoIX9D6ZUMvslGLQIp%2fvNmNQkZy8HhNoV6Lns%2figITP%2fpN0H8h9HjUTl9qn65xFOEVpc0motSy8alcTPtTRKq5Jvc4Ao0x3N%2fvCB1v4Epx7XC0UpFbw8TrYEvAczEfGsGM',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.http_agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
   'extra.infection' : 'boaxxe',
   'extra.tag' : '3ve',
   'feed.name' : 'Sinkhole-Events-HTTP IPv6',
   'malware.name' : 'boaxxe',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 7713,
   'source.geolocation.cc' : 'ID',
   'source.geolocation.city' : 'JAKARTA',
   'source.geolocation.region' : 'JAKARTA RAYA',
   'source.ip' : '2001:448a:1082:4d9b:7491:bf9e:3d5f:a634',
   'source.port' : 49460,
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2022-03-02T09:15:10+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : '3ve',
   'classification.taxonomy' : 'malicious-code',
   'classification.type' : 'infected-system',
   'destination.asn' : 6939,
   'destination.fqdn' : 'devps.net',
   'destination.geolocation.cc' : 'US',
   'destination.geolocation.city' : 'FREMONT',
   'destination.geolocation.region' : 'CALIFORNIA',
   'destination.ip' : '2001:470:1:332::fe',
   'destination.port' : 80,
   'destination.url' : 'http://devps.net/WMoUNCvuKGzdqSCeQcadP1%2f0B%2f3bzpOmyKBU85Z25HVOhvDQUPFl%2fk8uOcLewS%2b1BsuHXalRAOIgGOYYs2igj6UX8FkdCAmDewWPvfDhPD45nwd2tx1lLf2IoIfuOtIpGR6bN5Q6hGpSBgfERqCa0ImHcwfcZ2EdO%2fWvg7R8H6SLcTiuUC0I4pzvlWt1CRLgLdIEU1hZ0nnFHIHhchb6D7ITEgBQ2chQDxy5TJMrGjm4Dac6dKl%2ft5uYhRhSjAHkLLtgrJjsqVtVbelTAkt5kdcqLlO09m1SH%2fvtAb%2fOvR2DbhBss7%2f64DG7g6cAnghNA6JrFn1uW7sw%2bnKH8koKQwzUjdSsbrQAvmg4r0KDDW8Diq64gfDzxFWkzCLOYifc%2fwlinXPCl7aJiNCoieDC1U98RNQg%2f5td4SZmJnDQ2%2f96CPbFeSpCez5WD1rCjrxLj1h2cqzIgkydEWACceWP9ztxc4QaObzEcgOGxbRckWC7H2aaLeT8jaYEYdKi1pwEKChSL3YdEt4ZIb2IFrWwzNaXEpQzFXf07f902OEdI9vVA1ZdEOBPG6rAIkzMdebfprfVyhKEWtrCd3Skg3COUFtRQks5jzG1nv4sVGijTfSgyn6xE9Taka668Nycik6nmHy8Huj3oC01j3tee%2f1Z3eI6tV7lgM5d3uFJ84slRGHUCwMfVozOGmZRwNo%2fz%2bA',
   'extra.destination.naics' : 518210,
   'extra.destination.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.http_agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
   'extra.infection' : 'boaxxe',
   'extra.source.naics' : 517311,
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : '3ve',
   'feed.name' : 'Sinkhole-Events-HTTP IPv6',
   'malware.name' : 'boaxxe',
   'protocol.application' : 'http',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 11427,
   'source.geolocation.cc' : 'US',
   'source.geolocation.city' : 'GARLAND',
   'source.geolocation.region' : 'TEXAS',
   'source.ip' : '2603:8080:b20a:dc00:f06e:8304:71f6:27e2',
   'source.port' : 62932,
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2022-03-02T14:15:10+00:00'
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
