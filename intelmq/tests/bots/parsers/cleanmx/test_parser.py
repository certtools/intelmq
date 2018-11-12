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

PHISHING_REPORT = {"feed.url": "http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=",
                   "feed.name": "CleanMX Phishing",
                   "__type": "Report",
                   "raw": utils.base64_encode(PHISHING_FILE),
                   "time.observation": "2015-11-02T13:11:43+00:00"
                   }
PHISHING_EVENTS = [{
                        'source.abuse_contact': 'abuse@cloudflare.com',
                        'extra.descr': 'Cloudflare, Inc. CLOUD14 101 Townsend Street San Francisco CA 94107',
                        'extra.id': '11095095',
                        'classification.type': 'phishing',
                        'feed.name': 'CleanMX Phishing',
                        'extra.ns1': 'gail.ns.cloudflare.com',
                        'source.url': 'http://www.autoposting.com.br/i/',
                        'extra.phishtank': '5140280',
                        'source.fqdn': 'autoposting.com.br',
                        '__type': 'Event',
                        'extra.review': '104.28.14.106',
                        'extra.netname': 'CLOUDFLARENET',
                        'source.ip': '104.28.15.106',
                        'raw': 'PGVudHJ5PgoJPGxpbmU+MTwvbGluZT4KCTxpZD4xMTA5NTA5NTwvaWQ+Cgk8Zmlyc3Q+MTUwMjAzMTU5MDwvZmlyc3Q+Cgk8bGFzdD4wPC9sYXN0PgoJPHBoaXNodGFuaz41MTQwMjgwPC9waGlzaHRhbms+Cgk8dGFyZ2V0IC8+Cgk8dXJsPmh0dHA6Ly93d3cuYXV0b3Bvc3RpbmcuY29tLmJyL2kvPC91cmw+Cgk8cmVjZW50PnVwPC9yZWNlbnQ+Cgk8cmVzcG9uc2U+YWxpdmU8L3Jlc3BvbnNlPgoJPGlwPjEwNC4yOC4xNS4xMDY8L2lwPgoJPHJldmlldz4xMDQuMjguMTQuMTA2PC9yZXZpZXc+Cgk8ZG9tYWluPmF1dG9wb3N0aW5nLmNvbS5icjwvZG9tYWluPgoJPGNvdW50cnk+VVM8L2NvdW50cnk+Cgk8c291cmNlPkFSSU48L3NvdXJjZT4KCTxlbWFpbD5hYnVzZUBjbG91ZGZsYXJlLmNvbTwvZW1haWw+Cgk8aW5ldG51bT4xMDQuMTYuMC4wIC0gMTA0LjMxLjI1NS4yNTU8L2luZXRudW0+Cgk8bmV0bmFtZT5DTE9VREZMQVJFTkVUPC9uZXRuYW1lPgoJPGRlc2NyPkNsb3VkZmxhcmUsIEluYy4gQ0xPVUQxNCAxMDEgVG93bnNlbmQgU3RyZWV0IFNhbiBGcmFuY2lzY28gQ0EgOTQxMDc8L2Rlc2NyPgoJPG5zMT5nYWlsLm5zLmNsb3VkZmxhcmUuY29tPC9uczE+Cgk8bnMyPm1heC5ucy5jbG91ZGZsYXJlLmNvbTwvbnMyPgoJPG5zMyAvPgoJPG5zNCAvPgoJPG5zNSAvPgo8L2VudHJ5Pgo=',
                        'extra.response': 'alive',
                        'status': 'online',
                        'time.observation': '2015-11-02T13:11:43+00:00',
                        'extra.ns2': 'max.ns.cloudflare.com',
                        'feed.url': 'http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=',
                        'source.registry': 'ARIN',
                        'extra.inetnum': '104.16.0.0 - 104.31.255.255',
                        'source.geolocation.cc': 'US',
                        'time.source': '2017-08-06T14:59:50+00:00',
                    },
                    {
                        'source.abuse_contact': 'abuse@mochahost.com',
                        'extra.descr': 'Mochahost.com ML-17 2880 Zanker Rd #203 San Jose CA 95134',
                        'extra.id': '11095094',
                        'classification.type': 'phishing',
                        'feed.name': 'CleanMX Phishing',
                        'extra.ns1': 'ns2.cally-hosting.club',
                        'source.url': 'http://mvptrades.xyz/ad0be/view/?email=abuse@exxonmobil.com',
                        'extra.phishtank': '5176961',
                        'source.fqdn': 'mvptrades.xyz',
                        'event_description.target': 'Adobe',
                        'extra.review': '198.38.90.108',
                        'extra.netname': 'MOCAH-1',
                        'source.ip': '198.38.90.108',
                        'raw': 'PGVudHJ5PgoJPGxpbmU+MjwvbGluZT4KCTxpZD4xMTA5NTA5NDwvaWQ+Cgk8Zmlyc3Q+MTUwMzUwNzg4MzwvZmlyc3Q+Cgk8bGFzdD4wPC9sYXN0PgoJPHBoaXNodGFuaz41MTc2OTYxPC9waGlzaHRhbms+Cgk8dGFyZ2V0PkFkb2JlPC90YXJnZXQ+Cgk8dXJsPmh0dHA6Ly9tdnB0cmFkZXMueHl6L2FkMGJlL3ZpZXcvP2VtYWlsPWFidXNlQGV4eG9ubW9iaWwuY29tPC91cmw+Cgk8cmVjZW50PnVwPC9yZWNlbnQ+Cgk8cmVzcG9uc2U+YWxpdmU8L3Jlc3BvbnNlPgoJPGlwPjE5OC4zOC45MC4xMDg8L2lwPgoJPHJldmlldz4xOTguMzguOTAuMTA4PC9yZXZpZXc+Cgk8ZG9tYWluPm12cHRyYWRlcy54eXo8L2RvbWFpbj4KCTxjb3VudHJ5PlVTPC9jb3VudHJ5PgoJPHNvdXJjZT5BUklOPC9zb3VyY2U+Cgk8ZW1haWw+YWJ1c2VAbW9jaGFob3N0LmNvbTwvZW1haWw+Cgk8aW5ldG51bT4xOTguMzguODAuMCAtIDE5OC4zOC45NS4yNTU8L2luZXRudW0+Cgk8bmV0bmFtZT5NT0NBSC0xPC9uZXRuYW1lPgoJPGRlc2NyPk1vY2hhaG9zdC5jb20gTUwtMTcgMjg4MCBaYW5rZXIgUmQgIzIwMyBTYW4gSm9zZSBDQSA5NTEzNDwvZGVzY3I+Cgk8bnMxPm5zMi5jYWxseS1ob3N0aW5nLmNsdWI8L25zMT4KCTxuczI+bnMxLmNhbGx5LWhvc3RpbmcuY2x1YjwvbnMyPgoJPG5zMyAvPgoJPG5zNCAvPgoJPG5zNSAvPgo8L2VudHJ5Pgo=',
                        'extra.response': 'alive',
                        'status': 'online',
                        '__type': 'Event',
                        'time.observation': '2015-11-02T13:11:43+00:00',
                        'extra.ns2': 'ns1.cally-hosting.club',
                        'feed.url': 'http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=',
                        'source.registry': 'ARIN',
                        'extra.inetnum': '198.38.80.0 - 198.38.95.255',
                        'source.geolocation.cc': 'US',
                        'time.source': '2017-08-23T17:04:43+00:00',
                    },
                    {
                        'classification.type': 'phishing',
                        'event_description.target': 'Google',
                        'extra.id': "10952859",
                        "extra.phishtank": "5287671",
                        "extra.response": "alive",
                        "extra.review": "accounts.google.",
                        'feed.name': 'CleanMX Phishing',
                        'feed.url': 'http://support.clean-mx.de/clean-mx/xmlphishing?response=alive&domain=',
                        'raw': 'PGVudHJ5PgoJPGxpbmU+MjQ4NDM8L2xpbmU+Cgk8aWQ+MTA5NTI4NTk8L2lkPgoJPGZpcnN0PjE1MDgzNDg4ODk8L2ZpcnN0PgoJPGxhc3Q+MDwvbGFzdD4KCTxwaGlzaHRhbms+NTI4NzY3MTwvcGhpc2h0YW5rPgoJPHRhcmdldD5Hb29nbGU8L3RhcmdldD4KCTx1cmw+aHR0cDovL2FjY291bnRzLmdvb2dsZS5jb20uLzwvdXJsPgoJPHJlY2VudD50b2dnbGU8L3JlY2VudD4KCTxyZXNwb25zZT5hbGl2ZTwvcmVzcG9uc2U+Cgk8aXA+YWNjb3VudHMuZ29vZ2xlLjwvaXA+Cgk8cmV2aWV3PmFjY291bnRzLmdvb2dsZS48L3Jldmlldz4KCTxkb21haW4+YWNjb3VudHMuZ29vZ2xlLmNvbTwvZG9tYWluPgoJPGNvdW50cnkgLz4KCTxzb3VyY2U+QVJJTjwvc291cmNlPgoJPGVtYWlsIC8+Cgk8aW5ldG51bSAvPgoJPG5ldG5hbWUgLz4KCTxkZXNjciAvPgoJPG5zMSAvPgoJPG5zMiAvPgoJPG5zMyAvPgoJPG5zNCAvPgoJPG5zNSAvPgo8L2VudHJ5Pgo=',
                        'source.fqdn': 'accounts.google.com',
                        'source.url': 'http://accounts.google.com./',
                        'source.registry': 'ARIN',
                        'status': 'toggle',
                        'time.observation': '2015-11-02T13:11:43+00:00',
                        'time.source': '2017-10-18T17:48:09+00:00',
                        '__type': 'Event',
                    },
                    ]
VIRUS_REPORT = {"feed.url": "http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=",
                "feed.name": "CleanMX Viruses",
                "__type": "Report",
                "raw": utils.base64_encode(VIRUSES_FILE),
                "time.observation": "2015-11-02T13:11:43+00:00"
                }
VIRUSES_EVENTS = [{
                    'malware.name': 'js.agent.uo.2',
                    'feed.url': 'http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=',
                    'classification.type': 'malware',
                    'status': 'online',
                    'extra.descr': 'Cloudflare, Inc. CLOUD14 101 Townsend Street San Francisco CA 94107',
                    'source.url': 'http://quotescar.typepad.com/24wer.html',
                    'source.geolocation.cc': 'US',
                    'feed.name': 'CleanMX Viruses',
                    'source.ip': '104.16.105.123',
                    'extra.vt_info': 'JS:Trojan.Script.GE JS:Trojan.Script.GE JS.Decode.A JS:Trojan.Script.GE Trojan.IFrame.Script.1 Backdoor ( 04c529b31 ) Backdoor ( 04c529b31 ) JS:Trojan.Script.GE JS.Trojan.Kryptik.rf JS/Crypted.AT.gen JS/Kryptik.BP JS_EXPLOIT.SMDZ JS:Decode-EQ [Trj] Js.Tr',
                    'source.asn': 13335,
                    'extra.inetnum': '104.16.0.0 - 104.31.255.255',
                    'source.fqdn': 'typepad.com',
                    '__type': 'Event',
                    'extra.virustotal': 'http://www.virustotal.com/latest-report.html?resource=14404b4610a945706d802a54eed2429b',
                    'extra.response': 'alive',
                    'extra.review': '104.16.104.123',
                    'extra.ns2': 'roxy.ns.cloudflare.com',
                    'time.observation': '2015-11-02T13:11:43+00:00',
                    'extra.source': 'ARIN',
                    'raw': 'PGVudHJ5PgoJPGxpbmU+MTwvbGluZT4KCTxpZD4xMTI1ODgzNDk8L2lkPgoJPGZpcnN0PjE1MTMxMTc4MTA8L2ZpcnN0PgoJPGxhc3Q+MDwvbGFzdD4KCTxtZDU+MTQ0MDRiNDYxMGE5NDU3MDZkODAyYTU0ZWVkMjQyOWI8L21kNT4KCTx2aXJ1c3RvdGFsPmh0dHA6Ly93d3cudmlydXN0b3RhbC5jb20vbGF0ZXN0LXJlcG9ydC5odG1sP3Jlc291cmNlPTE0NDA0YjQ2MTBhOTQ1NzA2ZDgwMmE1NGVlZDI0MjliPC92aXJ1c3RvdGFsPgoJPHZ0X3Njb3JlPjM2LzU3ICg2My4yJSk8L3Z0X3Njb3JlPgoJPHZ0X2luZm8+SlM6VHJvamFuLlNjcmlwdC5HRSBKUzpUcm9qYW4uU2NyaXB0LkdFIEpTLkRlY29kZS5BIEpTOlRyb2phbi5TY3JpcHQuR0UgVHJvamFuLklGcmFtZS5TY3JpcHQuMSBCYWNrZG9vciAoIDA0YzUyOWIzMSApIEJhY2tkb29yICggMDRjNTI5YjMxICkgSlM6VHJvamFuLlNjcmlwdC5HRSBKUy5Ucm9qYW4uS3J5cHRpay5yZiBKUy9DcnlwdGVkLkFULmdlbiBKUy9LcnlwdGlrLkJQIEpTX0VYUExPSVQuU01EWiBKUzpEZWNvZGUtRVEgW1Ryal0gSnMuVHI8L3Z0X2luZm8+Cgk8c2Nhbm5lcj51bmRlZjwvc2Nhbm5lcj4KCTx2aXJ1c25hbWU+anMuYWdlbnQudW8uMjwvdmlydXNuYW1lPgoJPHVybD5odHRwOi8vcXVvdGVzY2FyLnR5cGVwYWQuY29tLzI0d2VyLmh0bWw8L3VybD4KCTxyZWNlbnQ+dXA8L3JlY2VudD4KCTxyZXNwb25zZT5hbGl2ZTwvcmVzcG9uc2U+Cgk8aXA+MTA0LjE2LjEwNS4xMjM8L2lwPgoJPGFzPkFTMTMzMzU8L2FzPgoJPHJldmlldz4xMDQuMTYuMTA0LjEyMzwvcmV2aWV3PgoJPGRvbWFpbj50eXBlcGFkLmNvbTwvZG9tYWluPgoJPGNvdW50cnk+VVM8L2NvdW50cnk+Cgk8c291cmNlPkFSSU48L3NvdXJjZT4KCTxlbWFpbD5hYnVzZUBjbG91ZGZsYXJlLmNvbTwvZW1haWw+Cgk8aW5ldG51bT4xMDQuMTYuMC4wIC0gMTA0LjMxLjI1NS4yNTU8L2luZXRudW0+Cgk8bmV0bmFtZT5DTE9VREZMQVJFTkVUPC9uZXRuYW1lPgoJPGRlc2NyPkNsb3VkZmxhcmUsIEluYy4gQ0xPVUQxNCAxMDEgVG93bnNlbmQgU3RyZWV0IFNhbiBGcmFuY2lzY28gQ0EgOTQxMDc8L2Rlc2NyPgoJPG5zMT5ub2FoLm5zLmNsb3VkZmxhcmUuY29tPC9uczE+Cgk8bnMyPnJveHkubnMuY2xvdWRmbGFyZS5jb208L25zMj4KCTxuczMgLz4KCTxuczQgLz4KCTxuczUgLz4KPC9lbnRyeT4K',
                    'extra.netname': 'CLOUDFLARENET',
                    'extra.vt_score': '36/57 (63.2%)',
                    'malware.hash.md5': '14404b4610a945706d802a54eed2429b',
                    'source.abuse_contact': 'abuse@cloudflare.com',
                    'extra.ns1': 'noah.ns.cloudflare.com',
                    'extra.id': '112588349',
                    'time.source': '2017-12-12T22:30:10+00:00',
                },
                {
                    'malware.name': 'phishing.html.doc',
                    'feed.url': 'http://support.clean-mx.de/clean-mx/xmlviruses?response=alive&domain=',
                    'classification.type': 'malware',
                    'status': 'online',
                    'extra.descr': 'Netregistry Pty LtdDIT route',
                    'source.url': 'http://nickhookphotography.com/tem/zee/e3cad48b778d59a6613ca12d42547c33/login.php?cmd=login_submit&id=a2e2b7deac4fd185743a14a92f23b617a2e2b7deac4fd185743a14a92f23b617&session=a2e2b7deac4fd185743a14a92f23b617a2e2b7deac4fd185743a14a92f23b617',
                    'source.geolocation.cc': 'AU',
                    'feed.name': 'CleanMX Viruses',
                    'source.ip': '27.121.64.179',
                    'extra.vt_info': 'HTML.Agent.SJ Suspicious_GEN.F47V0920 Phishing.HTML.Doc',
                    'source.asn': 24446,
                    'extra.inetnum': '27.121.64.0 - 27.121.71.255',
                    'source.fqdn': 'nickhookphotography.com',
                    '__type': 'Event',
                    'extra.virustotal': 'http://www.virustotal.com/latest-report.html?resource=a862d6f2238585042948ed1f720ce1f3',
                    'extra.response': 'alive',
                    'extra.review': '27.121.64.179',
                    'extra.ns2': 'ns-1.ezyreg.com',
                    'time.observation': '2015-11-02T13:11:43+00:00',
                    'extra.source': 'APNIC',
                    'raw': 'PGVudHJ5PgoJPGxpbmU+MjwvbGluZT4KCTxpZD4xMTI1ODgzNDY8L2lkPgoJPGZpcnN0PjE1MTMxMTc4MDk8L2ZpcnN0PgoJPGxhc3Q+MDwvbGFzdD4KCTxtZDU+YTg2MmQ2ZjIyMzg1ODUwNDI5NDhlZDFmNzIwY2UxZjM8L21kNT4KCTx2aXJ1c3RvdGFsPmh0dHA6Ly93d3cudmlydXN0b3RhbC5jb20vbGF0ZXN0LXJlcG9ydC5odG1sP3Jlc291cmNlPWE4NjJkNmYyMjM4NTg1MDQyOTQ4ZWQxZjcyMGNlMWYzPC92aXJ1c3RvdGFsPgoJPHZ0X3Njb3JlPjIvNjAgKDMuMyUpPC92dF9zY29yZT4KCTx2dF9pbmZvPkhUTUwuQWdlbnQuU0ogU3VzcGljaW91c19HRU4uRjQ3VjA5MjAgUGhpc2hpbmcuSFRNTC5Eb2M8L3Z0X2luZm8+Cgk8c2Nhbm5lcj51bmRlZjwvc2Nhbm5lcj4KCTx2aXJ1c25hbWU+UGhpc2hpbmcuSFRNTC5Eb2M8L3ZpcnVzbmFtZT4KCTx1cmw+aHR0cDovL25pY2tob29rcGhvdG9ncmFwaHkuY29tL3RlbS96ZWUvZTNjYWQ0OGI3NzhkNTlhNjYxM2NhMTJkNDI1NDdjMzMvbG9naW4ucGhwP2NtZD1sb2dpbl9zdWJtaXQmYW1wO2lkPWEyZTJiN2RlYWM0ZmQxODU3NDNhMTRhOTJmMjNiNjE3YTJlMmI3ZGVhYzRmZDE4NTc0M2ExNGE5MmYyM2I2MTcmYW1wO3Nlc3Npb249YTJlMmI3ZGVhYzRmZDE4NTc0M2ExNGE5MmYyM2I2MTdhMmUyYjdkZWFjNGZkMTg1NzQzYTE0YTkyZjIzYjYxNzwvdXJsPgoJPHJlY2VudD51cDwvcmVjZW50PgoJPHJlc3BvbnNlPmFsaXZlPC9yZXNwb25zZT4KCTxpcD4yNy4xMjEuNjQuMTc5PC9pcD4KCTxhcz5BUzI0NDQ2PC9hcz4KCTxyZXZpZXc+MjcuMTIxLjY0LjE3OTwvcmV2aWV3PgoJPGRvbWFpbj5uaWNraG9va3Bob3RvZ3JhcGh5LmNvbTwvZG9tYWluPgoJPGNvdW50cnk+QVU8L2NvdW50cnk+Cgk8c291cmNlPkFQTklDPC9zb3VyY2U+Cgk8ZW1haWw+YWJ1c2VAbmV0cmVnaXN0cnkuY29tLmF1PC9lbWFpbD4KCTxpbmV0bnVtPjI3LjEyMS42NC4wIC0gMjcuMTIxLjcxLjI1NTwvaW5ldG51bT4KCTxuZXRuYW1lPk5FVFJFR0lTVFJZPC9uZXRuYW1lPgoJPGRlc2NyPk5ldHJlZ2lzdHJ5IFB0eSBMdGRESVQgcm91dGU8L2Rlc2NyPgoJPG5zMT5ucy0yLmV6eXJlZy5jb208L25zMT4KCTxuczI+bnMtMS5lenlyZWcuY29tPC9uczI+Cgk8bnMzIC8+Cgk8bnM0IC8+Cgk8bnM1IC8+CjwvZW50cnk+Cg==',
                    'extra.netname': 'NETREGISTRY',
                    'extra.vt_score': '2/60 (3.3%)',
                    'malware.hash.md5': 'a862d6f2238585042948ed1f720ce1f3',
                    'source.abuse_contact': 'abuse@netregistry.com.au',
                    'extra.ns1': 'ns-2.ezyreg.com',
                    'extra.id': '112588346',
                    'time.source': '2017-12-12T22:30:09+00:00',
                }]


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
        self.assertMessageEqual(2, PHISHING_EVENTS[2])

    def test_viruses(self):
        self.input_message = VIRUS_REPORT
        self.run_bot()
        self.assertMessageEqual(0, VIRUSES_EVENTS[0])
        self.assertMessageEqual(1, VIRUSES_EVENTS[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
