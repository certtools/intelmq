# SPDX-FileCopyrightText: 2021 CysihZ
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.fireeye.parser import FireeyeParserBot


with open(os.path.join(os.path.dirname(__file__), 'event.txt')) as handle:
    FILE = handle.read()

EXAMPLE_REPORT = {"feed.url": "https://myfireeye.local",
                  'raw': utils.base64_encode(FILE),
                  "__type": "Report",
                  "feed.name": "Fireeye SB",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EVENT_TEMPL = {"feed.url": "https://myfireeye.local",
               "feed.name": "Fireeye SB",
               "__type": "Event",
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
EXAMPLE_EVENTS_PARTS = [{'classification.type': 'malware',
                         'feed.name': 'Fireeye SB',
                         'feed.url': 'https://myfireeye.local',
                         'malware.hash.md5': '21232f297a57a5a743894a0e4a801fc3',
                         'malware.hash.sha256': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                         },
                        {'destination.fqdn': 'shop.domain1.com',
                         'classification.type': 'malware-distribution',
                         'destination.port': 80,
                         'destination.url': 'http://shop.domain1.com/wp-content/n/',
                         'destination.urlpath': '/wp-content/n/',
                         'feed.name': 'Fireeye SB',
                         'feed.url': 'https://myfireeye.local',
                         'malware.hash.md5': '21232f297a57a5a743894a0e4a801fc3',
                         'malware.hash.sha256': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                         'time.observation': '2015-01-01T00:00:00+00:00',
                         },
                        ]


@test.skip_exotic()
class TestFireeyeParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for FireeyeParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FireeyeParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.run_bot()
        for position, event in enumerate(EXAMPLE_EVENTS_PARTS):
            event_ = EVENT_TEMPL.copy()
            event_.update(event)
            event_['raw'] = utils.base64_encode(FILE)
            self.assertMessageEqual(position, event_)
        self.assertOutputQFILE_LINES = FILE.splitlines()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
