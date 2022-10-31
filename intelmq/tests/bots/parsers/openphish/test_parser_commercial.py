# SPDX-FileCopyrightText: 2018 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.openphish.parser_commercial import OpenPhishCommercialParserBot

INPUT = """\
{"sector": "Telecommunications", "ssl_cert_issued_by": null, "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-f1b3a5cb1cc54864a6067e37086a8508.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357585&Signature=SRbgt2%2BfFpwJdrA6hqCQgK3y1RQ%3D", "url": "http://213.123.230.105/wordpress/press/?email=xxx@t-online.de", "ip": "213.123.230.105", "brand": "Deutsche Telekom", "isotime": "2022-03-22T05:06:25Z", "asn_name": "British Telecommunications PLC", "discover_time": "22-03-2022 05:06:25 UTC", "emails": [], "ssl_cert_issued_to": null, "family_id": "3550555f398b4fa6c66b2654af3113fb", "host": "213.123.230.105", "ssl_cert_serial": null, "country_code": "GB", "tld": "", "country_name": "United Kingdom of Great Britain and Northern Ireland", "phishing_kit": null, "page_language": "de:0.999996133811", "asn": "AS2856"}
{"sector": "e-Commerce", "ssl_cert_issued_by": null, "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-8eca70a1928940eeb1e2aafa1076e061.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357503&Signature=LMzTYuJm2k7mrjLcn9V7L55EbdY%3D", "url": "http://ngutfpg.cn/", "ip": "198.46.189.123", "brand": "Amazon.com Inc.", "isotime": "2022-03-22T05:05:03Z", "asn_name": "ColoCrossing", "discover_time": "22-03-2022 05:05:03 UTC", "emails": [], "ssl_cert_issued_to": null, "family_id": "79e57985c569483971acc71f5657f19d", "host": "ngutfpg.cn", "ssl_cert_serial": null, "country_code": "US", "tld": "cn", "country_name": "United States of America", "phishing_kit": null, "page_language": null, "asn": "AS36352"}
{"sector": "Financial", "ssl_cert_issued_by": "cPanel, Inc.", "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-dcafc463ad3348b2bd7ad74824bebb57.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357130&Signature=xq9Z3Bz8VaFCuPWmocRZSSASRXc%3D", "url": "https://kmctartscalicut.org/wp-includes/widgets/moi.wellce/zkzywi=/wzmowy=/wiyodg=/", "ip": "216.137.184.250", "brand": "Wells Fargo & Company", "isotime": "2022-03-22T04:58:50Z", "asn_name": "A2 Hosting, Inc.", "discover_time": "22-03-2022 04:58:50 UTC", "emails": ["donflow2021@yahoo.com", "adamhartnet@aol.com", "user0202777a@gmail.com", "9063851193a@gmail.com", "donflowbaba2021@outlook.com"], "ssl_cert_issued_to": "kmctartscalicut.org", "family_id": "4767beae13102eca27ac1914dc40871d", "host": "kmctartscalicut.org", "ssl_cert_serial": "E2E81AF3AC3F4A2B4F1BBC8B35ECFD49", "country_code": "SG", "tld": "org", "country_name": "Singapore", "phishing_kit": "https://opdata.s3.amazonaws.com/kits/202203/7c71721d227dfa91033361d0c6916ae4.zip?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357138&Signature=u0qJfPWIMLCvo2VALFKqUnysiZk%3D", "page_language": null, "asn": "AS55293"}
"""

OUTPUT_1 = {
    "classification.type": "phishing",
    "source.asn": 2856,
    "source.as_name": "British Telecommunications PLC",
    "extra.brand": "Deutsche Telekom",
    "source.geolocation.cc": "GB",
    "source.geolocation.country": "United Kingdom of Great Britain and Northern Ireland",
    "extra.emails": [],
    "extra.family_id": "3550555f398b4fa6c66b2654af3113fb",
    "source.ip": "213.123.230.105",
    "time.source": "2022-03-22T05:06:25+00:00",
    "extra.page_language": "de:0.999996133811",
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-f1b3a5cb1cc54864a6067e37086a8508.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357585&Signature=SRbgt2%2BfFpwJdrA6hqCQgK3y1RQ%3D",
    "extra.sector": "Telecommunications",
    "source.url": "http://213.123.230.105/wordpress/press/?email=xxx@t-online.de",
    "raw": "W3sic2VjdG9yIjogIlRlbGVjb21tdW5pY2F0aW9ucyIsICJzc2xfY2VydF9pc3N1ZWRfYnkiOiBudWxsLCAic2NyZWVuc2hvdCI6ICJodHRwczovL29wZGF0YS5zMy5hbWF6b25hd3MuY29tL3NjcmVlbnNob3RzL2ltZy1mMWIzYTVjYjFjYzU0ODY0YTYwNjdlMzcwODZhODUwOC5qcGc/QVdTQWNjZXNzS2V5SWQ9QUtJQTIzU1ZGV1lYS1RRTDZFUEkmRXhwaXJlcz0xNjQ4MzU3NTg1JlNpZ25hdHVyZT1TUmJndDIlMkJmRnB3SmRyQTZocUNRZ0szeTFSUSUzRCIsICJ1cmwiOiAiaHR0cDovLzIxMy4xMjMuMjMwLjEwNS93b3JkcHJlc3MvcHJlc3MvP2VtYWlsPXh4eEB0LW9ubGluZS5kZSIsICJpcCI6ICIyMTMuMTIzLjIzMC4xMDUiLCAiYnJhbmQiOiAiRGV1dHNjaGUgVGVsZWtvbSIsICJpc290aW1lIjogIjIwMjItMDMtMjJUMDU6MDY6MjVaIiwgImFzbl9uYW1lIjogIkJyaXRpc2ggVGVsZWNvbW11bmljYXRpb25zIFBMQyIsICJkaXNjb3Zlcl90aW1lIjogIjIyLTAzLTIwMjIgMDU6MDY6MjUgVVRDIiwgImVtYWlscyI6IFtdLCAic3NsX2NlcnRfaXNzdWVkX3RvIjogbnVsbCwgImZhbWlseV9pZCI6ICIzNTUwNTU1ZjM5OGI0ZmE2YzY2YjI2NTRhZjMxMTNmYiIsICJob3N0IjogIjIxMy4xMjMuMjMwLjEwNSIsICJzc2xfY2VydF9zZXJpYWwiOiBudWxsLCAiY291bnRyeV9jb2RlIjogIkdCIiwgInRsZCI6ICIiLCAiY291bnRyeV9uYW1lIjogIlVuaXRlZCBLaW5nZG9tIG9mIEdyZWF0IEJyaXRhaW4gYW5kIE5vcnRoZXJuIElyZWxhbmQiLCAicGhpc2hpbmdfa2l0IjogbnVsbCwgInBhZ2VfbGFuZ3VhZ2UiOiAiZGU6MC45OTk5OTYxMzM4MTEiLCAiYXNuIjogIkFTMjg1NiJ9XQ==",
    "__type": "Event"
}

OUTPUT_2 = {
    "classification.type": "phishing",
    "source.asn": 36352,
    "source.as_name": "ColoCrossing",
    "extra.brand": "Amazon.com Inc.",
    "source.geolocation.cc": "US",
    "source.geolocation.country": "United States of America",
    "extra.emails": [],
    "extra.family_id": "79e57985c569483971acc71f5657f19d",
    "source.fqdn": "ngutfpg.cn",
    "source.ip": "198.46.189.123",
    "time.source": "2022-03-22T05:05:03+00:00",
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-8eca70a1928940eeb1e2aafa1076e061.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357503&Signature=LMzTYuJm2k7mrjLcn9V7L55EbdY%3D",
    "extra.sector": "e-Commerce",
    "extra.tld": "cn",
    "source.url": "http://ngutfpg.cn/",
    "raw": "W3sic2VjdG9yIjogImUtQ29tbWVyY2UiLCAic3NsX2NlcnRfaXNzdWVkX2J5IjogbnVsbCwgInNjcmVlbnNob3QiOiAiaHR0cHM6Ly9vcGRhdGEuczMuYW1hem9uYXdzLmNvbS9zY3JlZW5zaG90cy9pbWctOGVjYTcwYTE5Mjg5NDBlZWIxZTJhYWZhMTA3NmUwNjEuanBnP0FXU0FjY2Vzc0tleUlkPUFLSUEyM1NWRldZWEtUUUw2RVBJJkV4cGlyZXM9MTY0ODM1NzUwMyZTaWduYXR1cmU9TE16VFl1Sm0yazdtcmpMY245VjdMNTVFYmRZJTNEIiwgInVybCI6ICJodHRwOi8vbmd1dGZwZy5jbi8iLCAiaXAiOiAiMTk4LjQ2LjE4OS4xMjMiLCAiYnJhbmQiOiAiQW1hem9uLmNvbSBJbmMuIiwgImlzb3RpbWUiOiAiMjAyMi0wMy0yMlQwNTowNTowM1oiLCAiYXNuX25hbWUiOiAiQ29sb0Nyb3NzaW5nIiwgImRpc2NvdmVyX3RpbWUiOiAiMjItMDMtMjAyMiAwNTowNTowMyBVVEMiLCAiZW1haWxzIjogW10sICJzc2xfY2VydF9pc3N1ZWRfdG8iOiBudWxsLCAiZmFtaWx5X2lkIjogIjc5ZTU3OTg1YzU2OTQ4Mzk3MWFjYzcxZjU2NTdmMTlkIiwgImhvc3QiOiAibmd1dGZwZy5jbiIsICJzc2xfY2VydF9zZXJpYWwiOiBudWxsLCAiY291bnRyeV9jb2RlIjogIlVTIiwgInRsZCI6ICJjbiIsICJjb3VudHJ5X25hbWUiOiAiVW5pdGVkIFN0YXRlcyBvZiBBbWVyaWNhIiwgInBoaXNoaW5nX2tpdCI6IG51bGwsICJwYWdlX2xhbmd1YWdlIjogbnVsbCwgImFzbiI6ICJBUzM2MzUyIn1d",
    "__type": "Event"
}

OUTPUT_3 = {
    "classification.type": "phishing",
    "source.asn": 55293,
    "source.as_name": "A2 Hosting, Inc.",
    "extra.brand": "Wells Fargo & Company",
    "source.geolocation.cc": "SG",
    "source.geolocation.country": "Singapore",
    "extra.emails": [
        "donflow2021@yahoo.com",
        "adamhartnet@aol.com",
        "user0202777a@gmail.com",
        "9063851193a@gmail.com",
        "donflowbaba2021@outlook.com"
    ],
    "extra.family_id": "4767beae13102eca27ac1914dc40871d",
    "source.fqdn": "kmctartscalicut.org",
    "source.ip": "216.137.184.250",
    "time.source": "2022-03-22T04:58:50+00:00",
    "extra.phishing_kit": "https://opdata.s3.amazonaws.com/kits/202203/7c71721d227dfa91033361d0c6916ae4.zip?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357138&Signature=u0qJfPWIMLCvo2VALFKqUnysiZk%3D",
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-dcafc463ad3348b2bd7ad74824bebb57.jpg?AWSAccessKeyId=AKIA23SVFWYXKTQL6EPI&Expires=1648357130&Signature=xq9Z3Bz8VaFCuPWmocRZSSASRXc%3D",
    "extra.sector": "Financial",
    "extra.ssl_cert_issued_by": "cPanel, Inc.",
    "extra.ssl_cert_issued_to": "kmctartscalicut.org",
    "extra.ssl_cert_serial": "E2E81AF3AC3F4A2B4F1BBC8B35ECFD49",
    "extra.tld": "org",
    "source.url": "https://kmctartscalicut.org/wp-includes/widgets/moi.wellce/zkzywi=/wzmowy=/wiyodg=/",
    "raw": "W3sic2VjdG9yIjogIkZpbmFuY2lhbCIsICJzc2xfY2VydF9pc3N1ZWRfYnkiOiAiY1BhbmVsLCBJbmMuIiwgInNjcmVlbnNob3QiOiAiaHR0cHM6Ly9vcGRhdGEuczMuYW1hem9uYXdzLmNvbS9zY3JlZW5zaG90cy9pbWctZGNhZmM0NjNhZDMzNDhiMmJkN2FkNzQ4MjRiZWJiNTcuanBnP0FXU0FjY2Vzc0tleUlkPUFLSUEyM1NWRldZWEtUUUw2RVBJJkV4cGlyZXM9MTY0ODM1NzEzMCZTaWduYXR1cmU9eHE5WjNCejhWYUZDdVBXbW9jUlpTU0FTUlhjJTNEIiwgInVybCI6ICJodHRwczovL2ttY3RhcnRzY2FsaWN1dC5vcmcvd3AtaW5jbHVkZXMvd2lkZ2V0cy9tb2kud2VsbGNlL3prenl3aT0vd3ptb3d5PS93aXlvZGc9LyIsICJpcCI6ICIyMTYuMTM3LjE4NC4yNTAiLCAiYnJhbmQiOiAiV2VsbHMgRmFyZ28gJiBDb21wYW55IiwgImlzb3RpbWUiOiAiMjAyMi0wMy0yMlQwNDo1ODo1MFoiLCAiYXNuX25hbWUiOiAiQTIgSG9zdGluZywgSW5jLiIsICJkaXNjb3Zlcl90aW1lIjogIjIyLTAzLTIwMjIgMDQ6NTg6NTAgVVRDIiwgImVtYWlscyI6IFsiZG9uZmxvdzIwMjFAeWFob28uY29tIiwgImFkYW1oYXJ0bmV0QGFvbC5jb20iLCAidXNlcjAyMDI3NzdhQGdtYWlsLmNvbSIsICI5MDYzODUxMTkzYUBnbWFpbC5jb20iLCAiZG9uZmxvd2JhYmEyMDIxQG91dGxvb2suY29tIl0sICJzc2xfY2VydF9pc3N1ZWRfdG8iOiAia21jdGFydHNjYWxpY3V0Lm9yZyIsICJmYW1pbHlfaWQiOiAiNDc2N2JlYWUxMzEwMmVjYTI3YWMxOTE0ZGM0MDg3MWQiLCAiaG9zdCI6ICJrbWN0YXJ0c2NhbGljdXQub3JnIiwgInNzbF9jZXJ0X3NlcmlhbCI6ICJFMkU4MUFGM0FDM0Y0QTJCNEYxQkJDOEIzNUVDRkQ0OSIsICJjb3VudHJ5X2NvZGUiOiAiU0ciLCAidGxkIjogIm9yZyIsICJjb3VudHJ5X25hbWUiOiAiU2luZ2Fwb3JlIiwgInBoaXNoaW5nX2tpdCI6ICJodHRwczovL29wZGF0YS5zMy5hbWF6b25hd3MuY29tL2tpdHMvMjAyMjAzLzdjNzE3MjFkMjI3ZGZhOTEwMzMzNjFkMGM2OTE2YWU0LnppcD9BV1NBY2Nlc3NLZXlJZD1BS0lBMjNTVkZXWVhLVFFMNkVQSSZFeHBpcmVzPTE2NDgzNTcxMzgmU2lnbmF0dXJlPXUwcUpmUFdJTUxDdm8yVkFMRktxVW55c2laayUzRCIsICJwYWdlX2xhbmd1YWdlIjogbnVsbCwgImFzbiI6ICJBUzU1MjkzIn1d",
    "__type": "Event"
}


class TestOpenPhishCommercialParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenPhishCommercialParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenPhishCommercialParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': utils.base64_encode(INPUT)}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_1)
        self.assertMessageEqual(1, OUTPUT_2)
        self.assertMessageEqual(2, OUTPUT_3)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
