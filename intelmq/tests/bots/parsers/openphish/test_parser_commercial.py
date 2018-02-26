# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.openphish.parser_commercial import OpenPhishCommercialParserBot

with open(os.path.join(os.path.dirname(__file__), 'feed_commercial.txt'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

OUTPUT1 = {"source.url": "http://example.com/glossy/zip/secure/d553c33636b465c21554b757e48bcf04/", "source.ip": "104.24.119.70", "time.source": "2018-02-06T15:16:06+00:00", "source.as_name": "Example Pete", "source.asn": 13335, "source.fqdn": "example.com", "source.geolocation.cc": "US", "raw": "eyJzZWN0b3IiOiAiRW1haWwgUHJvdmlkZXIiLCAidXJsIjogImh0dHA6Ly9leGFtcGxlLmNvbS9nbG9zc3kvemlwL3NlY3VyZS9kNTUzYzMzNjM2YjQ2NWMyMTU1NGI3NTdlNDhiY2YwNC8iLCAiaXAiOiAiMTA0LjI0LjExOS43MCIsICJicmFuZCI6ICJXZWJtYWlsIFByb3ZpZGVycyIsICJpc290aW1lIjogIjIwMTgtMDItMDZUMTU6MTY6MDZaIiwgImFzbl9uYW1lIjogIkV4YW1wbGUgUGV0ZSIsICJkaXNjb3Zlcl90aW1lIjogIjA2LTAyLTIwMTggMTU6MTY6MDYgVVRDIiwgImFzbiI6ICJBUzEzMzM1IiwgImZhbWlseV9pZCI6ICI5MjIwNzA2MDNhOTZkODFiZTBlMzU0MDk5ZDYyZjU0ZSIsICJob3N0IjogImV4YW1wbGUuY29tIiwgImNvdW50cnlfY29kZSI6ICJVUyIsICJ0bGQiOiAiZ2EiLCAiY291bnRyeV9uYW1lIjogIlVuaXRlZCBTdGF0ZXMiLCAicGhpc2hpbmdfa2l0IjogbnVsbCwgImVtYWlscyI6IFtdfQ==", "extra.brand": "Webmail Providers", "extra.country_name": "United States", "extra.discover_time": "06-02-2018 15:16:06 UTC", "extra.family_id": "922070603a96d81be0e354099d62f54e", "extra.phishing_kit": None, "extra.sector": "Email Provider", "extra.tld": "ga", "classification.type": "phishing", "__type": "Event"}
OUTPUT2 = {"source.url": "http://signin.eby.de.h7r9pganeatdzn6.civpro.example.com/?Ct5A47GsT3bMpTNwYXCmsa6JR7ylCJx2tpr3GordYJZnl", "source.ip": "196.41.123.211", "time.source": "2018-02-06T15:13:22+00:00", "source.as_name": "Example Richard", "source.asn": 36874, "source.fqdn": "signin.eby.de.h7r9pganeatdzn6.civpro.example.com", "source.geolocation.cc": "ZA", "raw": "eyJzZWN0b3IiOiAiZS1Db21tZXJjZSIsICJ1cmwiOiAiaHR0cDovL3NpZ25pbi5lYnkuZGUuaDdyOXBnYW5lYXRkem42LmNpdnByby5leGFtcGxlLmNvbS8/Q3Q1QTQ3R3NUM2JNcFROd1lYQ21zYTZKUjd5bENKeDJ0cHIzR29yZFlKWm5sIiwgImlwIjogIjE5Ni40MS4xMjMuMjExIiwgImJyYW5kIjogImVCYXkgSW5jLiIsICJpc290aW1lIjogIjIwMTgtMDItMDZUMTU6MTM6MjJaIiwgImFzbl9uYW1lIjogIkV4YW1wbGUgUmljaGFyZCIsICJkaXNjb3Zlcl90aW1lIjogIjA2LTAyLTIwMTggMTU6MTM6MjIgVVRDIiwgImFzbiI6ICJBUzM2ODc0IiwgImZhbWlseV9pZCI6ICIzNTEzNzAyZTA3OGI2ZTZkNzBiYjdmOWFiYmY0MGNkNiIsICJob3N0IjogInNpZ25pbi5lYnkuZGUuaDdyOXBnYW5lYXRkem42LmNpdnByby5leGFtcGxlLmNvbSIsICJjb3VudHJ5X2NvZGUiOiAiWkEiLCAidGxkIjogImNvLnphIiwgImNvdW50cnlfbmFtZSI6ICJTb3V0aCBBZnJpY2EiLCAicGhpc2hpbmdfa2l0IjogbnVsbCwgImVtYWlscyI6IFtdfQ==", "extra.brand": "eBay Inc.", "extra.country_name": "South Africa", "extra.discover_time": "06-02-2018 15:13:22 UTC", "extra.family_id": "3513702e078b6e6d70bb7f9abbf40cd6", "extra.phishing_kit": None, "extra.sector": "e-Commerce", "extra.tld": "co.za", "classification.type": "phishing", "__type": "Event"}

class TestOpenPhishCommercialParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for OpenPhishCommercialParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = OpenPhishCommercialParserBot
        cls.default_input_message = {'__type': 'Report', 'raw': RAW}

    def test_event(self):
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT1)
        self.assertMessageEqual(1, OUTPUT2)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
