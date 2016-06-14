# -*- coding: utf-8 -*-

import json
import unittest

from intelmq.lib import test
from intelmq.lib.utils import base64_decode
from intelmq.bots.parsers.misp.parser import MISPParserBot

EXAMPLE_REPORT = {
    "__type": "Report",
    "feed.accuracy": 100.0,
    "feed.name": "misp_test",
    "feed.url": "http://192.168.56.102/",
    "time.observation": "2016-06-11T23:24:28+00:00",
    "raw": "W3siaW5mbyI6ICJBIFJhbmRvbSBFdmVudCIsICJwdWJsaXNoX3RpbWVzdGFtcCI6"
           "ICIwIiwgImlkIjogIjIiLCAiUmVsYXRlZEV2ZW50IjogW10sICJkYXRlIjogIjIw"
           "MTYtMDYtMDkiLCAiVGFnIjogW3siZXhwb3J0YWJsZSI6IHRydWUsICJjb2xvdXIi"
           "OiAiIzAwNWE1YSIsICJuYW1lIjogImVjc2lydDptYWxpY2lvdXMtY29kZT1cInJh"
           "bnNvbXdhcmVcIiIsICJpZCI6ICI2In0sIHsiZXhwb3J0YWJsZSI6IHRydWUsICJj"
           "b2xvdXIiOiAiIzBmZjU0MSIsICJuYW1lIjogInByb2Nlc3NlZF9ieV9pbnRlbG1x"
           "IiwgImlkIjogIjIifSwgeyJleHBvcnRhYmxlIjogdHJ1ZSwgImNvbG91ciI6ICIj"
           "MTQyYmY3IiwgIm5hbWUiOiAiZm9yX2ludGVsbXFfcHJvY2Vzc2luZyIsICJpZCI6"
           "ICIxIn1dLCAidXVpZCI6ICI1NzU4ZWJmNS1jODk4LTQ4ZTYtOWZlOS01NjY1YzBh"
           "ODM4NjYiLCAiQXR0cmlidXRlIjogW3siY2F0ZWdvcnkiOiAiUGF5bG9hZCBkZWxp"
           "dmVyeSIsICJkaXN0cmlidXRpb24iOiAiNSIsICJ2YWx1ZSI6ICJodHRwOi8vZmFr"
           "ZS53ZWJzaXRlLmNvbS9tYWx3YXJlL2lzL2hlcmUiLCAidG9faWRzIjogZmFsc2Us"
           "ICJjb21tZW50IjogIiIsICJldmVudF9pZCI6ICIyIiwgInNoYXJpbmdfZ3JvdXBf"
           "aWQiOiAiMCIsICJkZWxldGVkIjogZmFsc2UsICJ0aW1lc3RhbXAiOiAiMTQ2NTY4"
           "MTMwNCIsICJTaGFyaW5nR3JvdXAiOiBbXSwgInV1aWQiOiAiNTc1Yzg1OTgtZjFm"
           "MC00YzE2LWE5NGEtMDYxMmMwYTgzODY2IiwgImlkIjogIjciLCAidHlwZSI6ICJ1"
           "cmwiLCAiU2hhZG93QXR0cmlidXRlIjogW119LCB7ImNhdGVnb3J5IjogIlBheWxv"
           "YWQgdHlwZSIsICJkaXN0cmlidXRpb24iOiAiNSIsICJ2YWx1ZSI6ICJMb2NreSIs"
           "ICJ0b19pZHMiOiBmYWxzZSwgImNvbW1lbnQiOiAiIiwgImV2ZW50X2lkIjogIjIi"
           "LCAic2hhcmluZ19ncm91cF9pZCI6ICIwIiwgImRlbGV0ZWQiOiBmYWxzZSwgInRp"
           "bWVzdGFtcCI6ICIxNDY1NjgxODAxIiwgIlNoYXJpbmdHcm91cCI6IFtdLCAidXVp"
           "ZCI6ICI1NzVjODU0OS05MDEwLTQ1NTUtOGIzNy0wNTdhYzBhODM4NjYiLCAiaWQi"
           "OiAiNiIsICJ0eXBlIjogInRleHQiLCAiU2hhZG93QXR0cmlidXRlIjogW119XSwg"
           "Im9yZ19pZCI6ICIxIiwgInRocmVhdF9sZXZlbF9pZCI6ICIxIiwgIlNoYWRvd0F0"
           "dHJpYnV0ZSI6IFtdLCAiZGlzdHJpYnV0aW9uIjogIjAiLCAiT3JnIjogeyJ1dWlk"
           "IjogIjU3NTg2ZTlhLTRhNjQtNGY3OS05MDA5LTRkYzFjMGE4Mzg2NiIsICJuYW1l"
           "IjogIk9SR05BTUUiLCAiaWQiOiAiMSJ9LCAiT3JnYyI6IHsidXVpZCI6ICI1NzU4"
           "NmU5YS00YTY0LTRmNzktOTAwOS00ZGMxYzBhODM4NjYiLCAibmFtZSI6ICJPUkdO"
           "QU1FIiwgImlkIjogIjEifSwgImF0dHJpYnV0ZV9jb3VudCI6ICIyIiwgInNoYXJp"
           "bmdfZ3JvdXBfaWQiOiAiMCIsICJwcm9wb3NhbF9lbWFpbF9sb2NrIjogZmFsc2Us"
           "ICJhbmFseXNpcyI6ICIwIiwgInRpbWVzdGFtcCI6ICIxNDY1NjgxODAxIiwgImxv"
           "Y2tlZCI6IGZhbHNlLCAicHVibGlzaGVkIjogZmFsc2UsICJvcmdjX2lkIjogIjEi"
           "fV0=",
}

EXAMPLE_EVENT = {
    "__type": "Event",
    "feed.accuracy": 100.0,
    "feed.name": "misp_test",
    "feed.url": "http://192.168.56.102/",
    "time.observation": "2016-06-11T23:24:28+00:00",
    "time.source": "2016-06-12T07:41:44+00:00",
    "source.url": "http://fake.website.com/malware/is/here",
    "event_description.text": "Payload delivery",
    "event_description.url": "http://192.168.56.102/event/view/2",
    "classification.type": "ransomware",
    "malware.name": "locky",
    "raw": "eyJhbmFseXNpcyI6ICIwIiwgIk9yZ2MiOiB7ImlkIjogIjEiLCAidXVpZCI6ICI1"
           "NzU4NmU5YS00YTY0LTRmNzktOTAwOS00ZGMxYzBhODM4NjYiLCAibmFtZSI6ICJP"
           "UkdOQU1FIn0sICJSZWxhdGVkRXZlbnQiOiBbXSwgIm9yZ2NfaWQiOiAiMSIsICJv"
           "cmdfaWQiOiAiMSIsICJUYWciOiBbeyJpZCI6ICI2IiwgIm5hbWUiOiAiZWNzaXJ0"
           "Om1hbGljaW91cy1jb2RlPVwicmFuc29td2FyZVwiIiwgImV4cG9ydGFibGUiOiB0"
           "cnVlLCAiY29sb3VyIjogIiMwMDVhNWEifSwgeyJpZCI6ICIyIiwgIm5hbWUiOiAi"
           "cHJvY2Vzc2VkX2J5X2ludGVsbXEiLCAiZXhwb3J0YWJsZSI6IHRydWUsICJjb2xv"
           "dXIiOiAiIzBmZjU0MSJ9LCB7ImlkIjogIjEiLCAibmFtZSI6ICJmb3JfaW50ZWxt"
           "cV9wcm9jZXNzaW5nIiwgImV4cG9ydGFibGUiOiB0cnVlLCAiY29sb3VyIjogIiMx"
           "NDJiZjcifV0sICJpbmZvIjogIkEgUmFuZG9tIEV2ZW50IiwgImlkIjogIjIiLCAi"
           "cHJvcG9zYWxfZW1haWxfbG9jayI6IGZhbHNlLCAidXVpZCI6ICI1NzU4ZWJmNS1j"
           "ODk4LTQ4ZTYtOWZlOS01NjY1YzBhODM4NjYiLCAicHVibGlzaGVkIjogZmFsc2Us"
           "ICJ0aHJlYXRfbGV2ZWxfaWQiOiAiMSIsICJPcmciOiB7ImlkIjogIjEiLCAidXVp"
           "ZCI6ICI1NzU4NmU5YS00YTY0LTRmNzktOTAwOS00ZGMxYzBhODM4NjYiLCAibmFt"
           "ZSI6ICJPUkdOQU1FIn0sICJkYXRlIjogIjIwMTYtMDYtMDkiLCAiU2hhZG93QXR0"
           "cmlidXRlIjogW10sICJBdHRyaWJ1dGUiOiBbeyJ2YWx1ZSI6ICJodHRwOi8vZmFr"
           "ZS53ZWJzaXRlLmNvbS9tYWx3YXJlL2lzL2hlcmUiLCAiZGVsZXRlZCI6IGZhbHNl"
           "LCAiU2hhZG93QXR0cmlidXRlIjogW10sICJldmVudF9pZCI6ICIyIiwgIlNoYXJp"
           "bmdHcm91cCI6IFtdLCAic2hhcmluZ19ncm91cF9pZCI6ICIwIiwgImlkIjogIjci"
           "LCAiZGlzdHJpYnV0aW9uIjogIjUiLCAidXVpZCI6ICI1NzVjODU5OC1mMWYwLTRj"
           "MTYtYTk0YS0wNjEyYzBhODM4NjYiLCAiY2F0ZWdvcnkiOiAiUGF5bG9hZCBkZWxp"
           "dmVyeSIsICJjb21tZW50IjogIiIsICJ0eXBlIjogInVybCIsICJ0aW1lc3RhbXAi"
           "OiAiMTQ2NTY4MTMwNCIsICJ0b19pZHMiOiBmYWxzZX0sIHsidmFsdWUiOiAiTG9j"
           "a3kiLCAiZGVsZXRlZCI6IGZhbHNlLCAiU2hhZG93QXR0cmlidXRlIjogW10sICJl"
           "dmVudF9pZCI6ICIyIiwgIlNoYXJpbmdHcm91cCI6IFtdLCAic2hhcmluZ19ncm91"
           "cF9pZCI6ICIwIiwgImlkIjogIjYiLCAiZGlzdHJpYnV0aW9uIjogIjUiLCAidXVp"
           "ZCI6ICI1NzVjODU0OS05MDEwLTQ1NTUtOGIzNy0wNTdhYzBhODM4NjYiLCAiY2F0"
           "ZWdvcnkiOiAiUGF5bG9hZCB0eXBlIiwgImNvbW1lbnQiOiAiIiwgInR5cGUiOiAi"
           "dGV4dCIsICJ0aW1lc3RhbXAiOiAiMTQ2NTY4MTgwMSIsICJ0b19pZHMiOiBmYWxz"
           "ZX1dLCAiYXR0cmlidXRlX2NvdW50IjogIjIiLCAic2hhcmluZ19ncm91cF9pZCI6"
           "ICIwIiwgImRpc3RyaWJ1dGlvbiI6ICIwIiwgImxvY2tlZCI6IGZhbHNlLCAicHVi"
           "bGlzaF90aW1lc3RhbXAiOiAiMCIsICJ0aW1lc3RhbXAiOiAiMTQ2NTY4MTgwMSJ9",
}


class TestMISPParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for the MISPParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = MISPParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)

    def assertMessageEqual(self, queue_pos, expected_msg):
        """
        Override test.BotTestCase.assertMessageEqual to allow
        comparison of the 'raw' as a dict. The MISP event is a JSON
        encoded dict which serializes non-deterministically because a
        dict is not ordered.
        """
        event = self.get_output_queue()[queue_pos]
        self.assertIsInstance(event, str)

        event_dict = json.loads(event)
        expected = expected_msg.copy()
        del event_dict['time.observation']
        del expected['time.observation']

        event_raw_dict = json.loads(base64_decode(event_dict.pop('raw')))
        expected_raw_dict = json.loads(base64_decode(expected.pop('raw')))
        self.assertDictEqual(event_raw_dict, expected_raw_dict)

        self.assertDictEqual(expected, event_dict)


if __name__ == '__main__':
    unittest.main()
