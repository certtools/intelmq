# -*- coding: utf-8 -*-

import json
import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.eset.parser import ESETParserBot
from intelmq.lib import utils

RAW_REPORT = """
[{"confidence": "Low", "count": 1337, "domain": "example.com", "downloaded_detection": null, "first_seen": "2018-12-31 23:00:00 UTC", "ip": null, "last_seen": "2020-06-20 09:00:00 UTC", "location": null, "opener_detection": null, "reason": "Host actively distributes high-severity threat in the form of executable code.", "state": "BlockedObject", "valid_to": "2020-07-01 00:00:00 UTC"}]
""".strip()
NXDOMAIN_RAW = """
[{"confidence": "Low", "count": 1337, "domain": "example.com", "downloaded_detection": null, "first_seen": "2018-12-31 23:00:00 UTC", "ip": "@ipv4_NXDOMAIN", "last_seen": "2020-06-20 09:00:00 UTC", "location": null, "opener_detection": null, "reason": "Host actively distributes high-severity threat in the form of executable code.", "state": "BlockedObject", "valid_to": "2020-07-01 00:00:00 UTC"}]
""".strip()

EXAMPLE_REPORT = {"feed.url": "https://eti.eset.com/taxiiservice/discovery",
                  "feed.name": "ESET ETI",
                  "__type": "Report",
                  "raw": utils.base64_encode(RAW_REPORT),
                  "time.observation": "2020-06-30T14:37:00+00:00",
                  "extra.eset_feed": "ei.domains v2 (json)",
                  }
NXDOMAIN_REPORT = {"feed.url": "https://eti.eset.com/taxiiservice/discovery",
                   "feed.name": "ESET ETI",
                   "__type": "Report",
                   "raw": utils.base64_encode(NXDOMAIN_RAW),
                   "time.observation": "2020-06-30T14:37:00+00:00",
                   "extra.eset_feed": "ei.domains v2 (json)",
                   }

EXAMPLE_EVENT = {
    'classification.type': 'malware-distribution',
    'event_description.text': 'Host actively distributes high-severity threat in '
                              'the form of executable code.',
    'feed.name': 'ESET ETI',
    'feed.url': 'https://eti.eset.com/taxiiservice/discovery',
    'raw': utils.base64_encode(json.dumps(json.loads(RAW_REPORT)[0], sort_keys=True)),
    'source.fqdn': 'example.com',
    'time.source': '2020-06-20T09:00:00+00:00',
    "extra.eset_feed": "ei.domains v2 (json)",
    "__type": "Event",
    }
NXDOMAIN_EVENT = EXAMPLE_EVENT.copy()
NXDOMAIN_EVENT['raw'] = utils.base64_encode(json.dumps(json.loads(NXDOMAIN_RAW)[0], sort_keys=True))


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

    def test_nxdomain(self):
        """ Test if correct Event has been produced. """
        self.input_message = NXDOMAIN_REPORT
        self.run_bot()
        self.assertMessageEqual(0, NXDOMAIN_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
