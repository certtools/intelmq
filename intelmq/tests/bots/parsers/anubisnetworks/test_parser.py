# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.anubisnetworks.parser import AnubisNetworksParserBot


EXAMPLE_REPORT = {"feed.url": "https://prod.cyberfeed.net/stream?key=",
                  "feed.accuracy": 100.0,
                  "__type": "Report",
                  "feed.name": "AnubisNetworks",
                  "raw": "eyJfZ2VvX2Vudl9yZW1vdGVfYWRkciI6eyJwYXRoIjoiZW52LnJlbW90ZV9hZGRyIiwiYXNuX25hbWUiOiJFeGFtcGxlQVMiLCJhc24iOjY1NTM2LCJsb25naXR1ZGUiOjEzLCJsYXRpdHVkZSI6MzcsImlwIjoiMjAzLjAuMTEzLjIiLCJuZXRtYXNrIjoyNCwiY291bnRyeV9jb2RlIjoiQVQiLCJjb3VudHJ5X25hbWUiOiJBdXN0cmlhIiwicmVnaW9uIjoiVmllbm5hIiwicmVnaW9uX2NvZGUiOiIwMSIsImNpdHkiOiJWaWVubmEiLCJwb3N0YWxfY29kZSI6IjEwMTAifSwiX3RzIjoxNDg0MDQxNTMwLCJxdHlwZSI6IkEiLCJfb3JpZ2luIjoiZG5zbWFsd2FyZSIsIl9wcm92aWRlciI6InNwaWtlbnMiLCJ0cm9qYW5mYW1pbHkiOiJOaXZkb3J0IiwiZW52Ijp7InNlcnZlcl9wb3J0Ijo4MCwicmVtb3RlX2FkZHIiOiIyMDMuMC4xMTMuMiIsInJlcXVlc3RfbWV0aG9kIjoiUE9TVCJ9fQ==",
                  "time.observation": "2016-04-19T23:16:08+00:00"
                  }

EXAMPLE_EVENT  = {"classification.type": "malware",
                  "destination.port": 80,
                  "feed.accuracy": 100.0,
                  "malware.name": "nivdort",
                  "event_description.text": "Sinkhole attempted connection",
                  "time.source": "2017-01-10T09:45:30+00:00",
                  "source.ip": "203.0.113.2",
                  "source.network": "203.0.113.0/24",
                  "feed.url": "https://prod.cyberfeed.net/stream?key=",
                  "source.geolocation.country": "Austria",
                  "source.geolocation.cc": "AT",
                  "source.geolocation.region": "Vienna",
                  "source.geolocation.city": "Vienna",
                  "source.geolocation.longitude": 13.,
                  "source.geolocation.latitude": 37.,
                  "source.asn": 65536,
                  "source.as_name": "ExampleAS",
                  "time.observation": "2016-04-19T23:16:08+00:00",
                  "__type": "Event",
                  "feed.name": "AnubisNetworks",
                  "raw": EXAMPLE_REPORT['raw'],
                  'extra': '{"request_method": "POST"}',
                  }

EXAMPLE_REPORT2 = {"feed.name": "AnubisNetworks",
                   "feed.accuracy": 100.0,
                   "feed.url": "http://alerts.bitsighttech.com:8080/stream?",
                   "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTcHlBcHAiLCJlbnYiOnsicmVtb"
                          "3RlX3BvcnQiOiI1Mjg4OCIsInNlcnZlcl9uYW1lIjoiZGV2LX"
                          "VwZGF0ZS5pbmZvIiwic2VydmVyX2FkZHIiOiIxOTUuMjIuMjg"
                          "uMTk2IiwicmVxdWVzdF9tZXRob2QiOiJQT1NUIiwicmVtb3Rl"
                          "X2FkZHIiOiIxOTAuMTI0LjY3LjIxMSIsInNlcnZlcl9wb3J0I"
                          "joiODAifSwiX3RzIjoxNDYxMTA3NzU0LCJfZ2VvX2Vudl9yZW"
                          "1vdGVfYWRkciI6eyJjb3VudHJ5X25hbWUiOiJEb21pbmljYW4"
                          "gUmVwdWJsaWMifX0=",
                   "__type": "Report",
                   "time.observation":
                   "2016-04-19T23:16:10+00:00"
                   }

EXAMPLE_EVENT2  = {"feed.name": "AnubisNetworks",
                   "malware.name": "spyapp",
                   "destination.fqdn": "dev-update.info",
                   "source.ip": "190.124.67.211",
                   "destination.ip": "195.22.28.196",
                   "__type": "Event",
                   "source.geolocation.country": "Dominican Republic",
                   "time.source": "2016-04-19T23:15:54+00:00",
                   "source.port": 52888,
                   "time.observation": "2016-04-19T23:16:10+00:00",
                   "extra": "{\"request_method\": \"POST\"}",
                   "feed.url": "http://alerts.bitsighttech.com:8080/stream?",
                   "destination.port": 80,
                   "feed.accuracy": 100.0,
                   "raw": "eyJ0cm9qYW5mYW1pbHkiOiJTcHlBcHAiLCJlbnYiOnsicmVt"
                          "b3RlX3BvcnQiOiI1Mjg4OCIsInNlcnZlcl9uYW1lIjoiZGV2"
                          "LXVwZGF0ZS5pbmZvIiwic2VydmVyX2FkZHIiOiIxOTUuMjIu"
                          "MjguMTk2IiwicmVxdWVzdF9tZXRob2QiOiJQT1NUIiwicmVt"
                          "b3RlX2FkZHIiOiIxOTAuMTI0LjY3LjIxMSIsInNlcnZlcl9w"
                          "b3J0IjoiODAifSwiX3RzIjoxNDYxMTA3NzU0LCJfZ2VvX2Vu"
                          "dl9yZW1vdGVfYWRkciI6eyJjb3VudHJ5X25hbWUiOiJEb21p"
                          "bmljYW4gUmVwdWJsaWMifX0=",
                   "classification.type": "malware",
                   "event_description.text": "Sinkhole attempted connection"
                   }


class TestAnubisNetworksParserBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = AnubisNetworksParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test: report without fqdn """
        self.run_bot()

        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def test_with_fqdn(self):
        """ Test: report with fqdn """
        self.input_message = EXAMPLE_REPORT2
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
