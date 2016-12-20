# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.dyn.parser import DynParserBot
from intelmq.lib import utils

with open(os.path.join(os.path.dirname(__file__), 'ponmocup-infected-domains-CIF-latest.txt')) as handle:
    EXAMPLE_FILE = handle.read()


EXAMPLE_REPORT = {"feed.url": "http://security-research.dyndns.org/pub/botnet/ponmocup/ponmocup-finder/ponmocup-infected-domains-CIF-latest.txt",
                  "feed.name": "DynDNS ponmocup Domains",
                  "__type": "Report",
                  "raw": utils.base64_encode(EXAMPLE_FILE),
                  "time.observation": "2015-11-02T13:11:43+00:00"
                  }

EXAMPLE_EVENTS = [{"feed.url": "http://security-research.dyndns.org/pub/botnet/ponmocup/ponmocup-finder/ponmocup-infected-domains-CIF-latest.txt",
                   "feed.name": "DynDNS ponmocup Domains",
                   "source.fqdn": "25308.example.com",
                   "source.url": "http://25308.example.com/url",
                   "raw": "LyAyNTMwOC5leGFtcGxlLmNvbSBodHRwOi8vMjUzMDguZXhhbXBsZS5jb20vdXJsIG1hbGljaW91cy5leGFtcGxlLm5ldA==",
                   "time.observation": "2015-11-02T13:11:44+00:00",
                   "time.source": "2016-03-15T07:47:49+00:00",
                   "classification.type": "malware",
                   "destination.fqdn": "malicious.example.net",
                   "event_description.text": "has malicious code redirecting to malicious host",
                   "__type": "Event"
                  },
                  {"feed.url": "http://security-research.dyndns.org/pub/botnet/ponmocup/ponmocup-finder/ponmocup-infected-domains-CIF-latest.txt",
                   "feed.name": "DynDNS ponmocup Domains",
                   "destination.fqdn": "25308.example.com",
                   "destination.url": "http://25308.example.com/url",
                   "raw": "LyAyNTMwOC5leGFtcGxlLmNvbSBodHRwOi8vMjUzMDguZXhhbXBsZS5jb20vdXJsIG1hbGljaW91cy5leGFtcGxlLm5ldA==",
                   "time.observation": "2015-11-02T13:11:44+00:00",
                   "time.source": "2016-03-15T07:47:49+00:00",
                   "classification.type": "compromised",
                   "source.fqdn": "malicious.example.net",
                   "event_description.text": "host has been compromised and has malicious code infecting users",
                   "__type": "Event"
                  },
                  {"feed.url": "http://security-research.dyndns.org/pub/botnet/ponmocup/ponmocup-finder/ponmocup-infected-domains-CIF-latest.txt",
                   "feed.name": "DynDNS ponmocup Domains",
                   "source.fqdn": "36015.example.com",
                   "source.url": "http://36015.example.com/url",
                   "raw": "LyAzNjAxNS5leGFtcGxlLmNvbSBodHRwOi8vMzYwMTUuZXhhbXBsZS5jb20vdXJsIG1hbGljaW91czIuZXhhbXBsZS5uZXQ=",
                   "time.observation": "2015-11-02T13:11:44+00:00",
                   "time.source": "2016-03-15T07:47:49+00:00",
                   "classification.type": "malware",
                   "destination.fqdn": "malicious2.example.net",
                   "event_description.text": "has malicious code redirecting to malicious host",
                   "__type": "Event"
                  },

                  {"feed.url": "http://security-research.dyndns.org/pub/botnet/ponmocup/ponmocup-finder/ponmocup-infected-domains-CIF-latest.txt",
                   "feed.name": "DynDNS ponmocup Domains",
                   "destination.fqdn": "36015.example.com",
                   "destination.url": "http://36015.example.com/url",
                   "raw": "LyAzNjAxNS5leGFtcGxlLmNvbSBodHRwOi8vMzYwMTUuZXhhbXBsZS5jb20vdXJsIG1hbGljaW91czIuZXhhbXBsZS5uZXQ=",
                   "time.observation": "2015-11-02T13:11:44+00:00",
                   "time.source": "2016-03-15T07:47:49+00:00",
                   "classification.type": "compromised",
                   "source.fqdn": "malicious2.example.net",
                   "event_description.text": "host has been compromised and has malicious code infecting users",
                   "__type": "Event"
                  },
                  ]


class TestDynParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for DynParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DynParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENTS[0])
        self.assertMessageEqual(1, EXAMPLE_EVENTS[1])
        self.assertMessageEqual(2, EXAMPLE_EVENTS[2])
        self.assertMessageEqual(3, EXAMPLE_EVENTS[3])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
