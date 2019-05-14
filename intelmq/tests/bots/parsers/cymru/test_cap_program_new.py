# -*- coding: utf-8 -*-
import os.path
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.cymru.parser_cap_program import CymruCAPProgramParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'certname_20190327.txt')) as handle:
    RAW = handle.read()
RAW_LINES = RAW.splitlines()


REPORT = {'__type': 'Report',
          'raw': utils.base64_encode(RAW),
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENT0 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-03-22T11:18:52+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[3]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'conficker',
          'malware.name': 'conficker',
          }
EVENT1 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'destination.ip': '172.16.0.22',
          'destination.port': 80,
          'time.source': '2019-03-25T03:44:22+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[4]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'nivdort',
          'malware.name': 'nivdort',
          'protocol.transport': 'tcp',
          }
EVENT2 = {'__type': 'Event',
          'time.source': '2017-10-31 10:00:00',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'ssh',
          'classification.type': 'brute-force',
          'protocol.application': 'ssh',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[5]])),
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-01-10T22:25:58+00:00',
          }

EVENT3 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'stealrat',
          'malware.name': 'stealrat',
          'classification.type': 'c2server',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-03-25T17:47:40+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[6]])),
          }
EVENT4 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'http_post',
          'malware.name': 'http_post',
          'classification.type': 'c2server',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.fqdn': 'www.pfeffer.at',
          'time.source': '2019-03-25T05:01:47+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[7]])),
          }
EVENT5 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'darknet',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'destination.port': 23,
          'time.source': '2019-03-25T17:24:06+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[8]])),
          }
EVENT51 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'darknet',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'destination.port': 2323,
          'time.source': '2019-03-25T17:24:06+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[8]])),
          }
EVENT6 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'darknet',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'destination.port': 55756,
          'time.source': '2019-03-25T04:27:11+00:00',
          'protocol.transport': 'udp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[9]])),
          }
EVENT7 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'destination.port': 22,
          'time.source': '2019-03-25T14:08:53+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[10]])),
          }
EVENT8 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-03-20T13:03:18+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[11]])),
          'classification.type': 'phishing',
          'classification.identifier': 'phishing',
          'source.url': 'http://www.example.com/',
          }
EVENT9 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.port': 34320,
          'time.source': '2019-03-25T16:00:00+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[12]])),
          'classification.type': 'proxy',
          'classification.identifier': 'openproxy',
          'protocol.application': 'http',
          }
EVENT10 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.port': 61039,
          'time.source': '2019-03-25T10:38:00+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[13]])),
          'classification.type': 'proxy',
          'classification.identifier': 'openproxy',
          'protocol.application': 'socks4',
          }
EVENT11 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-03-25T06:29:38+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[14]])),
          'classification.type': 'vulnerable service',
          'classification.identifier': 'dns-open-resolver',
          'protocol.application': 'dns',
          }

class TestCymruCAPProgramParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CymruCAPProgramParserBot with the new format.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CymruCAPProgramParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': 'Cg=='}

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        self.assertMessageEqual(0, EVENT0)
        self.assertMessageEqual(1, EVENT1)
        self.assertMessageEqual(2, EVENT2)
        self.assertMessageEqual(3, EVENT3)
        self.assertMessageEqual(4, EVENT4)
        self.assertMessageEqual(5, EVENT5)
        self.assertMessageEqual(6, EVENT51)
        self.assertMessageEqual(7, EVENT6)
        self.assertMessageEqual(8, EVENT7)
        self.assertMessageEqual(9, EVENT8)
        self.assertMessageEqual(10, EVENT9)
        self.assertMessageEqual(11, EVENT10)
        self.assertMessageEqual(12, EVENT11)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
