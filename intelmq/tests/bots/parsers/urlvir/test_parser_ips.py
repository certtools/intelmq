# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.urlvir.parser_ips import URLVirIPsParserBot

EXAMPLE_REPORT = {"feed.name": "URLVir",
                  "feed.url": "http://www.urlvir.com/export-ip-addresses/",
                  "raw": "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj"
                         "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCiNVUkxWaXIgQWN0"
                         "aXZlIE1hbGljaW91cyBJUCBBZGRyZXNzZXMgSG9zdGluZyBNYWx3"
                         "YXJlCiNVcGRhdGVkIG9uIEF1Z3VzdCAxNywgMjAxNSwgMTA6MTYg"
                         "YW0KI0ZyZWUgZm9yIG5vbmNvbW1lcmNpYWwgdXNlIG9ubHksIGNv"
                         "bnRhY3QgdXMgZm9yIG1vcmUgaW5mb3JtYXRpb24KIyMjIyMjIyMj"
                         "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj"
                         "IyMjIyMjIyMjIyMjIyMjIyMjCjE5Mi4wLjIuMQoxOTIuMC4yLjIK"
                         "MTkyLjAuMi4zCjE5Mi4wLjIuNA==",
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "URLVir",
                 "feed.url": "http://www.urlvir.com/export-ip-addresses/",
                 "source.ip": "192.0.2.1",
                 "classification.type": "malware",
                 "__type": "Event",
                 "raw": "MTkyLjAuMi4x",
                 "time.observation": "2015-01-01T00:00:00+00:00",
                 }


class TestURLVirIPsParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for URLVirIPsParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLVirIPsParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
