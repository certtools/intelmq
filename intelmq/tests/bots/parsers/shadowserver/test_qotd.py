# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.qotd_parser import \
    ShadowServerQotdParserBot

with open(os.path.join(os.path.dirname(__file__), 'qotd.csv')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "ShadowServer QOTD",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'classification.identifier': 'qotd',
           'classification.type': 'vulnerable service',
           'extra': '{"sic": 654321, "quote": "N?s matamos o tempo, mas ele enterra-nos.?? (Machado de Assis)??\\"", "naics": 123456}',
           'feed.name': 'ShadowServer QOTD',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnVUJFUkxBTkRJQScpLCh1J3Byb3RvY29sJywgdSd1ZHAnKSwodSduYWljcycsIHUnMTIzNDU2JyksKHUndGltZXN0YW1wJywgdScyMDE0LTAzLTE2IDA4OjEyOjMzJyksKHUncmVnaW9uJywgdSdNSU5BUyBHRVJBSVMnKSwodSdob3N0bmFtZScsIHUnMTc5LTEyNi0wMDItMDM4LnhkLWR5bmFtaWMuY3RiY25ldHN1cGVyLmNvbS5icicpLCh1J2FzbicsIHUnNTMwMDYnKSwodSdzaWMnLCB1JzY1NDMyMScpLCh1J3F1b3RlJywgdSdOP3MgbWF0YW1vcyBvIHRlbXBvLCBtYXMgZWxlIGVudGVycmEtbm9zLj8/IChNYWNoYWRvIGRlIEFzc2lzKT8/IicpLCh1J3RhZycsIHUncW90ZCcpLCh1J2lwJywgdScxNzkuMTI2LjIuMzgnKSwodSdnZW8nLCB1J0JSJyksKHUncG9ydCcsIHUnMTcnKSI=',
           'source.asn': 53006,
           'source.geolocation.cc': 'BR',
           'source.geolocation.city': 'UBERLANDIA',
           'source.geolocation.region': 'MINAS GERAIS',
           'source.ip': '179.126.2.38',
           'source.port': 17,
           'source.reverse_dns': '179-126-002-038.xd-dynamic.ctbcnetsuper.com.br',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:33+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'qotd',
           'classification.type': 'vulnerable service',
           'extra': '{"quote": "When a stupid man is doing something he is ashamed of, he always declares?? that it is his duty. George Bernard Shaw (1856-1950)??\\""}',
           'feed.name': 'ShadowServer QOTD',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnU0VPVUwnKSwodSdwcm90b2NvbCcsIHUndWRwJyksKHUnbmFpY3MnLCB1JzAnKSwodSd0aW1lc3RhbXAnLCB1JzIwMTQtMDMtMTYgMDg6MTI6MzMnKSwodSdyZWdpb24nLCB1IlNFT1VMLVQnVUtQWU9MU0kiKSwodSdob3N0bmFtZScsIHUnJyksKHUnYXNuJywgdSczNzg2JyksKHUnc2ljJywgdScwJyksKHUncXVvdGUnLCB1J1doZW4gYSBzdHVwaWQgbWFuIGlzIGRvaW5nIHNvbWV0aGluZyBoZSBpcyBhc2hhbWVkIG9mLCBoZSBhbHdheXMgZGVjbGFyZXM/PyB0aGF0IGl0IGlzIGhpcyBkdXR5LiBHZW9yZ2UgQmVybmFyZCBTaGF3ICgxODU2LTE5NTApPz8iJyksKHUndGFnJywgdSdxb3RkJyksKHUnaXAnLCB1JzEyMy4xNDAuMTQ5LjEzMScpLCh1J2dlbycsIHUnS1InKSwodSdwb3J0JywgdScxNycpIg==',
           'source.asn': 3786,
           'source.geolocation.cc': 'KR',
           'source.geolocation.city': 'SEOUL',
           'source.geolocation.region': u"SEOUL-T'UKPYOLSI",
           'source.ip': '123.140.149.131',
           'source.port': 17,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:33+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'qotd',
           'classification.type': 'vulnerable service',
           'extra': '{"quote": "_The secret of being miserable is to have leisure to bother about whether?? you are happy or not.  The cure for it is occupation._?? George Bernard Shaw (1856-1950)??"}',
           'feed.name': 'ShadowServer QOTD',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnV0FZTkUnKSwodSdwcm90b2NvbCcsIHUndWRwJyksKHUnbmFpY3MnLCB1JzAnKSwodSd0aW1lc3RhbXAnLCB1JzIwMTQtMDMtMTYgMDg6MTI6MzQnKSwodSdyZWdpb24nLCB1J1BFTk5TWUxWQU5JQScpLCh1J2hvc3RuYW1lJywgdSd1MTUxNjk3MzIub25saW5laG9tZS1zZXJ2ZXIuY29tJyksKHUnYXNuJywgdSc4NTYwJyksKHUnc2ljJywgdScwJyksKHUncXVvdGUnLCB1J19UaGUgc2VjcmV0IG9mIGJlaW5nIG1pc2VyYWJsZSBpcyB0byBoYXZlIGxlaXN1cmUgdG8gYm90aGVyIGFib3V0IHdoZXRoZXI/PyB5b3UgYXJlIGhhcHB5IG9yIG5vdC4gIFRoZSBjdXJlIGZvciBpdCBpcyBvY2N1cGF0aW9uLl8/PyBHZW9yZ2UgQmVybmFyZCBTaGF3ICgxODU2LTE5NTApPz8nKSwodSd0YWcnLCB1J3FvdGQnKSwodSdpcCcsIHUnNzQuMjA4LjIwOS40NScpLCh1J2dlbycsIHUnVVMnKSwodSdwb3J0JywgdScxNycpIg==',
           'source.asn': 8560,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'WAYNE',
           'source.geolocation.region': 'PENNSYLVANIA',
           'source.ip': '74.208.209.45',
           'source.port': 17,
           'source.reverse_dns': 'u15169732.onlinehome-server.com',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:34+00:00'},
          {'__type': 'Event',
           'classification.identifier': 'qotd',
           'classification.type': 'vulnerable service',
           'extra': '{"quote": "_We have no more right to consume happiness without producing it than to?? consume wealth without producing it._ George Bernard Shaw (1856-1950)??"}',
           'feed.name': 'ShadowServer QOTD',
           'protocol.application': 'qotd',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnUEhPRU5JWCcpLCh1J3Byb3RvY29sJywgdSd1ZHAnKSwodSduYWljcycsIHUnMCcpLCh1J3RpbWVzdGFtcCcsIHUnMjAxNC0wMy0xNiAwODoxMjozNCcpLCh1J3JlZ2lvbicsIHUnQVJJWk9OQScpLCh1J2hvc3RuYW1lJywgdScyMy4xOS40MS4yMTgucmRucy51YmlxdWl0eS5pbycpLCh1J2FzbicsIHUnMTUwMDMnKSwodSdzaWMnLCB1JzAnKSwodSdxdW90ZScsIHUnX1dlIGhhdmUgbm8gbW9yZSByaWdodCB0byBjb25zdW1lIGhhcHBpbmVzcyB3aXRob3V0IHByb2R1Y2luZyBpdCB0aGFuIHRvPz8gY29uc3VtZSB3ZWFsdGggd2l0aG91dCBwcm9kdWNpbmcgaXQuXyBHZW9yZ2UgQmVybmFyZCBTaGF3ICgxODU2LTE5NTApPz8nKSwodSd0YWcnLCB1J3FvdGQnKSwodSdpcCcsIHUnMjMuMTkuNDEuMjE4JyksKHUnZ2VvJywgdSdVUycpLCh1J3BvcnQnLCB1JzE3Jyki',
           'source.asn': 15003,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'PHOENIX',
           'source.geolocation.region': 'ARIZONA',
           'source.ip': '23.19.41.218',
           'source.port': 17,
           'source.reverse_dns': '23.19.41.218.rdns.ubiquity.io',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T08:12:34+00:00'}]


class TestShadowServerQotdParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowServerQotdParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowServerQotdParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':
    unittest.main()
