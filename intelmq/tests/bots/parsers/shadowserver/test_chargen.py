# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.shadowserver.chargen_parser import \
    ShadowServerChargenParserBot

with open(os.path.join(os.path.dirname(__file__), 'chargen.csv')) as handle:
    EXAMPLE_FILE = handle.read()

EXAMPLE_REPORT = {"feed.name": "ShadowServer Chargen",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENTS = [{'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'extra': '{"sic": 654321, "response_size": 116, "naics": 123456}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnUkVZS0pBVklLJyksKHUncHJvdG9jb2wnLCB1J3VkcCcpLCh1J25haWNzJywgdScxMjM0NTYnKSwodSd0aW1lc3RhbXAnLCB1JzIwMTQtMDMtMTYgMDQ6MTU6MTknKSwodSdyZWdpb24nLCB1J0hPRlVPQk9SR0FSU1ZBT0lPJyksKHUnaG9zdG5hbWUnLCB1JycpLCh1J2FzbicsIHUnMTI5NjknKSwodSdzaWMnLCB1JzY1NDMyMScpLCh1J3RhZycsIHUnY2hhcmdlbicpLCh1J2lwJywgdSc4OC4xNDkuMjMuMjMwJyksKHUnZ2VvJywgdSdJUycpLCh1J3BvcnQnLCB1JzE5JyksKHUnc2l6ZScsIHUnMTE2Jyki',
           'source.asn': 12969,
           'source.geolocation.cc': 'IS',
           'source.geolocation.city': 'REYKJAVIK',
           'source.geolocation.region': 'HOFUOBORGARSVAOIO',
           'source.ip': '88.149.23.230',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'extra': '{"response_size": 116}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnVEhBTkggUEhPIEhPIENISSBNSU5IJyksKHUncHJvdG9jb2wnLCB1J3VkcCcpLCh1J25haWNzJywgdScwJyksKHUndGltZXN0YW1wJywgdScyMDE0LTAzLTE2IDA0OjE1OjE5JyksKHUncmVnaW9uJywgdSdITyBDSEkgTUlOSCcpLCh1J2hvc3RuYW1lJywgdScnKSwodSdhc24nLCB1JzQ1NTQzJyksKHUnc2ljJywgdScwJyksKHUndGFnJywgdSdjaGFyZ2VuJyksKHUnaXAnLCB1JzExMi4xOTcuMjQwLjEnKSwodSdnZW8nLCB1J1ZOJyksKHUncG9ydCcsIHUnMTknKSwodSdzaXplJywgdScxMTYnKSI=',
           'source.asn': 45543,
           'source.geolocation.cc': 'VN',
           'source.geolocation.city': 'THANH PHO HO CHI MINH',
           'source.geolocation.region': 'HO CHI MINH',
           'source.ip': '112.197.240.1',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'extra': '{"response_size": 116}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnUk9NQScpLCh1J3Byb3RvY29sJywgdSd1ZHAnKSwodSduYWljcycsIHUnMCcpLCh1J3RpbWVzdGFtcCcsIHUnMjAxNC0wMy0xNiAwNDoxNToxOScpLCh1J3JlZ2lvbicsIHUnTEFaSU8nKSwodSdob3N0bmFtZScsIHUnaG9zdDI2LTE0Ni1zdGF0aWMuMzYtODUtYi5idXNpbmVzcy50ZWxlY29taXRhbGlhLml0JyksKHUnYXNuJywgdSczMjY5JyksKHUnc2ljJywgdScwJyksKHUndGFnJywgdSdjaGFyZ2VuJyksKHUnaXAnLCB1Jzg1LjM2LjE0Ni4yNicpLCh1J2dlbycsIHUnSVQnKSwodSdwb3J0JywgdScxOScpLCh1J3NpemUnLCB1JzExNicpIg==',
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
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'extra': '{"response_size": 116}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnVklDVE9SSUEnKSwodSdwcm90b2NvbCcsIHUndWRwJyksKHUnbmFpY3MnLCB1JzAnKSwodSd0aW1lc3RhbXAnLCB1JzIwMTQtMDMtMTYgMDQ6MTU6MTknKSwodSdyZWdpb24nLCB1J0JSSVRJU0ggQ09MVU1CSUEnKSwodSdob3N0bmFtZScsIHUnJyksKHUnYXNuJywgdSc2MzI3JyksKHUnc2ljJywgdScwJyksKHUndGFnJywgdSdjaGFyZ2VuJyksKHUnaXAnLCB1JzE4NC42OS4xNjguMjM3JyksKHUnZ2VvJywgdSdDQScpLCh1J3BvcnQnLCB1JzE5JyksKHUnc2l6ZScsIHUnMTE2Jyki',
           'source.asn': 6327,
           'source.geolocation.cc': 'CA',
           'source.geolocation.city': 'VICTORIA',
           'source.geolocation.region': 'BRITISH COLUMBIA',
           'source.ip': '184.69.168.237',
           'source.port': 19,
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'},
          {'__type': 'Event',
           'classification.type': 'vulnerable service',
           'classification.identifier': 'chargen',
           'extra': '{"response_size": 116}',
           'feed.name': 'ShadowServer Chargen',
           'protocol.application': 'chargen',
           'protocol.transport': 'udp',
           'raw': 'Iih1J3NlY3RvcicsIHUnJyksKHUnY2l0eScsIHUnSE9OT0xVTFUnKSwodSdwcm90b2NvbCcsIHUndWRwJyksKHUnbmFpY3MnLCB1JzAnKSwodSd0aW1lc3RhbXAnLCB1JzIwMTQtMDMtMTYgMDQ6MTU6MTknKSwodSdyZWdpb24nLCB1J0hBV0FJSScpLCh1J2hvc3RuYW1lJywgdSdkaGNwLTEyOC0xNzEtMzItMTIuYmlsZ2VyLmhhd2FpaS5lZHUnKSwodSdhc24nLCB1JzYzNjAnKSwodSdzaWMnLCB1JzAnKSwodSd0YWcnLCB1J2NoYXJnZW4nKSwodSdpcCcsIHUnMTI4LjE3MS4zMi4xMicpLCh1J2dlbycsIHUnVVMnKSwodSdwb3J0JywgdScxOScpLCh1J3NpemUnLCB1JzExNicpIg==',
           'source.asn': 6360,
           'source.geolocation.cc': 'US',
           'source.geolocation.city': 'HONOLULU',
           'source.geolocation.region': 'HAWAII',
           'source.ip': '128.171.32.12',
           'source.port': 19,
           'source.reverse_dns': 'dhcp-128-171-32-12.bilger.hawaii.edu',
           'time.observation': '2015-01-01T00:00:00+00:00',
           'time.source': '2014-03-16T04:15:19+00:00'}]


class TestShadowServerChargenParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a ShadowServerChargenParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowServerChargenParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        for i, EVENT in enumerate(EVENTS):
            self.assertMessageEqual(i, EVENT)


if __name__ == '__main__':
    unittest.main()
