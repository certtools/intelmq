# -*- coding: utf-8 -*-
"""
Data is from the HIBP Documentation
"""
import json
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.hibp.parser_callback import HIBPCallbackParserBot

REQUEST = {
    "Email": "test@example.com",
    "Domain": "example.com",
    "DomainEmails": ["test@example.com", "test2@example.com"],
    "Breach": [
        {
            "Name": "Adobe",
            "Title": "Adobe",
            "Domain": "adobe.com",
            "BreachDate": "2013-10-04",
            "AddedDate": "2013-12-04T00:00Z",
            "ModifiedDate": "2013-12-04T00:00Z",
            "PwnCount": 152445165,
            "Description": "In October 2013, 153 million Adobe accounts were breached with each containing an internal ID, username, email, <em>encrypted</em> password and a password hint in plain text. The password cryptography was poorly done and <a href=\"http://stricture-group.com/files/adobe-top100.txt\" target=\"_blank\" rel=\"noopener\">many were quickly resolved back to plain text</a>. The unencrypted hints also <a href=\"http://www.troyhunt.com/2013/11/adobe-credentials-and-serious.html\" target=\"_blank\" rel=\"noopener\">disclosed much about the passwords</a> adding further to the risk that hundreds of millions of Adobe customers already faced.",
            "DataClasses": ["Email addresses", "Password hints", "Passwords", "Usernames"],
            "IsVerified":True,
            "IsSensitive":False,
            "IsRetired":False,
            "IsSpamList":False
        },
        {
            "Name": "BattlefieldHeroes",
            "Title": "Battlefield Heroes",
            "Domain": "battlefieldheroes.com",
            "BreachDate": "2011-06-26",
            "AddedDate": "2014-01-23T13:10Z",
            "ModifiedDate": "2014-01-23T13:10Z",
            "PwnCount": 530270,
            "Description": "In June 2011 as part of a final breached data dump, the hacker collective &quot;LulzSec&quot; <a href=\"http://www.rockpapershotgun.com/2011/06/26/lulzsec-over-release-battlefield-heroes-data\" target=\"_blank\" rel=\"noopener\">obtained and released over half a million usernames and passwords from the game Battlefield Heroes</a>. The passwords were stored as MD5 hashes with no salt and many were easily converted back to their plain text versions.",
            "DataClasses": ["Passwords", "Usernames"],
            "IsVerified":True,
            "IsSensitive":False,
            "IsRetired":False,
            "IsSpamList":False
        }
    ],
    "Paste": [
        {
            "Source": "Pastebin",
            "Id": "8Q0BvKD8",
            "Title": "syslog",
            "Date": "2014-03-04T19:14:54Z",
            "EmailCount": 139
        },
        {
            "Source": "Pastie",
            "Id": "7152479",
            "Date": "2013-03-28T16:51:10Z",
            "EmailCount": 30
        }
    ]
}
RAW = utils.base64_encode(json.dumps(REQUEST))


REPORT = {"feed.name": "HIBP Enterprise",
          "time.observation": "2019-03-01T01:01:01+00:00",
          "__type": "Report",
          "raw": RAW
          }

EVENT = {"feed.name": "HIBP Enterprise",
         "raw": RAW,
         "time.observation": "2019-03-01T01:01:01+00:00",
         "extra.domain_emails": REQUEST["DomainEmails"],
         "extra.breach": REQUEST["Breach"],
         "extra.paste": REQUEST["Paste"],
         "classification.taxonomy": "information content security",
         "classification.type": "leak",
         "source.account": "test@example.com",
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
        cls.default_input_message = REPORT

    def test_feodo_event(self):
        """ Test Feodotracker IPs. """
        self.run_bot()
        self.assertMessageEqual(0, EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
