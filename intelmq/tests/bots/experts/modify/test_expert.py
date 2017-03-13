# -*- coding: utf-8 -*-
"""
Testing modify expert bot.
"""

import unittest

from pkg_resources import resource_filename

import intelmq.lib.test as test
from intelmq.lib.utils import load_configuration
from intelmq.bots.experts.modify.expert import ModifyExpertBot, convert_config

EVENT_TEMPL = {"__type": "Event",
               "feed.name": "Spamhaus Cert",
               "feed.url": "https://portal.spamhaus.org/cert/api.php?cert="
                           "<CERTNAME>&key=<APIKEY>",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-01T00:00:00+00:00",
               }
INPUT = [{'malware.name': 'confickerab'},
         {'malware.name': 'gozi2'},
         {'feed.name': 'Abuse.ch',
          'feed.url': 'https://feodotracker.abuse.ch/blocklist/?download=domainblocklist'},
         {'malware.name': 'zeus_gameover_us'},
         {'malware.name': 'sality-p2p'},
         {'malware.name': 'foobar', 'feed.name': 'Other Feed'},
         {'source.port': 80, 'malware.name': 'zeus'},
         ]
OUTPUT = [{'classification.identifier': 'conficker'},
          {'classification.identifier': 'gozi'},
          {'classification.identifier': 'feodo'},
          {'classification.identifier': 'zeus'},
          {'classification.identifier': 'sality'},
          {},
          {'protocol.application': 'http', 'classification.identifier': 'zeus'},
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

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT
        self.run_bot(iterations=len(INPUT))

        for position, event_out in enumerate(OUTPUT):
            self.assertMessageEqual(position, event_out)

    def test_conversion(self):
        """ Test if the conversion from old dict-based config to new list based is correct. """
        old_path = resource_filename('intelmq',
                                     'tests/bots/experts/modify/old_format.conf')
        old_config = load_configuration(old_path)
        new_path = resource_filename('intelmq',
                                     'tests/bots/experts/modify/new_format.conf')
        new_config = load_configuration(new_path)
        self.assertDictEqual(convert_config(old_config)[0],
                             new_config[0])

EVENT_TEMPL2 = {"__type": "Event",
               "feed.name": "Testing IntelMQ Mock Feed",
               "feed.url": "https://intelmq.org/does-not-exist",
               "classification.type": "botnet drone",
               "time.observation": "2015-01-02T01:20:00+00:00",
               }

INPUT2 = [
    {'malware.name': 'bitdefender-foreign'},
    {'malware.name': 'bitdefender-pykspa_improved'},
    {'malware.name': 'bitdefender-sumxa'},
    {'malware.name': 'downloaderbot-mxb'},
    {'malware.name': 'downloaderbot-2'},
    {'malware.name': 'dridex-data'},
    {'malware.name': 'gameover-zeus-dga'},
    {'malware.name': 'gameover-zeus-peer'},
    {'malware.name': 'gozi2'},
    {'malware.name': 'sality_virus'},
    {'malware.name': 'salityv3'},
    {'malware.name': 'tinba-dga'},
    {'malware.name': 'urlzone'},
    {'malware.name': 'urlzone2'},
    {'malware.name': 'citadel-b54'},
    {'malware.name': 'caphaw'},
    {'malware.name': 'b68-zeroaccess-3-abbit'},
    {'malware.name': 'downadup'},
    {'malware.name': 'sality'},
    {'malware.name': 'sality2'},
    {'malware.name': 'xcodeghost'},
    {'malware.name': 'citadel certpl'},
    {'malware.name': 'dridex-data'},
    {'malware.name': 'bitdefender-nivdort'},
    {'malware.name': 'securityscorecard-someexample-value'},
    {'malware.name': 'anyvalue'},
         ]
OUTPUT2 = [
    {'protocol.transport': 'tcp', 'classification.identifier': 'trojan.generic'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'pykspa'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'dridex'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'downloader-bot'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'downloader-bot'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'dridex'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'gameover zeus dga'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'gameover zeus p2p'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'gozi'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'sality'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'sality'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'tinba'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'urlzone/bebloh'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'urlzone/bebloh'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'citadel'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'caphaw/shylock'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'zeroaccess'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'conficker'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'sality'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'sality'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'xcodeghost'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'citadel'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'dridex'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'nivdort'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'someexample-value'},
    {'protocol.transport': 'tcp', 'classification.identifier': 'anyvalue'},
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

    def test_bot_name(self):
        "Do **not** test that our second test has the same name as the bot."

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = INPUT2
        self.run_bot(iterations=len(INPUT2))

        for position, event_out in enumerate(OUTPUT2):
            self.assertMessageEqual(position, event_out)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
