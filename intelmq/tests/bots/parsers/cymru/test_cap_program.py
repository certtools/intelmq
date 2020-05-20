# -*- coding: utf-8 -*-
import os.path
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.cymru.parser_cap_program import CymruCAPProgramParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'infected_20171031.txt')) as handle:
    RAW = handle.read()
RAW_LINES = RAW.splitlines()


REPORT = {'__type': 'Report',
          'raw': utils.base64_encode(RAW),
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENT0 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'ssh',
          'classification.type': 'brute-force',
          'protocol.application': 'ssh',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:3])),
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:00+00:00',
          }
EVENT1 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'classification.identifier': 'dns-open-resolver',
          'classification.type': 'vulnerable service',
          'protocol.application': 'dns',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:01+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[3]])),
          }
EVENT2 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:02+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[4]])),
          'classification.type': 'phishing',
          'classification.identifier': 'phishing',
          'source.url': 'http://www.example.com/',
          }
EVENT3 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:03+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[5]])),
          'classification.type': 'proxy',
          'classification.identifier': 'openproxy',
          'extra.request': 'HTTP CONNECT (8080)',
          }
EVENT4 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:04+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[6]])),
          'classification.type': 'spam',
          'classification.identifier': 'spam',
          }
EVENT5 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:05+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[7]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'conficker',
          'malware.name': 'conficker',
          'destination.ip': '172.16.0.22',
          'extra.source_port': 1337,
          }
EVENT6 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:06+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[8]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'conficker',
          'malware.name': 'conficker',
          }
EVENT7 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.asn': 64496,
          'source.ip': '172.16.0.21',
          'time.source': '2018-03-05T14:18:25+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[9]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'mirai mirai bot',
          'malware.name': 'mirai mirai bot',
          }
EVENT8 = {'__type': 'Event',
          'time.observation': '2015-11-01T00:01:45+00:05',
          'source.as_name': 'Example AS Name',
          'source.ip': '172.16.0.21',
          'time.source': '2017-10-31T10:00:05+00:00',
          'raw': utils.base64_encode('\n'.join(RAW_LINES[:2] + [RAW_LINES[10]])),
          'classification.type': 'infected-system',
          'classification.identifier': 'malwareexample',
          'malware.name': 'malwareexample',
          'destination.ip': '172.16.0.22',
          'extra.source_port': 1337,
          'event_description.text': 'Some Botnet',
          }


class TestCymruCAPProgramParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CymruCAPProgramParserBot.
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
        self.assertMessageEqual(6, EVENT6)
        self.assertMessageEqual(7, EVENT7)
        self.assertMessageEqual(8, EVENT8)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
