# SPDX-FileCopyrightText: 2022 Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/scan_docker.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Accessible Docker Service',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2010-02-10T00:00:00+00:00",
                  "extra.file_name": "2010-02-10-scan_docker-test.csv",
                  }
EVENTS = [
        {
   '__type' : 'Event',
   'classification.identifier' : 'open-docker',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.api_version' : '1.37',
   'extra.arch' : 'amd64',
   'extra.build_time' : '2018-05-09T22:18:36.000000000+00:00',
   'extra.content_type' : 'application/json; charset=UTF-8',
   'extra.date' : 'Fri, 06 May 2022 14:06:30 GMT',
   'extra.experimental' : 'false',
   'extra.git_commit' : 'f150324',
   'extra.go_version' : 'go1.9.5',
   'extra.http' : 'HTTP/1.1',
   'extra.http_code' : 200,
   'extra.http_reason' : 'OK',
   'extra.kernel_version' : '3.10.0-514.26.2.el7.x86_64',
   'extra.min_api_version' : '1.12',
   'extra.os.name' : 'linux',
   'extra.server' : 'Docker/18.05.0-ce (linux)',
   'extra.source.sector' : 'Communications, Service Provider, and Hosting Service',
   'extra.tag' : 'docker',
   'extra.version' : '18.05.0-ce',
   'feed.name' : 'Accessible Docker Service',
   'protocol.application' : 'docker',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[1]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.1',
   'source.port' : 2375,
   'source.reverse_dns' : 'node01.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:00+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-docker',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.api_version' : '1.26',
   'extra.arch' : 'amd64',
   'extra.build_time' : '2022-03-02T15:25:43.414574467+00:00',
   'extra.content_type' : 'application/json',
   'extra.date' : 'Fri, 06 May 2022 14:08:07 GMT',
   'extra.experimental' : 'false',
   'extra.git_commit' : '7d71120/1.13.1',
   'extra.go_version' : 'go1.10.3',
   'extra.http' : 'HTTP/1.1',
   'extra.http_code' : 200,
   'extra.http_reason' : 'OK',
   'extra.kernel_version' : '3.10.0-693.2.2.el7.x86_64',
   'extra.min_api_version' : '1.12',
   'extra.os.name' : 'linux',
   'extra.pkg_version' : 'docker-1.13.1-209.git7d71120.el7.centos.x86_64',
   'extra.server' : 'Docker/1.13.1 (linux)',
   'extra.tag' : 'docker',
   'extra.version' : '1.13.1',
   'feed.name' : 'Accessible Docker Service',
   'protocol.application' : 'docker',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[2]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.2',
   'source.port' : 2375,
   'source.reverse_dns' : 'node02.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:01+00:00'
},

{
   '__type' : 'Event',
   'classification.identifier' : 'open-docker',
   'classification.taxonomy' : 'vulnerable',
   'classification.type' : 'vulnerable-system',
   'extra.api_version' : '1.37',
   'extra.arch' : 'amd64',
   'extra.build_time' : '2018-05-09T22:18:36.000000000+00:00',
   'extra.content_type' : 'application/json; charset=UTF-8',
   'extra.date' : 'Fri, 06 May 2022 14:08:06 GMT',
   'extra.experimental' : 'false',
   'extra.git_commit' : 'f150324',
   'extra.go_version' : 'go1.9.5',
   'extra.http' : 'HTTP/1.1',
   'extra.http_code' : 200,
   'extra.http_reason' : 'OK',
   'extra.kernel_version' : '3.10.0-514.26.2.el7.x86_64',
   'extra.min_api_version' : '1.12',
   'extra.os.name' : 'linux',
   'extra.server' : 'Docker/18.05.0-ce (linux)',
   'extra.tag' : 'docker',
   'extra.version' : '18.05.0-ce',
   'feed.name' : 'Accessible Docker Service',
   'protocol.application' : 'docker',
   'protocol.transport' : 'tcp',
   'raw' : utils.base64_encode('\n'.join([EXAMPLE_LINES[0], EXAMPLE_LINES[3]])),
   'source.asn' : 64512,
   'source.geolocation.cc' : 'ZZ',
   'source.geolocation.city' : 'City',
   'source.geolocation.region' : 'Region',
   'source.ip' : '192.168.0.3',
   'source.port' : 2375,
   'source.reverse_dns' : 'node03.example.com',
   'time.observation' : '2010-02-10T00:00:00+00:00',
   'time.source' : '2010-02-10T00:00:02+00:00'
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
