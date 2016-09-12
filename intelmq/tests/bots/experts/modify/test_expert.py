# -*- coding: utf-8 -*-
"""
Testing modify expert bot.
"""

import unittest

from pkg_resources import resource_filename

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
         {'feed.name': 'Abuse.ch',
          'feed.url': 'https://feodotracker.abuse.ch/blocklist/?download=domainblocklist'},
         {'malware.name': 'zeus_gameover_us'},
         {'malware.name': 'foobar', 'feed.name': 'Other Feed'},
         {'feed.name': '', 'source.port': 80},
         ]
OUTPUT = [{'classification.identifier': 'conficker'},
          {'classification.identifier': 'gozi'},
          {'classification.identifier': 'feodo'},
          {'classification.identifier': 'zeus'},
          {},
          {'protocol.application': 'http'},
          ]
for index in range(len(INPUT)):
    copy1 = EVENT_TEMPL.copy()
    copy2 = EVENT_TEMPL.copy()
    copy1.update(INPUT[index])
    copy2.update(INPUT[index])
    copy2.update(OUTPUT[index])
    INPUT[index] = copy1
    OUTPUT[index] = copy2


class TestModifyExpertBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for ModifyExpertBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ModifyExpertBot
        config_path = resource_filename('intelmq',
                                        'bots/experts/modify/examples/default.conf')
        cls.sysconfig = {'configuration_path': config_path
                         }
        cls.default_input_message = {'__type': 'Event'}

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT
        self.run_bot(iterations=len(INPUT))

        for position, event_out in enumerate(OUTPUT):
            self.assertMessageEqual(position, event_out)

EVENT_TEMPL2 = {"__type": "Event",
               "feed.name": "Testing IntelMQ Mock Feed",
               "feed.url": "https://intelmq.org/does-not-exist",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-02T01:20:00+00:00",
               "raw": "",
               }

INPUT2 = [
    {'malware.name': 'Citadel certpl'},
    {'malware.name': 'dridex-data'},
    {'malware.name': 'bitdefender-nivdort'},
    {'malware.name': 'securityscorecard-someexample-value'},
         ]
OUTPUT2 = [
    {'classification.identifier': 'citadel'},
    {'classification.identifier': 'dridex'},
    { 'malware.name': 'nivdort'},
    { 'malware.name': 'someexample-value'},
          ]
for index in range(len(INPUT2)):
    copy1 = EVENT_TEMPL2.copy()
    copy2 = EVENT_TEMPL2.copy()
    copy1.update(INPUT2[index])
    copy2.update(INPUT2[index])
    copy2.update(OUTPUT2[index])
    INPUT2[index] = copy1
    OUTPUT2[index] = copy2

class TestMoreFeedsModifyExpertBot(test.BotTestCase, unittest.TestCase):
    """Testing ModifyExpertBot for 'morefeeds' configuration.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ModifyExpertBot
        config_path = resource_filename('intelmq',
                                        'bots/experts/modify/examples/morefeeds.conf')
        cls.sysconfig = {'configuration_path': config_path
                         }
        cls.default_input_message = {'__type': 'Event'}


    def test_bot_name(self):
        "Do **not** test that our second test has the same name as the bot."
        pass


    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT2
        self.run_bot(iterations=len(INPUT2))

        for position, event_out in enumerate(OUTPUT2):
            self.assertMessageEqual(position, event_out)


if __name__ == '__main__':
    unittest.main()
