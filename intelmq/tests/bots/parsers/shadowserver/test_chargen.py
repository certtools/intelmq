# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'chargen.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()
with open(os.path.join(os.path.dirname(__file__), 'chargen_short.csv')) as handle:
    EXAMPLE_FILE_SHORT = handle.read()
EXAMPLE_LINE_SHORT = EXAMPLE_FILE_SHORT.splitlines()

with open(os.path.join(os.path.dirname(__file__),
                       'chargen_RECONSTRUCTED.csv')) as handle:
    RECONSTRUCTED_FILE = handle.read()
RECONSTRUCTED_LINES = RECONSTRUCTED_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Chargen",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_REPORT_SHORT = {"feed.name": "ShadowServer Chargen",
                        "raw": utils.base64_encode(EXAMPLE_FILE_SHORT),
                        "__type": "Report",
                        "time.observation": "2015-01-01T00:00:00+00:00",
                        }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer Chargen',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-chargen',
           'classification.taxonomy': 'vulnerable',
           'extra.response_size': 116,
           'extra.naics': 123456,
           'extra.tag': 'chargen',
           'extra.sic': 654321,
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[1], ''])),
           'source.asn': 12969,
           'source.geolocation.cc': 'IS',
           'source.geolocation.city': 'REYKJAVIK',
           'source.geolocation.region': 'HOFUOBORGARSVAOIO',
           'source.ip': '88.149.23.230',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Chargen',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-chargen',
           'classification.taxonomy': 'vulnerable',
           'extra.tag': 'chargen',
           'extra.response_size': 116,
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode(
               '\n'.join([EXAMPLE_LINES[0],
                          ('"2014-03-16 04:15:19","112.197.240.1","udp","19",'
                           '"","chargen","116","45543","VN","HO CHI MINH",'
                           '"THANH PHO HO CHI MINH","0","0",""'), ''])),
           'source.asn': 45543,
           'source.geolocation.cc': 'VN',
           'source.geolocation.city': 'THANH PHO HO CHI MINH',
           'source.geolocation.region': 'HO CHI MINH',
           'source.ip': '112.197.240.1',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Chargen',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-chargen',
           'classification.taxonomy': 'vulnerable',
           'extra.response_size': 116,
           'extra.tag': 'chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode(
               '\n'.join([EXAMPLE_LINES[0],
                          ('"2014-03-16 04:15:19","85.36.146.26","udp","19",'
                           '"host26-146-static.36-85-b.business.telecomitalia.it",'
                           '"chargen","116","3269","IT","LAZIO","ROMA","0","0",""'), ''])),
           'source.asn': 3269,
           'source.geolocation.cc': 'IT',
           'source.geolocation.city': 'ROMA',
           'source.geolocation.region': 'LAZIO',
           'source.ip': '85.36.146.26',
           'source.port': 19,
           'source.reverse_dns': 'host26-146-static.36-85-b.business.telecomit'
           'alia.it',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Chargen',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-chargen',
           'classification.taxonomy': 'vulnerable',
           'extra.tag': 'chargen',
           'extra.response_size': 116,
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode(
               '\n'.join([EXAMPLE_LINES[0],
                          ('"2014-03-16 04:15:19","184.69.168.237","udp","19",'
                           '"","chargen","116","6327","CA","BRITISH COLUMBIA",'
                           '"VICTORIA","0","0",""'), ''])),
           'source.asn': 6327,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'VICTORIA',
           'source.geolocation.region': 'BRITISH COLUMBIA',
           'source.ip': '184.69.168.237',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer Chargen',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'open-chargen',
           'classification.taxonomy': 'vulnerable',
           'extra.response_size': 116,
           'extra.tag': 'chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode(
               '\n'.join([EXAMPLE_LINES[0],
                          ('"2014-03-16 04:15:19","128.171.32.12","udp","19",'
                           '"dhcp-128-171-32-12.bilger.hawaii.edu","chargen",'
                           '"116","6360","US","HAWAII","HONOLULU","0","0",""'), ''])),
           'source.asn': 6360,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'HONOLULU',
           'source.geolocation.region': 'HAWAII',
           'source.ip': '128.171.32.12',
           'source.port': 19,
           'source.reverse_dns': 'dhcp-128-171-32-12.bilger.hawaii.edu',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'}]
EVENT_SHORT = {'__type': 'Event',
               'feed.name': 'ShadowServer Chargen',
               'classification.type': 'vulnerable service',
               'classification.identifier': 'open-chargen',
               'classification.taxonomy': 'vulnerable',
               'extra.tag': 'chargen',
               'protocol.application': 'chargen',
               'protocol.transport': 'udp',
               'raw': utils.base64_encode('\n'.join([EXAMPLE_LINE_SHORT[0],
                                                    '"2014-11-26 05:20:54","192.168.45.68","udp","19",'
                                                    '"","chargen","","8447","AT","3","WIEN"', ''])),
               'source.asn': 8447,
               'source.geolocation.cc': 'AT',
               'source.geolocation.city': 'WIEN',
               'source.geolocation.region': '3',
               'source.ip': '192.168.45.68',
               'source.port': 19,
               'time.source': '2014-11-26T05:20:54+00:00'}


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Open-Chargen'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)

    def test_event_short(self):
        """ Test with short header. """
        self.input_message = EXAMPLE_REPORT_SHORT
        self.allowed_warning_count = 2
        self.run_bot()
        self.assertMessageEqual(0, EVENT_SHORT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
