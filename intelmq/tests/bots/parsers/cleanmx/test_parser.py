# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.utils as utils
import intelmq.lib.test as test
from intelmq.bots.parsers.cleanmx.parser import \
    CleanMXParserBot


with open(os.path.join(os.path.dirname(__file__), 'xmlphishing')) as handle:
    PHISHING_FILE = handle.read()
with open(os.path.join(os.path.dirname(__file__), 'xmlviruses')) as handle:
    VIRUSES_FILE = handle.read()

PHISHING_REPORT = {"feed.url": "http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&format=csv&domain=",
                   "feed.name": "CleanMX Phishing",
                   "__type": "Report",
                   "raw": utils.base64_encode(PHISHING_FILE),
                   "time.observation": "2015-11-02T13:11:43+00:00"
                   }
PHISHING_EVENTS = [{'__type': 'Event',
                    'classification.type': 'phishing',
                    'event_description.target': 'DHL',
                    'extra': '{"ddescr": "Example Layer", "id": "9377142", "inetnum": '
                             '"198.18.0.0 - 198.19.255.255", "netname": "EXAMPLE-NETWORK-15", '
                             '"ns1": "ns2.example.com", "ns2": "ns1.example.com", "phishtank": '
                             '"4647345", "response": "alive", "review": "198.18.0.1"}',
                    'feed.name': 'CleanMX Phishing',
                    'feed.url': 'http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&format=csv&domain=',
                    'raw': 'bGluZSxpZCxmaXJzdHRpbWUsbGFzdHRpbWUscGhpc2h0YW5rLHZpcnVzbmFtZSx1cmwscmVjZW50LHJlc3BvbnNlLGlwLHJldmlldyxkb21haW4sY291bnRyeSxzb3VyY2UsZW1haWwsaW5ldG51bSxuZXRuYW1lLGRkZXNjcixuczEsbnMyLG5zMyxuczQsbnM1DQoxLDkzNzcxNDIsMjAxNi0xMS0yOSAxMDozMTo0NSwxOTcwLTAxLTAxIDAxOjAwOjAwLDQ2NDczNDUsREhMLGh0dHA6Ly9leGFtcGxlLmNvbS9kZWhsJTIwcGFja2FnZS9jb25maXJtLyxkb3duLGFsaXZlLDE5OC4xOC4wLjEsMTk4LjE4LjAuMSwxOTguMTguMC4xLFVTLEFSSU4sYWJ1c2VAZXhhbXBsZS5jb20sMTk4LjE4LjAuMCAtIDE5OC4xOS4yNTUuMjU1LEVYQU1QTEUtTkVUV09SSy0xNSxFeGFtcGxlIExheWVyLG5zMi5leGFtcGxlLmNvbSxuczEuZXhhbXBsZS5jb20sLCwNCg==',
                    'source.abuse_contact': 'abuse@example.com',
                    'source.geolocation.cc': 'US',
                    'source.ip': '198.18.0.1',
                    'source.registry': 'ARIN',
                    'source.url': 'http://example.com/dehl%20package/confirm/',
                    'status': 'offline',
                    'time.source': '2016-11-29T10:31:45+00:00'},
                   {'__type': 'Event',
                    'classification.type': 'phishing',
                    'event_description.target': 'Free',
                    'extra': '{"id": "9377136", "inetnum": "198.18.0.0 - 198.19.255.255", '
                             '"netname": "EXAMPLE", "ns1": "ns-de.example.com", "ns2": '
                             '"ns-de.example.net", "ns3": "ns-de.example.com", "ns4": '
                             '"ns-de.example.org", "phishtank": "4647412", "response": "alive", '
                             '"review": "198.18.0.7"}',
                    'feed.name': 'CleanMX Phishing',
                    'feed.url': 'http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&format=csv&domain=',
                    'raw': 'bGluZSxpZCxmaXJzdHRpbWUsbGFzdHRpbWUscGhpc2h0YW5rLHZpcnVzbmFtZSx1cmwscmVjZW50LHJlc3BvbnNlLGlwLHJldmlldyxkb21haW4sY291bnRyeSxzb3VyY2UsZW1haWwsaW5ldG51bSxuZXRuYW1lLGRkZXNjcixuczEsbnMyLG5zMyxuczQsbnM1DQo3LDkzNzcxMzYsMjAxNi0xMS0yOSAxMDoxNzozOCwxOTcwLTAxLTAxIDAxOjAwOjAwLDQ2NDc0MTIsRnJlZSxodHRwOi8vZXhhbXBsZS5uZXQvRnIvNWI4Y2EzY2FmODlmNWNkNjI0YzJiNjkyYjk5NzFjY2MvLHVwLGFsaXZlLDE5OC4xOC4wLjcsMTk4LjE4LjAuNyxleGFtcGxlLm5ldCxQTCxSSVBFLGFidXNlQGV4YW1wbGUubmV0LDE5OC4xOC4wLjAgLSAxOTguMTkuMjU1LjI1NSxFWEFNUExFLCxucy1kZS5leGFtcGxlLmNvbSxucy1kZS5leGFtcGxlLm5ldCxucy1kZS5leGFtcGxlLmNvbSxucy1kZS5leGFtcGxlLm9yZywNCg==',
                    'source.abuse_contact': 'abuse@example.net',
                    'source.fqdn': 'example.net',
                    'source.geolocation.cc': 'PL',
                    'source.ip': '198.18.0.7',
                    'source.registry': 'RIPE',
                    'source.url': 'http://example.net/Fr/5b8ca3caf89f5cd624c2b692b9971ccc/',
                    'status': 'online',
                    'time.source': '2016-11-29T10:17:38+00:00'}
                   ]
VIRUS_REPORT = {"feed.url": "http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&format=csv&domain=",
                "feed.name": "CleanMX Viruses",
                "__type": "Report",
                "raw": utils.base64_encode(VIRUSES_FILE),
                "time.observation": "2015-11-02T13:11:43+00:00"
                }
VIRUSES_EVENTS = [{'__type': 'Event',
                   'classification.type': 'malware',
                   'extra': '{"ddescr": "<![CDATA[Example]]>", "id": "104542833", "inetnum": '
                            '"198.18.0.0 - 198.19.255.255", "netname": "EXAMPLE-COM", "ns1": '
                            '"ns10.domaincontrol.com", "ns2": "ns09.domaincontrol.com", '
                            '"response": "alive", "review": "198.18.0.8", "source": "ARIN", "sub": "sub16"}',
                   'feed.name': 'CleanMX Viruses',
                   'feed.url': 'http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&format=csv&domain=',
                   'malware.name': 'solimba.032',
                   'raw': 'bGluZSxpZCxzdWIsZmlyc3R0aW1lLGxhc3R0aW1lLHNjYW5uZXIsdmlydXNuYW1lLHVybCxyZWNlbnQscmVzcG9uc2UsaXAsYXMscmV2aWV3LGRvbWFpbixjb3VudHJ5LHNvdXJjZSxlbWFpbCxpbmV0bnVtLG5ldG5hbWUsZGRlc2NyLG5zMSxuczIsbnMzLG5zNCxuczUNCjgsMTA0NTQyODMzLHN1YjE2LDIwMTYtMTEtMjkgMTE6MTg6MjQsMTk3MC0wMS0wMSAwMTowMDowMCx1bmRlZixTb2xpbWJhLjAzMixodHRwOi8vZGwuZXhhbXBsZS5jb20vbi8zLjEuMTIuOS82NDgzNzkzL0J1cytEcml2ZXIuZXhlLHVwLGFsaXZlLDE5OS41OS4yNDMuMTIwLEFTTkEsMTk4LjE4LjAuOCxleGFtcGxlLmNvbSxVUyxBUklOLGFidXNlQGV4YW1wbGUuY29tLDE5OC4xOC4wLjAgLSAxOTguMTkuMjU1LjI1NSxFWEFNUExFLUNPTSw8IVtDREFUQVtFeGFtcGxlXV0+LG5zMTAuZG9tYWluY29udHJvbC5jb20sbnMwOS5kb21haW5jb250cm9sLmNvbSwsLA0K',
                   'source.abuse_contact': 'abuse@example.com',
                   'source.fqdn': 'example.com',
                   'source.geolocation.cc': 'US',
                   'source.ip': '199.59.243.120',
                   'source.url': 'http://dl.example.com/n/3.1.12.9/6483793/Bus+Driver.exe',
                   'status': 'online',
                   'time.source': '2016-11-29T11:18:24+00:00'},
                  {'__type': 'Event',
                   'classification.type': 'malware',
                   'extra': '{"ddescr": "<![CDATA[Example]]>", "id": "104542831", "inetnum": '
                            '"198.18.0.0 - 198.19.255.255", "netname": "EXAMPLENET", "ns1": '
                            '"f1g1ns2.example.net", "ns2": "f1g1ns1.example.net", "response": '
                            '"alive", "review": "120.26.127.170", "source": "APNIC", "sub": "sub16"}',
                   'feed.name': 'CleanMX Viruses',
                   'feed.url': 'http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&format=csv&domain=',
                   'malware.name': 'trj/ci.a',
                   'raw': 'bGluZSxpZCxzdWIsZmlyc3R0aW1lLGxhc3R0aW1lLHNjYW5uZXIsdmlydXNuYW1lLHVybCxyZWNlbnQscmVzcG9uc2UsaXAsYXMscmV2aWV3LGRvbWFpbixjb3VudHJ5LHNvdXJjZSxlbWFpbCxpbmV0bnVtLG5ldG5hbWUsZGRlc2NyLG5zMSxuczIsbnMzLG5zNCxuczUNCjksMTA0NTQyODMxLHN1YjE2LDIwMTYtMTEtMjkgMTE6MTg6MjQsMTk3MC0wMS0wMSAwMTowMDowMCx1bmRlZixUcmovQ0kuQSxodHRwOi8vZGwuZXhhbXBsZS5jb20vZG93bmxvYWQvJUU4JUJGJTg1JUU5JTlCJUI3OSVFNSVBRSU5OCVFNiU5NiVCOSVFNCVCOCU4QiVFOCVCRCVCRF8zMkAxMDUzNzEuZXhlLHVwLGFsaXZlLDE5OC4xOC4wLjksYXMzNzk2MywxMjAuMjYuMTI3LjE3MCxleGFtcGxlLmNvbSxDTixBUE5JQyxzb25nQGV4YW1wbGUuY29tLDE5OC4xOC4wLjAgLSAxOTguMTkuMjU1LjI1NSxFWEFNUExFTkVULDwhW0NEQVRBW0V4YW1wbGVdXT4sZjFnMW5zMi5leGFtcGxlLm5ldCxmMWcxbnMxLmV4YW1wbGUubmV0LCwsDQo=',
                   'source.abuse_contact': 'song@example.com',
                   'source.asn': 37963,
                   'source.fqdn': 'example.com',
                   'source.geolocation.cc': 'CN',
                   'source.ip': '198.18.0.9',
                   'source.url': 'http://dl.example.com/download/%E8%BF%85%E9%9B%B79%E5%AE%98%E6%96%B9%E4%B8%8B%E8%BD%BD_32@105371.exe',
                   'status': 'online',
                   'time.source': '2016-11-29T11:18:24+00:00'},
                  ]


class TestCleanMXParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CleanMXParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CleanMXParserBot
        cls.default_input_message = PHISHING_REPORT

    def test_phishing(self):
        self.run_bot()
        self.assertMessageEqual(0, PHISHING_EVENTS[0])
        self.assertMessageEqual(1, PHISHING_EVENTS[1])

    def test_viruses(self):
        self.input_message = VIRUS_REPORT
        self.run_bot()
        self.assertMessageEqual(0, VIRUSES_EVENTS[0])
        self.assertMessageEqual(1, VIRUSES_EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
