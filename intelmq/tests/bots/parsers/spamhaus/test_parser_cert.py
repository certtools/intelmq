# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.spamhaus.parser_cert import SpamhausCERTParserBot


with open(os.path.join(os.path.dirname(__file__), 'cert.txt')) as handle:
    FILE = handle.read()
FILE_LINES = FILE.splitlines()

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
EXAMPLE_EVENTS_PARTS = [{'source.ip': '109.126.64.2',
                         'source.asn': 12635,
                         'time.source': '2015-08-31T08:16:10+00:00',
                         'malware.name': 'asprox',
                         'destination.port': 25,
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '109.90.233.19',
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
                        {'source.ip': '109.91.0.227',
                         'source.asn': 6830,
                         'time.source': '2015-08-31T09:00:57+00:00',
                         'malware.name': 'conficker',
                         'destination.port': 80,
                         'destination.ip': '216.66.15.109',
                         'extra': '{"destination.local_port": 1430}',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '111.111.111.183',
                         'source.asn': 11178,
                         'time.source': '2016-08-13T17:58:59+00:00',
                         'malware.name': 'iotmirai',
                         'source.geolocation.cc': 'LV',
                         },
                        {'source.ip': '198.51.100.54',
                         'source.asn': 8559,
                         'time.source': '2018-03-03T13:41:36+00:00',
                         'classification.type': 'brute-force',
                         'classification.identifier': 'rdp',
                         'protocol.application': 'rdp',
                         'destination.port': 3389,
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '198.51.100.54',
                         'source.asn': 8559,
                         'time.source': '2018-03-03T13:41:36+00:00',
                         'classification.type': 'vulnerable service',
                         'classification.identifier': 'openrelay',
                         'protocol.application': 'smtp',
                         'destination.port': 25,
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '245.16.92.48',
                         'source.asn': 64496,
                         'time.source': '2018-03-20T13:29:12+00:00',
                         'destination.ip': '249.145.142.15',
                         'destination.port': 22,
                         'classification.type': 'brute-force',
                         'classification.identifier': 'ssh',
                         'source.geolocation.cc': 'AT',
                         'protocol.application': 'ssh',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '245.16.92.48',
                         'source.asn': 64496,
                         'time.source': '2018-03-20T13:29:12+00:00',
                         'destination.ip': '249.145.142.15',
                         'destination.port': 23,
                         'classification.type': 'brute-force',
                         'classification.identifier': 'telnet',
                         'source.geolocation.cc': 'AT',
                         'protocol.application': 'telnet',
                         'protocol.transport': 'tcp',
                         },
                        {'source.ip': '172.20.148.81',
                         'source.asn': 64496,
                         'time.source': '2018-03-17T13:00:32+00:00',
                         'destination.port': 80,
                         'classification.type': 'scanner',
                         'classification.identifier': 'wordpress-vulnerabilities',
                         'event_description.text': 'scanning for wordpress vulnerabilities',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         'protocol.application': 'http',
                         },
                        {'source.ip': '172.20.148.81',
                         'source.asn': 64496,
                         'time.source': '2018-03-17T13:00:32+00:00',
                         'destination.port': 80,
                         'classification.type': 'scanner',
                         'classification.identifier': 'wordpress-login',
                         'event_description.text': 'scanning for wordpress login pages',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         'protocol.application': 'http',
                         },
                        {'source.ip': '109.91.0.227',
                         'source.asn': 64496,
                         'time.source': '2015-08-31T09:00:57+00:00',
                         'malware.name': 's_other',
                         'destination.port': 80,
                         'destination.ip': '216.66.15.109',
                         'extra': '{"destination.local_port": 1430}',
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                         {'classification.type': 'spam',
                         'classification.identifier': 'spamlink',
                         'malware.name': 'darkmailer2',
                         'malware.version': '1660',
                         'source.url': 'http://example.com/',
                         'protocol.transport': 'tcp',
                         'source.asn': 64496,
                         'source.geolocation.cc': 'AT',
                         'source.ip': '192.168.46.8',
                         'event_description.text': 'Link appeared in a spam email from ip in extra.spam_ip.',
                         'time.source': '2018-04-08T13:05:08+00:00',
                         'extra': '{"spam_ip": "192.168.46.8"}',
                         },
                        {'source.ip': '198.51.100.54',
                         'source.asn': 64496,
                         'time.source': '2018-05-31T09:40:54+00:00',
                         'classification.type': 'brute-force',
                         'classification.identifier': 'smtp',
                         'protocol.application': 'smtp',
                         'destination.port': 25,
                         'source.geolocation.cc': 'AT',
                         'protocol.transport': 'tcp',
                         },
                        ]


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
            event_ = EVENT_TEMPL.copy()
            event_.update(event)
            event_['raw'] = utils.base64_encode('\n'.join((FILE_LINES[0],
                                                           FILE_LINES[1+position])))
            self.assertMessageEqual(position, event_)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
