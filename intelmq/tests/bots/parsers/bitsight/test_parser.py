# -*- coding: utf-8 -*-

import unittest
import intelmq.lib.test as test
from intelmq.bots.parsers.bitsight.parser import BitsightParserBot


EXAMPLE_REPORT = {"feed.name": "BitSight", 
                  "__type": "Report", 
                  "raw": "eyJfdHMiOjE0NjA5ODQ5MzksImVudiI6eyJyZXF1ZXN0X21ldGhvZCI6IkdFVC"
                  "IsInNlcnZlcl9hZGRyIjoiMTk1LjIyLjI4LjE5NiIsInNlcnZlcl9wb3J0IjoiODAiLCJ"
                  "yZW1vdGVfYWRkciI6Ijg1LjI0My4xMjkuMTg0IiwicmVtb3RlX3BvcnQiOiI1MjA4NiIs"
                  "InNlcnZlcl9uYW1lIjoiY3lzdGFseDAyLmNvbSJ9LCJ0cm9qYW5mYW1pbHkiOiJDYXJ1Z"
                  "mF4IiwiX2dlb19lbnZfcmVtb3RlX2FkZHIiOnsiY291bnRyeV9uYW1lIjoiUG9ydHVnYWwifX0=", 
                  "feed.accuracy": 100.0, 
                  "feed.url": "http://alerts.bitsighttech.com:8080/stream?", 
                  "time.observation": "2016-04-18T13:08:59+00:00"}

EXAMPLE_EVENT = {"extra": "{\"request_method\": \"GET\"}", 
                "source.port": 52086, 
                "source.ip": "85.243.129.184", 
                "event_description.text": "Sinkhole attempted connection", 
                "feed.name": "BitSight", 
                "feed.accuracy": 100.0, 
                "feed.url": "http://alerts.bitsighttech.com:8080/stream?", 
                "raw": "ZXlKZmRITWlPakUwTmpBNU9EUTVNemtzSW1WdWRpSTZleUp5WlhGMVpYTjBYMjFsZEd"
                "odlpDSTZJa2RGVkNJc0luTmxjblpsY2w5aFpHUnlJam9pTVRrMUxqSXlMakk0TGpFNU5pSXNJb"
                "k5sY25abGNsOXdiM0owSWpvaU9EQWlMQ0p5WlcxdmRHVmZZV1JrY2lJNklqZzFMakkwTXk0eE1"
                "qa3VNVGcwSWl3aWNtVnRiM1JsWDNCdmNuUWlPaUkxTWpBNE5pSXNJbk5sY25abGNsOXVZVzFsS"
                "WpvaVkzbHpkR0ZzZURBeUxtTnZiU0o5TENKMGNtOXFZVzVtWVcxcGJIa2lPaUpEWVhKMVptRjR"
                "JaXdpWDJkbGIxOWxiblpmY21WdGIzUmxYMkZrWkhJaU9uc2lZMjkxYm5SeWVWOXVZVzFsSWpvaVVHOXlkSFZuWVd3aWZYMD0=", 
                "time.observation": "2016-04-18T13:08:59+00:00", 
                "time.source": "2016-04-18T13:08:59+00:00", 
                "malware.name": "carufax", 
                "destination.fqdn": "cystalx02.com", 
                "destination.port": 80, 
                "destination.ip": "195.22.28.196", 
                "__type": "Event",
                "classification.type": "malware"
                }


class TestBitsightParserBot(test.BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = BitsightParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
