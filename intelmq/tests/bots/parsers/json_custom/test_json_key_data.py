# -*- coding: utf-8 -*-
import base64
import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.json_custom.parser import JSONCustomParserBot

with open(os.path.join(os.path.dirname(__file__), 'json_key_data.json'), 'rb') as fh:
    RAW = base64.b64encode(fh.read()).decode()

REPORT = {"feed.name": "Test Feed",
          "raw": RAW,
          "__type": "Report",
          }
EVENT = {'__type': 'Event',
         'classification.type': 'malware',
         'extra.tags': ['SSH Scanner', 'SSH Worm'],
         'feed.name': 'Test Feed',
         'raw': 'eyJpcCI6ICIxNzkuMTI0LjM2LjE5NiIsICJzZWVuIjogdHJ1ZSwgImNsYXNzaWZpY2F0aW9'
                'uIjogIm1hbGljaW91cyIsICJzcG9vZmFibGUiOiBmYWxzZSwgImZpcnN0X3NlZW4iOiAiMj'
                'AyMC0wMS0xMyIsICJsYXN0X3NlZW4iOiAiMjAyMC0xMi0xNCIsICJhY3RvciI6ICJ1bmtub'
                '3duIiwgInRhZ3MiOiBbIlNTSCBTY2FubmVyIiwgIlNTSCBXb3JtIl0sICJjdmUiOiBbXSwg'
                'Im1ldGFkYXRhIjogeyJjb3VudHJ5IjogIkJyYXppbCIsICJjb3VudHJ5X2NvZGUiOiAiQlI'
                'iLCAiY2l0eSI6ICJTXHUwMGUzbyBQYXVsbyIsICJvcmdhbml6YXRpb24iOiAiRVFVSU5JWC'
                'BCUkFTSUwiLCAicmVnaW9uIjogIlNcdTAwZTNvIFBhdWxvIiwgInJkbnMiOiAiMTk2LjM2L'
                'jEyNC4xNzkuc3RhdGljLnNwMi5hbG9nLmNvbS5iciIsICJhc24iOiAiQVMxNjM5NyIsICJ0'
                'b3IiOiBmYWxzZSwgIm9zIjogIkxpbnV4IDMuMS0zLjEwIiwgImNhdGVnb3J5IjogImlzcCI'
                'sICJ2cG4iOiBmYWxzZSwgInZwbl9zZXJ2aWNlIjogIiJ9LCAicmF3X2RhdGEiOiB7InNjYW'
                '4iOiBbeyJwb3J0IjogMjIsICJwcm90b2NvbCI6ICJUQ1AifSwgeyJwb3J0IjogMjIyMiwgI'
                'nByb3RvY29sIjogIlRDUCJ9XSwgIndlYiI6IHt9LCAiamEzIjogW119LCAiX190eXBlIjog'
                'ImRpY3QifQ==',
         'time.source': '2020-12-14T00:00:00+00:00',
         'source.ip': '179.124.36.196'
         }


class TestJSONCustomParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a JSONCustomParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = JSONCustomParserBot

    def test_sample(self):
        """ Test if correct Event has been produced. """
        self.input_message = REPORT
        self.sysconfig = {"json_data_format": True,
                          "json_data_key": "data",
                          "type": "malware",
                          "time_format": "from_format_midnight|%Y-%m-%d",
                          "translate_fields": {"source.ip": "ip",
                                               "time.source": "last_seen",
                                               "extra.tags": "tags"
                                               }
                          }
        self.run_bot()
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
