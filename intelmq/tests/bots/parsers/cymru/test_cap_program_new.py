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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
          }
EVENT4 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'http_post',
          'malware.name': 'http_post',
          'classification.type': 'c2server',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.fqdn': 'www.example.com',
          'time.source': '2019-03-25T05:01:47+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[7]])),
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
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
          'source.geolocation.cc': 'AT',
          }
EVENT12 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-09-11T08:05:00+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[15]])),
          'classification.type': 'proxy',
          'classification.identifier': 'openproxy',
          'protocol.application': 'httppost',
          'source.geolocation.cc': 'AT',
          }
EVENT13 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'extra.source_port': 61458,
          'time.source': '2019-09-11T16:39:57+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[16]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'conficker',
          'malware.name': 'conficker',
          'destination.ip': '172.16.0.22',
          'source.geolocation.cc': 'AT',
          }
EVENT14 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.port': 15390,
          'destination.ip': '172.16.0.22',
          'destination.port': 80,
          'time.source': '2019-09-11T00:31:30+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[17]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'azorult',
          'malware.name': 'azorult',
          'protocol.transport': 'tcp',
          'source.geolocation.cc': 'AT',
          }
EVENT15 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.port': 53488,
          'source.ip': '172.16.0.21',
          'destination.port': 445,
          'time.source': '2019-09-11T11:07:58+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[18]])),
          'source.geolocation.cc': 'AT',
          }
EVENT16 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'darknet',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.port': 23365,
          'source.ip': '172.16.0.21',
          'destination.port': 23,
          'time.source': '2019-09-11T11:57:37+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[19]])),
          'source.geolocation.cc': 'AT',
          }
EVENT17 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'darknet',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.port': 3,
          'source.ip': '172.16.0.21',
          'destination.port': 3,
          'time.source': '2019-09-11T00:49:45+00:00',
          'protocol.transport': 'icmp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[20]])),
          'source.geolocation.cc': 'AT',
          }
EVENT18 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2019-09-12T07:01:00+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[21]])),
          'classification.type': 'proxy',
          'classification.identifier': 'openproxy',
          'protocol.application': 'socks4',
          'source.geolocation.cc': 'AT',
          }
EVENT19 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.port': 53912,
          'time.source': '2019-09-17T02:58:48+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[22]])),
          'classification.type': 'scanner',
          'classification.identifier': 'scanner',
          'protocol.transport': 'tcp',
          'source.geolocation.cc': 'AT',
          }
EVENT20 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'source.fqdn': 'sub.example.com',
          'source.port': 80,
          'time.source': '2019-09-22T05:39:38+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[23]])),
          'classification.identifier': 'http_post',
          'malware.name': 'http_post',
          'classification.type': 'c2server',
          'source.geolocation.cc': 'AT',
          }
EVENT21 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.type': 'scanner',
          'classification.identifier': 'scanner',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.port': 55133,
          'source.ip': '172.16.0.21',
          'destination.port': 57518,
          'time.source': '2019-09-19T00:03:13+00:00',
          'protocol.transport': 'tcp',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[24]])),
          'source.geolocation.cc': 'AT',
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
        self.assertMessageEqual(13, EVENT12)
        self.assertMessageEqual(14, EVENT13)
        self.assertMessageEqual(15, EVENT14)
        self.assertMessageEqual(16, EVENT15)
        self.assertMessageEqual(17, EVENT16)
        self.assertMessageEqual(18, EVENT17)
        self.assertMessageEqual(19, EVENT18)
        self.assertMessageEqual(20, EVENT19)
        self.assertMessageEqual(21, EVENT20)
        self.assertMessageEqual(22, EVENT21)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
