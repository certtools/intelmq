# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.eset.parser import ESETParserBot
from intelmq.lib import utils


RAW_REPORT = """
[{"confidence": "Low", "count": 1337, "domain": "example.com", "downloaded_detection": null, "first_seen": "2018-12-31 23:00:00 UTC", "ip": null, "last_seen": "2020-06-20 09:00:00 UTC", "location": null, "opener_detection": null, "reason": "Host actively distributes high-severity threat in the form of executable code.", "state": "BlockedObject", "valid_to": "2020-07-01 00:00:00 UTC", "_eset_feed": "ei.domains v2 (json)"}]
""".strip()

EXAMPLE_REPORT = {"feed.url": "https://eti.eset.com/taxiiservice/discovery",
                  "feed.name": "ESET ETI",
                  "__type": "Report",
                  "raw": utils.base64_encode(RAW_REPORT),
                  "time.observation": "2020-06-30T14:37:00+00:00"
                  }

EXAMPLE_EVENT = {
    'classification.type': 'malware-distribution',
    'event_description.text': 'Host actively distributes high-severity threat in '
                              'the form of executable code.',
    'feed.name': 'ESET ETI',
    'feed.url': 'https://eti.eset.com/taxiiservice/discovery',
    'raw': 'eyJjb25maWRlbmNlIjogIkxvdyIsICJjb3VudCI6IDEzMzcsICJkb21haW4iOiAiZXhhbXBsZS5jb20iLCAiZG93bmxvYWRlZF9kZXRlY3Rpb24iOiBudWxsLCAiZmlyc3Rfc2VlbiI6ICIyMDE4LTEyLTMxIDIzOjAwOjAwIFVUQyIsICJpcCI6IG51bGwsICJsYXN0X3NlZW4iOiAiMjAyMC0wNi0yMCAwOTowMDowMCBVVEMiLCAibG9jYXRpb24iOiBudWxsLCAib3BlbmVyX2RldGVjdGlvbiI6IG51bGwsICJyZWFzb24iOiAiSG9zdCBhY3RpdmVseSBkaXN0cmlidXRlcyBoaWdoLXNldmVyaXR5IHRocmVhdCBpbiB0aGUgZm9ybSBvZiBleGVjdXRhYmxlIGNvZGUuIiwgInN0YXRlIjogIkJsb2NrZWRPYmplY3QiLCAidmFsaWRfdG8iOiAiMjAyMC0wNy0wMSAwMDowMDowMCBVVEMiLCAiX2VzZXRfZmVlZCI6ICJlaS5kb21haW5zIHYyIChqc29uKSJ9',
    'source.fqdn': 'example.com',
    'time.source': '2020-06-20T09:00:00+00:00',
    "__type": "Event",
    }


class TestESETParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ESETParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ESETParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
