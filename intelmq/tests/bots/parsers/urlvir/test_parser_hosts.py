# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.urlvir.parser_hosts import URLVirHostsParserBot


EXAMPLE_REPORT = {"feed.url": "http://www.urlvir.com/export-hosts/",
                  "raw": "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj"
                         "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiNVUkxWaXIgQWN0"
                         "aXZlIE1hbGljaW91cyBIb3N0cwojVXBkYXRlZCBvbiBBdWd1c3Qg"
                         "MTcsIDIwMTUsIDExOjI5IGFtCiNGcmVlIGZvciBub25jb21tZXJj"
                         "aWFsIHVzZSBvbmx5LCBjb250YWN0IHVzIGZvciBtb3JlIGluZm9y"
                         "bWF0aW9uCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj"
                         "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwpleGFt"
                         "cGxlLm5ldA==",
                  "__type": "Report",
                  "feed.name": "URLVir"}
EXAMPLE_EVENT = {"feed.url": "http://www.urlvir.com/export-hosts/",
                 "feed.name": "URLVir",
                 "__type": "Event",
                 "source.fqdn": "example.net",
                 "classification.type": "malware",
                 "raw": "ZXhhbXBsZS5uZXQ=",
                 }


class TestURLVirHostsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a URLVirHostsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLVirHostsParserBot
        cls.default_input_message = json.dumps(EXAMPLE_REPORT)

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.prepare_bot()
        self.run_bot()
        self.assertEventAlmostEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':
    unittest.main()
