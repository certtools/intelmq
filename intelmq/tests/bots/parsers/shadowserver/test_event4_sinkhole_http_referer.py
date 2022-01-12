# SPDX-FileCopyrightText: 2021 Mikk Margus Möll <mikk@cert.ee>
#
# SPDX-License-Identifier: AGPL-3.0-or-later
# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'testdata/event4_sinkhole_http_referer.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

EXAMPLE_REPORT = {'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2021-03-05T00:00:00+00:00",
                  "extra.file_name": "2021-03-04-event4_sinkhole_http_referer.csv",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
           'classification.identifier': 'sinkhole-http-referer',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.asn': 60781,
           'destination.fqdn': '12106.mobapptrack.com',
           'destination.geolocation.cc': 'NL',
           'destination.geolocation.city': 'AMSTERDAM',
           'destination.geolocation.region': 'NOORD-HOLLAND',
           'destination.ip': '85.17.31.82',
           'destination.port': 80,
           'destination.url': 'http://12106.mobapptrack.com/favicon.ico',
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting Service',
           'extra.event_id': '1614816002',
           'extra.family': 'kovter',
           'extra.http_referer': 'http://12106.mobapptrack.com/click/redirect?feed_id=12106&sub_id=7&q=8A5491983C8FBE7743E2D2C36E45EBC4-18307118D2626C9BD756B3F09D14BB910E381EE4',
           'extra.http_referer_asn': 28753,
           'extra.http_referer_city': 'FRANKFURT AM MAIN',
           'extra.http_referer_geo': 'DE',
           'extra.http_referer_hostname': '12106.mobapptrack.com',
           'extra.http_referer_ip': '178.162.203.211',
           'extra.http_referer_naics': 518210,
           'extra.http_referer_port': '80',
           'extra.http_referer_region': 'HESSEN',
           'extra.http_referer_sector': 'Communications, Service Provider, and Hosting '
                                        'Service',
           'extra.protocol': 'tcp',
           'extra.tag': 'kovter',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[1]])),
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2021-03-04T00:00:02+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'sinkhole-http-referer',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.asn': 28753,
           'destination.fqdn': 'freescanonline.com',
           'destination.geolocation.cc': 'DE',
           'destination.geolocation.city': 'FRANKFURT AM MAIN',
           'destination.geolocation.region': 'HESSEN',
           'destination.port': 80,
           'destination.url': 'http://freescanonline.com/animalally.com',
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting '
                                       'Service',
           'destination.ip': '178.162.1.2',
           'extra.event_id': '1614816011',
           'extra.family': 'sunburst',
           'extra.http_referer': 'http://x.noizm.com/jump.php?u=http://freescanonline.com/animalally.com',
           'extra.http_referer_asn': 9370,
           'extra.http_referer_city': 'OSAKA',
           'extra.http_referer_geo': 'JP',
           'extra.http_referer_hostname': 'x.noizm.com',
           'extra.http_referer_naics': 518210,
           'extra.http_referer_port': '80',
           'extra.http_referer_ip': '59.106.1.2',
           'extra.http_referer_region': 'OSAKA',
           'extra.http_referer_sector': 'Communications, Service Provider, and Hosting '
                                        'Service',
           'extra.protocol': 'tcp',
           'extra.tag': 'sunburst',
           'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[2]])),
           'time.source': '2021-03-04T00:00:11+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'sinkhole-http-referer',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.asn': 28753,
           'destination.fqdn': 'rxrtb.bid',
           'destination.geolocation.cc': 'DE',
           'destination.geolocation.city': 'FRANKFURT AM MAIN',
           'destination.geolocation.region': 'HESSEN',
           'destination.port': 80,
           'destination.url': 'http://rxrtb.bid/getjs?r=0.6393021999392658',
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting '
                                       'Service',
           'destination.ip': '178.162.1.2',
           'extra.event_id': '1614816012',
           'extra.family': 'kovter',
           'extra.http_referer': 'http://x.blogspot.com/',
           'extra.http_referer_ip': '142.250.3.4',
           'extra.http_referer_asn': 15169,
           'extra.http_referer_city': 'MOUNTAIN VIEW',
           'extra.http_referer_geo': 'US',
           'extra.http_referer_hostname': 'x.blogspot.com',
           'extra.http_referer_naics': 519130,
           'extra.http_referer_port': '80',
           'extra.http_referer_region': 'CALIFORNIA',
           'extra.http_referer_sector': 'Communications, Service Provider, and Hosting '
                                        'Service',
           'extra.protocol': 'tcp',
           'extra.tag': 'kovter',
           'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[3]])),
           'time.source': '2021-03-04T00:00:12+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'sinkhole-http-referer',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.asn': 60781,
           'destination.fqdn': 'freescanonline.com',
           'destination.geolocation.cc': 'NL',
           'destination.geolocation.city': 'AMSTERDAM',
           'destination.geolocation.region': 'NOORD-HOLLAND',
           'destination.ip': '5.79.71.225',
           'destination.port': 80,
           'destination.url': 'http://freescanonline.com/personalationmall.com',
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting '
                                       'Service',
           'extra.event_id': '1614816013',
           'extra.family': 'sunburst',
           'extra.http_referer': 'http://www.example.com/teams/default.asp?u=EKL&t=c&s=lacrosse&p=remote&url=http://freescanonline.com/personalationmall.com',
           'extra.http_referer_asn': 14618,
           'extra.http_referer_city': 'ASHBURN',
           'extra.http_referer_geo': 'US',
           'extra.http_referer_hostname': 'www.example.com',
           'extra.http_referer_ip': '34.232.5.6',
           'extra.http_referer_naics': 454110,
           'extra.http_referer_port': '80',
           'extra.http_referer_region': 'VIRGINIA',
           'extra.http_referer_sector': 'Retail Trade',
           'extra.protocol': 'tcp',
           'extra.tag': 'sunburst',
           'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[4]])),
           'time.source': '2021-03-04T00:00:13+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'sinkhole-http-referer',
           'classification.taxonomy': 'other',
           'classification.type': 'other',
           'destination.asn': 60781,
           'destination.fqdn': 'freescanonline.com',
           'destination.geolocation.cc': 'NL',
           'destination.geolocation.city': 'AMSTERDAM',
           'destination.geolocation.region': 'NOORD-HOLLAND',
           'destination.port': 80,
           'destination.url': 'http://freescanonline.com/raftcomply.com',
           'extra.destination.naics': 518210,
           'extra.destination.sector': 'Communications, Service Provider, and Hosting '
                                       'Service',
           'destination.ip': '5.79.1.2',
           'extra.event_id': '1614816086',
           'extra.family': 'sunburst',
           'extra.http_referer': 'http://x.communes.jp/?url=http://freescanonline.com/raftcomply.com',
           'extra.http_referer_asn': 2516,
           'extra.http_referer_city': 'SAPPORO',
           'extra.http_referer_geo': 'JP',
           'extra.http_referer_hostname': 'x.communes.jp',
           'extra.http_referer_ip': '210.172.7.8',
           'extra.http_referer_naics': 517312,
           'extra.http_referer_port': '80',
           'extra.http_referer_region': 'HOKKAIDO',
           'extra.http_referer_sector': 'Communications, Service Provider, and Hosting '
                                        'Service',
           'extra.protocol': 'tcp',
           'extra.tag': 'sunburst',
           'feed.name': 'Sinkhole-Events-HTTP-Referer IPv4',
           'raw': utils.base64_encode('\n'.join([EXAMPLE_LINES[0],
                                                 EXAMPLE_LINES[5]])),
           'time.source': '2021-03-04T00:01:26+00:00'}]


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
