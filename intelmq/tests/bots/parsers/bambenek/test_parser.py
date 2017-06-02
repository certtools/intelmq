# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.bambenek.parser import BambenekParserBot

with open(os.path.join(os.path.dirname(__file__), 'c2-dommasterlist.txt')) as handle:
    DOMAIN_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'c2-ipmasterlist.txt')) as handle:
    IP_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'dga-feed.txt')) as handle:
    DGA_FILE = handle.read()

DOMAIN_REPORT = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt',
                 'feed.name': 'Bambenek C2 Domain Feed',
                 '__type': 'Report',
                 'raw': utils.base64_encode(DOMAIN_FILE),
                 'time.observation': '2016-01-01T00:00:00+00:00'
                }

DOMAIN_EVENTS = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt',
                 'feed.name': 'Bambenek C2 Domain Feed',
                 '__type': 'Event',
                 'time.observation': '2016-01-01T00:00:00+00:00',
                 'raw': 'c2ZraDIxb2tycm5sdS5jb20sRG9tYWluIHVzZWQgYnkgc2hpb3RvYi91cmx6b25lL2JlYmxvaCwyMDE2LTExLTEyIDE1OjAyLGh0dHA6Ly9vc2ludC5iYW1iZW5la2NvbnN1bHRpbmcuY29tL21hbnVhbC9iZWJsb2gudHh0',
                 'time.source': '2016-11-12T15:02:00+00:00',
                 'source.fqdn': 'sfkh21okrrnlu.com',
                 'malware.name': 'bebloh',
                 'classification.type': 'c&c',
                 'status': 'online',
                 'event_description.text': 'Domain used by shiotob/urlzone/bebloh',
                 'event_description.url': 'http://osint.bambenekconsulting.com/manual/bebloh.txt'
                }

IP_REPORT = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt',
             'feed.name': 'Bambenek C2 IP Feed',
             '__type': 'Report',
             'raw': utils.base64_encode(IP_FILE),
             'time.observation': '2016-01-01T00:00:00+00:00'
            }

IP_EVENTS = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt',
             'feed.name': 'Bambenek C2 IP Feed',
             '__type': 'Event',
             'time.observation': '2016-01-01T00:00:00+00:00',
             'raw': 'MjEzLjI0Ny40Ny4xOTAsSVAgdXNlZCBieSBzaGlvdG9iL3VybHpvbmUvYmVibG9oIEMmQywyMDE2LTExLTEyIDE4OjAyLGh0dHA6Ly9vc2ludC5iYW1iZW5la2NvbnN1bHRpbmcuY29tL21hbnVhbC9iZWJsb2gudHh0',
             'source.ip': '213.247.47.190',
             'malware.name': 'bebloh',
             'classification.type': 'c&c',
             'status': 'online',
             'time.source': '2016-11-12T18:02:00+00:00',
             'event_description.text': 'IP used by shiotob/urlzone/bebloh C&C',
             'event_description.url': 'http://osint.bambenekconsulting.com/manual/bebloh.txt'
            }

DGA_REPORT = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/dga-feed.txt',
              'feed.name': 'Bambenek DGA Domain Feed',
              '__type': 'Report',
              'raw': utils.base64_encode(DGA_FILE),
              'time.observation': '2016-01-01T00:00:00+00:00'
             }

DGA_EVENTS = {'feed.url': 'http://osint.bambenekconsulting.com/feeds/dga-feed.txt',
              'feed.name': 'Bambenek DGA Domain Feed',
              '__type': 'Event',
              'time.observation': '2016-01-01T00:00:00+00:00',
              'raw': 'eHFtY2xudXNhc3d2b2YuY29tLERvbWFpbiB1c2VkIGJ5IENyeXB0b2xvY2tlciAtIEZsYXNoYmFjayBER0EgZm9yIDEwIE5vdiAyMDE2LDIwMTYtMTEtMTAsaHR0cDovL29zaW50LmJhbWJlbmVrY29uc3VsdGluZy5jb20vbWFudWFsL2NsLnR4dA==',
              'time.source': '2016-11-10T00:00:00+00:00',
              'source.fqdn': 'xqmclnusaswvof.com',
              'classification.type': 'dga domain',
              'malware.name': 'cryptolocker',
              'event_description.text': 'Domain used by Cryptolocker - Flashback DGA for 10 Nov 2016',
              'event_description.url': 'http://osint.bambenekconsulting.com/manual/cl.txt'
             }


class TestBambenekParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase for BambenekParserBot. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = BambenekParserBot
        cls.default_input_message = DOMAIN_REPORT

    def test_domain(self):
        self.run_bot()
        self.assertMessageEqual(0, DOMAIN_EVENTS)

    def test_ip(self):
        self.input_message = IP_REPORT
        self.run_bot()
        self.assertMessageEqual(0, IP_EVENTS)

    def test_dga(self):
        self.input_message = DGA_REPORT
        self.run_bot()
        self.assertMessageEqual(0, DGA_EVENTS)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
