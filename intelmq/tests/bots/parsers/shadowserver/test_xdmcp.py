# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot

with open(os.path.join(os.path.dirname(__file__), 'xdmcp.csv')) as handle:
    EXAMPLE_FILE = handle.read()
EXAMPLE_LINES = EXAMPLE_FILE.splitlines()

with open(os.path.join(os.path.dirname(__file__),
                       'xdmcp_RECONSTRUCTED.csv')) as handle:
    RECONSTRUCTED_FILE = handle.read()
RECONSTRUCTED_LINES = RECONSTRUCTED_FILE.splitlines()

EXAMPLE_REPORT = {"feed.name": "ShadowServer XDMCP",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "netmanage", "size": "50", "status": "Linux 2.6.32-573.3.1.el6.i686", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[1], ''])),
           'source.asn': 4812,
           'source.geolocation.cc': 'CN',
           'source.geolocation.city': 'SHANGHAI',
           'source.geolocation.region': 'SHANGHAI',
           'source.ip': '61.152.122.54',
           'source.port': 177,
           'time.observation': '2016-05-17T19:04:55+00:00',
           'time.source': '2016-05-17T19:04:55+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "bimsdev1", "size": "48", "status": "0 users  load: 0.0, 0.0, 0.0", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[2], ''])),
           'source.asn': 4837,
           'source.geolocation.cc': 'CN',
           'source.geolocation.city': 'TIANJIN',
           'source.geolocation.region': 'TIANJIN',
           'source.ip': '218.68.63.240',
           'source.port': 177,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2016-05-17T19:04:56+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "zyite01", "size": "50", "status": "4 users  load: 28.2, 28.6, 28.8", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[3], ''])),
           'source.asn': 9808,
           'source.geolocation.cc': 'CN',
           'source.geolocation.city': 'HARBIN',
           'source.geolocation.region': 'HEILONGJIANG',
           'source.ip': '211.137.249.158',
           'source.port': 177,
           'time.source': '2016-05-17T19:04:56+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "PAGOS", "size": "44", "status": "Linux 3.12.55-52.42-default", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[4], ''])),
           'source.asn': 8151,
           'source.geolocation.cc': 'MX',
           'source.geolocation.city': 'MEDELLIN DE BRAVO',
           'source.geolocation.region': 'VERACRUZ',
           'source.reverse_dns': 'customer-187-174-250-38.uninet-ide.com.mx',
           'source.ip': '187.174.250.38',
           'source.port': 177,
           'time.source': '2016-05-17T19:04:57+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "linux-ws15", "size": "52", "status": "0 user, load: 0.00, 0.00, 0.00", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[5], ''])),
           'source.asn': 3549,
           'source.geolocation.cc': 'CO',
           'source.geolocation.city': 'SANTIAGO DE CALI',
           'source.geolocation.region': 'VALLE DEL CAUCA',
           'source.ip': '152.231.30.35',
           'source.port': 177,
           'time.source': '2016-05-17T19:04:57+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Unwilling", "reported_hostname": "mvodtown", "size": "51", "status": "!Display not authorized to connect", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[6], ''])),
           'source.asn': 9318,
           'source.geolocation.cc': 'KR',
           'source.geolocation.city': 'SEOUL',
           'source.geolocation.region': 'SEOUL TEUGBYEOLSI',
           'source.ip': '218.39.178.182',
           'source.port': 177,
           'time.source': '2016-05-17T19:04:57+00:00' },
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'extra': '{"opcode": "Willing", "reported_hostname": "WASWP", "size": "45", "status": "0 users  load: 0.1, 0.2, 0.2", "tag": "xdmcp"}',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[7], ''])),
           'source.asn': 38661,
           'source.geolocation.cc': 'KR',
           'source.geolocation.city': 'GURO-DONG',
           'source.geolocation.region': 'SEOUL TEUGBYEOLSI',
           'source.ip': '121.0.141.75',
           'source.port': 177,
           'time.source': '2016-05-17T19:04:57+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "VENDITTI.localdomain.net", "size": "58", "status": "Linux 2.6.32-64GB-i686", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[8], ''])),
           'source.asn': 12874,
           'source.geolocation.cc': 'IT',
           'source.geolocation.city': 'CASORIA',
           'source.geolocation.region': 'NAPOLI',
           'source.ip': '89.97.0.73',
           'source.port': 177,
           'source.reverse_dns': '89-97-0-73.ip2.fastwebnet.it',
           'time.source': '2016-05-17T19:04:58+00:00'},
          {'__type': 'Event',
           'feed.name': 'ShadowServer XDMCP',
           'classification.identifier': 'openxdmcp',
           'classification.taxonomy': 'Vulnerable',
           'classification.type': 'vulnerable service',
           'extra': '{"opcode": "Willing", "reported_hostname": "kasei", "size": "45", "status": "0 users  load: 11., 11., 11.", "tag": "xdmcp"}',
           'protocol.application': 'xdmcp',
           'protocol.transport': 'udp',
           'raw': utils.base64_encode('\n'.join([RECONSTRUCTED_LINES[0],
                                                 RECONSTRUCTED_LINES[9], ''])),
           'source.asn': 11105,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'BURNABY',
           'source.geolocation.region': 'BRITISH COLUMBIA',
           'source.ip': '209.87.31.2',
           'source.port': 177,
           'source.reverse_dns': 'kasei.cecm.sfu.ca',
           'time.source': '2016-05-17T19:04:58+00:00'}]


class TestShadowserverParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowserverParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.default_input_message = EXAMPLE_REPORT
        cls.sysconfig = {'feedname': 'Open-XDMCP'}

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
