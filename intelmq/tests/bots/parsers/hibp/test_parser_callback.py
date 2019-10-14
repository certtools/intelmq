# -*- coding: utf-8 -*-
"""
Data is from the HIBP Documentation
"""
import json
import unittest
import pkg_resources

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.hibp.parser_callback import HIBPCallbackParserBot

BREACHREQUEST = json.load(open(pkg_resources.resource_filename('intelmq', 'tests/bots/parsers/hibp/breach_callbacktest.json')))
BREACHRAW = utils.base64_encode(json.dumps(BREACHREQUEST, sort_keys=True))
BR_REP = {"feed.name": "HIBP Enterprise",
          "time.observation": "2019-03-01T01:01:01+00:00",
          "__type": "Report",
          "raw": BREACHRAW
          }
BR_EV = {"feed.name": "HIBP Enterprise",
         "raw": BREACHRAW,
         "time.observation": "2019-03-01T01:01:01+00:00",
         "extra.domain_emails": BREACHREQUEST["DomainEmails"],
         "extra.breach": BREACHREQUEST["Breach"],
         "classification.taxonomy": "information content security",
         "classification.type": "leak",
         "classification.identifier": "breach",
         "source.account": "test2@example.com",
         "source.fqdn": "example.com",
         "__type": "Event"
         }

PASTEREQUEST = json.load(open(pkg_resources.resource_filename('intelmq', 'tests/bots/parsers/hibp/paste_callbacktest.json')))
PASTERAW = utils.base64_encode(json.dumps(PASTEREQUEST, sort_keys=True))
PA_REP = {"feed.name": "HIBP Enterprise",
          "time.observation": "2019-03-01T01:01:01+00:00",
          "__type": "Report",
          "raw": PASTERAW
          }
PA_EV = {"feed.name": "HIBP Enterprise",
         "raw": PASTERAW,
         "time.observation": "2019-03-01T01:01:01+00:00",
         "extra.domain_emails": PASTEREQUEST["DomainEmails"],
         "extra.paste": PASTEREQUEST["Paste"],
         "classification.taxonomy": "information content security",
         "classification.type": "leak",
         "classification.identifier": "paste",
         "source.account": "test2@example.com",
         "source.fqdn": "example.com",
         "__type": "Event"
         }


BREACHREALREQUEST = json.load(open(pkg_resources.resource_filename('intelmq', 'tests/bots/parsers/hibp/breach_real.json')))
BREACHREALRAW = utils.base64_encode(json.dumps(BREACHREALREQUEST, sort_keys=True))
BR_REAL_REP = {"feed.name": "HIBP Enterprise",
               "time.observation": "2019-03-01T01:01:01+00:00",
               "__type": "Report",
               "raw": BREACHREALRAW
               }
BR_REAL_EV = {"feed.name": "HIBP Enterprise",
              "raw": BREACHREALRAW,
              "time.observation": "2019-03-01T01:01:01+00:00",
              "time.source": "2019-09-30T17:15:11+00:00",
              "extra.domain_emails": BREACHREALREQUEST["DomainEmails"],
              "extra.breach": BREACHREALREQUEST["Breach"],
              "classification.taxonomy": "information content security",
              "classification.type": "leak",
              "classification.identifier": "breach",
              "source.fqdn": "example.com",
              "__type": "Event"
              }


class TestHIBPCallbackParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for HIBPCallbackParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = HIBPCallbackParserBot
        cls.default_input_message = BR_REP

    def test_breach(self):
        """ Test Breach from Callback Tester. """
        self.run_bot()
        self.assertMessageEqual(0, BR_EV)

    def test_paste(self):
        """ Test Paste from Callback Tester. """
        self.input_message = PA_REP
        self.run_bot()
        self.assertMessageEqual(0, PA_EV)

    def test_real_breach(self):
        """ Test Breach for real data. Misses the Email field. """
        self.input_message = BR_REAL_REP
        self.run_bot()
        for i, email in enumerate(("user.name1@example.com",
                                   "user.name2@example.com")):
            event = BR_REAL_EV.copy()
            event['source.account'] = email
            self.assertMessageEqual(i, event)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
