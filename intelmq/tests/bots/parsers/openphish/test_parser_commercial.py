# SPDX-FileCopyrightText: 2018 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.openphish.parser_commercial import OpenPhishCommercialParserBot

INPUT = """\
{"sector": "Telecommunications", "ssl_cert_issued_by": null, "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-f1b3a5cb1cc54864a6067e37086a8508.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357585&Signature=SRbgt2%2BfFpwJdrA6hqCQgK3y1RQ%3D", "url": "http://213.123.230.105/wordpress/press/?email=xxx@t-online.de", "ip": "213.123.230.105", "brand": "Deutsche Telekom", "isotime": "2022-03-22T05:06:25Z", "asn_name": "British Telecommunications PLC", "discover_time": "22-03-2022 05:06:25 UTC", "emails": [], "ssl_cert_issued_to": null, "family_id": "3550555f398b4fa6c66b2654af3113fb", "host": "213.123.230.105", "ssl_cert_serial": null, "country_code": "GB", "tld": "", "country_name": "United Kingdom of Great Britain and Northern Ireland", "phishing_kit": null, "page_language": "de:0.999996133811", "asn": "AS2856"}
{"sector": "e-Commerce", "ssl_cert_issued_by": null, "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-8eca70a1928940eeb1e2aafa1076e061.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357503&Signature=LMzTYuJm2k7mrjLcn9V7L55EbdY%3D", "url": "http://ngutfpg.cn/", "ip": "198.46.189.123", "brand": "Amazon.com Inc.", "isotime": "2022-03-22T05:05:03Z", "asn_name": "ColoCrossing", "discover_time": "22-03-2022 05:05:03 UTC", "emails": [], "ssl_cert_issued_to": null, "family_id": "79e57985c569483971acc71f5657f19d", "host": "ngutfpg.cn", "ssl_cert_serial": null, "country_code": "US", "tld": "cn", "country_name": "United States of America", "phishing_kit": null, "page_language": null, "asn": "AS36352"}
{"sector": "Financial", "ssl_cert_issued_by": "cPanel, Inc.", "screenshot": "https://opdata.s3.amazonaws.com/screenshots/img-dcafc463ad3348b2bd7ad74824bebb57.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357130&Signature=xq9Z3Bz8VaFCuPWmocRZSSASRXc%3D", "url": "https://kmctartscalicut.org/wp-includes/widgets/moi.wellce/zkzywi=/wzmowy=/wiyodg=/", "ip": "216.137.184.250", "brand": "Wells Fargo & Company", "isotime": "2022-03-22T04:58:50Z", "asn_name": "A2 Hosting, Inc.", "discover_time": "22-03-2022 04:58:50 UTC", "emails": ["donflow2021@yahoo.com", "adamhartnet@aol.com", "user0202777a@gmail.com", "9063851193a@gmail.com", "donflowbaba2021@outlook.com"], "ssl_cert_issued_to": "kmctartscalicut.org", "family_id": "4767beae13102eca27ac1914dc40871d", "host": "kmctartscalicut.org", "ssl_cert_serial": "E2E81AF3AC3F4A2B4F1BBC8B35ECFD49", "country_code": "SG", "tld": "org", "country_name": "Singapore", "phishing_kit": "https://opdata.s3.amazonaws.com/kits/202203/7c71721d227dfa91033361d0c6916ae4.zip?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357138&Signature=u0qJfPWIMLCvo2VALFKqUnysiZk%3D", "page_language": null, "asn": "AS55293"}
"""
INPUT_LINES = [utils.base64_encode(f"[{line}]") for line in INPUT.strip().splitlines()]


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
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-f1b3a5cb1cc54864a6067e37086a8508.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357585&Signature=SRbgt2%2BfFpwJdrA6hqCQgK3y1RQ%3D",
    "extra.sector": "Telecommunications",
    "source.url": "http://213.123.230.105/wordpress/press/?email=xxx@t-online.de",
    "raw": INPUT_LINES[0],
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
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-8eca70a1928940eeb1e2aafa1076e061.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357503&Signature=LMzTYuJm2k7mrjLcn9V7L55EbdY%3D",
    "extra.sector": "e-Commerce",
    "extra.tld": "cn",
    "source.url": "http://ngutfpg.cn/",
    "raw": INPUT_LINES[1],
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
    "extra.phishing_kit": "https://opdata.s3.amazonaws.com/kits/202203/7c71721d227dfa91033361d0c6916ae4.zip?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357138&Signature=u0qJfPWIMLCvo2VALFKqUnysiZk%3D",
    "screenshot_url": "https://opdata.s3.amazonaws.com/screenshots/img-dcafc463ad3348b2bd7ad74824bebb57.jpg?AWSAccessKeyId=XXXXXXXXXXXXXXXXXXXX&Expires=1648357130&Signature=xq9Z3Bz8VaFCuPWmocRZSSASRXc%3D",
    "extra.sector": "Financial",
    "extra.ssl_cert_issued_by": "cPanel, Inc.",
    "extra.ssl_cert_issued_to": "kmctartscalicut.org",
    "extra.ssl_cert_serial": "E2E81AF3AC3F4A2B4F1BBC8B35ECFD49",
    "extra.tld": "org",
    "source.url": "https://kmctartscalicut.org/wp-includes/widgets/moi.wellce/zkzywi=/wzmowy=/wiyodg=/",
    "raw": INPUT_LINES[2],
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
