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
    "time.observation": "2016-06-15T09:25:26+00:00",
    "raw": "W3siQXR0cmlidXRlIjogW3siU2hhZG93QXR0cmlidXRlIjogW10sICJTaGFyaW5n"
           "R3JvdXAiOiBbXSwgImNhdGVnb3J5IjogIlBheWxvYWQgZGVsaXZlcnkiLCAiY29t"
           "bWVudCI6ICIiLCAiZGVsZXRlZCI6IGZhbHNlLCAiZGlzdHJpYnV0aW9uIjogIjUi"
           "LCAiZXZlbnRfaWQiOiAiMiIsICJpZCI6ICI3IiwgInNoYXJpbmdfZ3JvdXBfaWQi"
           "OiAiMCIsICJ0aW1lc3RhbXAiOiAiMTQ2NTY4MTMwNCIsICJ0b19pZHMiOiBmYWxz"
           "ZSwgInR5cGUiOiAidXJsIiwgInV1aWQiOiAiNTc1Yzg1OTgtZjFmMC00YzE2LWE5"
           "NGEtMDYxMmMwYTgzODY2IiwgInZhbHVlIjogImh0dHA6Ly9mYWtlLndlYnNpdGUu"
           "Y29tL21hbHdhcmUvaXMvaGVyZSJ9LCB7IlNoYWRvd0F0dHJpYnV0ZSI6IFtdLCAi"
           "U2hhcmluZ0dyb3VwIjogW10sICJjYXRlZ29yeSI6ICJQYXlsb2FkIHR5cGUiLCAi"
           "Y29tbWVudCI6ICIiLCAiZGVsZXRlZCI6IGZhbHNlLCAiZGlzdHJpYnV0aW9uIjog"
           "IjUiLCAiZXZlbnRfaWQiOiAiMiIsICJpZCI6ICI2IiwgInNoYXJpbmdfZ3JvdXBf"
           "aWQiOiAiMCIsICJ0aW1lc3RhbXAiOiAiMTQ2NTY4MTgwMSIsICJ0b19pZHMiOiBm"
           "YWxzZSwgInR5cGUiOiAidGV4dCIsICJ1dWlkIjogIjU3NWM4NTQ5LTkwMTAtNDU1"
           "NS04YjM3LTA1N2FjMGE4Mzg2NiIsICJ2YWx1ZSI6ICJMb2NreSJ9XSwgIk9yZyI6"
           "IHsiaWQiOiAiMSIsICJuYW1lIjogIk9SR05BTUUiLCAidXVpZCI6ICI1NzU4NmU5"
           "YS00YTY0LTRmNzktOTAwOS00ZGMxYzBhODM4NjYifSwgIk9yZ2MiOiB7ImlkIjog"
           "IjEiLCAibmFtZSI6ICJPUkdOQU1FIiwgInV1aWQiOiAiNTc1ODZlOWEtNGE2NC00"
           "Zjc5LTkwMDktNGRjMWMwYTgzODY2In0sICJSZWxhdGVkRXZlbnQiOiBbXSwgIlNo"
           "YWRvd0F0dHJpYnV0ZSI6IFtdLCAiVGFnIjogW3siY29sb3VyIjogIiMwMDVhNWEi"
           "LCAiZXhwb3J0YWJsZSI6IHRydWUsICJpZCI6ICI2IiwgIm5hbWUiOiAiZWNzaXJ0"
           "Om1hbGljaW91cy1jb2RlPVwicmFuc29td2FyZVwiIn0sIHsiY29sb3VyIjogIiMx"
           "NDJiZjciLCAiZXhwb3J0YWJsZSI6IHRydWUsICJpZCI6ICIxIiwgIm5hbWUiOiAi"
           "Zm9yX2ludGVsbXFfcHJvY2Vzc2luZyJ9XSwgImFuYWx5c2lzIjogIjAiLCAiYXR0"
           "cmlidXRlX2NvdW50IjogIjIiLCAiZGF0ZSI6ICIyMDE2LTA2LTA5IiwgImRpc3Ry"
           "aWJ1dGlvbiI6ICIwIiwgImlkIjogIjIiLCAiaW5mbyI6ICJBIFJhbmRvbSBFdmVu"
           "dCIsICJsb2NrZWQiOiBmYWxzZSwgIm9yZ19pZCI6ICIxIiwgIm9yZ2NfaWQiOiAi"
           "MSIsICJwcm9wb3NhbF9lbWFpbF9sb2NrIjogZmFsc2UsICJwdWJsaXNoX3RpbWVz"
           "dGFtcCI6ICIwIiwgInB1Ymxpc2hlZCI6IGZhbHNlLCAic2hhcmluZ19ncm91cF9p"
           "ZCI6ICIwIiwgInRocmVhdF9sZXZlbF9pZCI6ICIxIiwgInRpbWVzdGFtcCI6ICIx"
           "NDY1NjgxODAxIiwgInV1aWQiOiAiNTc1OGViZjUtYzg5OC00OGU2LTlmZTktNTY2"
           "NWMwYTgzODY2In1d",
}

EXAMPLE_EVENT = {
    "__type": "Event",
    "feed.accuracy": 100.0,
    "feed.name": "misp_test",
    "feed.url": "http://192.168.56.102/",
    "time.observation": "2016-06-15T09:25:26+00:00",
    "time.source": "2016-06-11T21:41:44+00:00",
    "source.url": "http://fake.website.com/malware/is/here",
    "event_description.text": "Payload delivery",
    "event_description.url": "http://192.168.56.102/event/view/2",
    "classification.type": "ransomware",
    "malware.name": "locky",
    "raw": "eyJBdHRyaWJ1dGUiOiBbeyJTaGFkb3dBdHRyaWJ1dGUiOiBbXSwgIlNoYXJpbmdH"
           "cm91cCI6IFtdLCAiY2F0ZWdvcnkiOiAiUGF5bG9hZCBkZWxpdmVyeSIsICJjb21t"
           "ZW50IjogIiIsICJkZWxldGVkIjogZmFsc2UsICJkaXN0cmlidXRpb24iOiAiNSIs"
           "ICJldmVudF9pZCI6ICIyIiwgImlkIjogIjciLCAic2hhcmluZ19ncm91cF9pZCI6"
           "ICIwIiwgInRpbWVzdGFtcCI6ICIxNDY1NjgxMzA0IiwgInRvX2lkcyI6IGZhbHNl"
           "LCAidHlwZSI6ICJ1cmwiLCAidXVpZCI6ICI1NzVjODU5OC1mMWYwLTRjMTYtYTk0"
           "YS0wNjEyYzBhODM4NjYiLCAidmFsdWUiOiAiaHR0cDovL2Zha2Uud2Vic2l0ZS5j"
           "b20vbWFsd2FyZS9pcy9oZXJlIn0sIHsiU2hhZG93QXR0cmlidXRlIjogW10sICJT"
           "aGFyaW5nR3JvdXAiOiBbXSwgImNhdGVnb3J5IjogIlBheWxvYWQgdHlwZSIsICJj"
           "b21tZW50IjogIiIsICJkZWxldGVkIjogZmFsc2UsICJkaXN0cmlidXRpb24iOiAi"
           "NSIsICJldmVudF9pZCI6ICIyIiwgImlkIjogIjYiLCAic2hhcmluZ19ncm91cF9p"
           "ZCI6ICIwIiwgInRpbWVzdGFtcCI6ICIxNDY1NjgxODAxIiwgInRvX2lkcyI6IGZh"
           "bHNlLCAidHlwZSI6ICJ0ZXh0IiwgInV1aWQiOiAiNTc1Yzg1NDktOTAxMC00NTU1"
           "LThiMzctMDU3YWMwYTgzODY2IiwgInZhbHVlIjogIkxvY2t5In1dLCAiT3JnIjog"
           "eyJpZCI6ICIxIiwgIm5hbWUiOiAiT1JHTkFNRSIsICJ1dWlkIjogIjU3NTg2ZTlh"
           "LTRhNjQtNGY3OS05MDA5LTRkYzFjMGE4Mzg2NiJ9LCAiT3JnYyI6IHsiaWQiOiAi"
           "MSIsICJuYW1lIjogIk9SR05BTUUiLCAidXVpZCI6ICI1NzU4NmU5YS00YTY0LTRm"
           "NzktOTAwOS00ZGMxYzBhODM4NjYifSwgIlJlbGF0ZWRFdmVudCI6IFtdLCAiU2hh"
           "ZG93QXR0cmlidXRlIjogW10sICJUYWciOiBbeyJjb2xvdXIiOiAiIzAwNWE1YSIs"
           "ICJleHBvcnRhYmxlIjogdHJ1ZSwgImlkIjogIjYiLCAibmFtZSI6ICJlY3NpcnQ6"
           "bWFsaWNpb3VzLWNvZGU9XCJyYW5zb213YXJlXCIifSwgeyJjb2xvdXIiOiAiIzE0"
           "MmJmNyIsICJleHBvcnRhYmxlIjogdHJ1ZSwgImlkIjogIjEiLCAibmFtZSI6ICJm"
           "b3JfaW50ZWxtcV9wcm9jZXNzaW5nIn1dLCAiYW5hbHlzaXMiOiAiMCIsICJhdHRy"
           "aWJ1dGVfY291bnQiOiAiMiIsICJkYXRlIjogIjIwMTYtMDYtMDkiLCAiZGlzdHJp"
           "YnV0aW9uIjogIjAiLCAiaWQiOiAiMiIsICJpbmZvIjogIkEgUmFuZG9tIEV2ZW50"
           "IiwgImxvY2tlZCI6IGZhbHNlLCAib3JnX2lkIjogIjEiLCAib3JnY19pZCI6ICIx"
           "IiwgInByb3Bvc2FsX2VtYWlsX2xvY2siOiBmYWxzZSwgInB1Ymxpc2hfdGltZXN0"
           "YW1wIjogIjAiLCAicHVibGlzaGVkIjogZmFsc2UsICJzaGFyaW5nX2dyb3VwX2lk"
           "IjogIjAiLCAidGhyZWF0X2xldmVsX2lkIjogIjEiLCAidGltZXN0YW1wIjogIjE0"
           "NjU2ODE4MDEiLCAidXVpZCI6ICI1NzU4ZWJmNS1jODk4LTQ4ZTYtOWZlOS01NjY1"
           "YzBhODM4NjYifQ=="
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


if __name__ == '__main__':
    unittest.main()
