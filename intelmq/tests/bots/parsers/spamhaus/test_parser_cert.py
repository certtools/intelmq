# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.spamhaus.parser_cert import SpamhausCERTParserBot


with open(os.path.join(os.path.dirname(__file__), 'cert.txt')) as handle:
    FILE = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                              "<CERTNAME>&key=<APIKEY>",
                  'raw': utils.base64_encode(FILE),
                  "__type": "Report",
                  "feed.name": "Spamhaus Cert",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT_TEMPL = {"feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                           "<CERTNAME>&",
               "feed.name": "Spamhaus Cert",
               "__type": "Event",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
EXAMPLE_EVENTS_PARTS = [{'raw': 'MTA5LjEyNi42NC4yLEFTMTI2MzUsQVQsMTQ0MTAwODk3M'
                                'Cxhc3Byb3gsLCwyNSwsdGNw',
                         'source.ip': '109.126.64.2',
                         'source.asn': 12635,
                         'time.source': '2015-08-31T08:16:10+00:00',
                         'malware.name': 'asprox',
                         'destination.port': 25,
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'raw': 'MTA5LjkwLjIzMy4xOSxBUzY4MzAsQVQsMTQ0MTAwODM1M'
                                'SxwYXRjaGVyLGR4eHQuc2lua2hvbGUuZGssMjEyLjIyNy'
                                '4yMC4xOSw4MCwxMDM2LHRjcA==',
                         'source.ip': '109.90.233.19',
                         'source.asn': 6830,
                         'time.source': '2015-08-31T08:05:51+00:00',
                         'malware.name': 'patcher',
                         'destination.port': 80,
                         'destination.fqdn': 'dxxt.sinkhole.dk',
                         'destination.ip': '212.227.20.19',
                         'extra': '{"destination.local_port": 1036}',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'raw': 'MTA5LjkxLjAuMjI3LEFTNjgzMCxBVCwxNDQxMDExNjU3L'
                                'GNvbmZpY2tlciwyMTYuNjYuMTUuMTA5LDIxNi42Ni4xNS'
                                '4xMDksODAsMTQzMCx0Y3A=',
                         'source.ip': '109.91.0.227',
                         'source.asn': 6830,
                         'time.source': '2015-08-31T09:00:57+00:00',
                         'malware.name': 'conficker',
                         'destination.port': 80,
                         'destination.ip': '216.66.15.109',
                         'extra': '{"destination.local_port": 1430}',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'raw': 'MTExLjExMS4xMTEuMTgzLEFTMTExNzgsTFYsMTQ3MTExMTEzOSxpb3RtaXJhaSwtLD8sPyw/LD8=',
                         'source.ip': '111.111.111.183',
                         'source.asn': 11178,
                         'time.source': '2016-08-13T17:58:59+00:00',
                         'malware.name': 'iotmirai',
                         'source.geolocation.cc': 'LV',
                         },
                        {'raw': 'MTExLjExMS4xMTEuMjMwLEFTMTExNzgsTFYsMTQ3MTExMTEzNCxnb290a2l0LCwxMTEuMTExLjExMS4xNjYsMTY5Nix4eHh4eHh4eHh4eC5jb20sdGNw',
                         'source.ip': '111.111.111.230',
                         'source.asn': 11178,
                         'time.source': '2016-08-13T17:58:54+00:00',
                         'malware.name': 'gootkit',
                         'destination.ip': '111.111.111.166',
                         'destination.fqdn': 'xxxxxxxxxxx.com',
                         'destination.port': 1696,
                         'source.geolocation.cc': 'LV',
                         'protocol.transport': 'tcp',
                         }]


class TestSpamhausCERTParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for SpamhausCERTParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = SpamhausCERTParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        for position, event in enumerate(EXAMPLE_EVENTS_PARTS):
            event.update(EVENT_TEMPL)
            self.assertMessageEqual(position, event)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
