# -*- coding: utf-8 -*-
"""
Testing modify expert bot.
"""
from __future__ import unicode_literals

import unittest

import intelmq.lib.test as test
from intelmq.bots.experts.modify.expert import ModifyExpertBot

EVENT_TEMPL = {"__type": "Event",
               "feed.name": "Spamhaus Cert",
               "feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                           "<CERTNAME>&key=<APIKEY>",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-01T00:00:00+00:00",
               "raw": "",
               }
INPUT = [{'malware.name': 'confickerab'},
         {'malware.name': 'gozi2'},
         {'malware.name': 'feodo'},
         ]
OUTPUT = [{'classification.identifier': 'conficker'},
          {'classification.identifier': 'gozi'},
          {'classification.identifier': 'feodo'},
          ]
for event_in, event_out in zip(INPUT, OUTPUT):
    event_in.update(EVENT_TEMPL)
    event_out.update(event_in)
    event_out.update(EVENT_TEMPL)


class TestModifyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ModifyExpertBot.
    """

    @classmethod
    def set_bot(self):
        self.bot_reference = ModifyExpertBot
        self.sysconfig = {'filter': False,
                          'overwrite_cc': False,
                          'verify_cert': False,
                          }

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT
        self.run_bot(iterations=len(INPUT))

        for position, event_out in enumerate(OUTPUT):
            self.assertMessageEqual(position, event_out)


if __name__ == '__main__':
    unittest.main()
