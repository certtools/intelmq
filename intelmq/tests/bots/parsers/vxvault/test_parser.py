# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

import intelmq.lib.test as test
from intelmq.bots.parsers.vxvault.parser import VXVaultParserBot

EXAMPLE_REPORT = {"feed.name": "VxVault",
                  "feed.url": "http://vxvault.siri-urz.net/URL_List.php",
                  "raw": "PHByZT4KVlggVmF1bHQgbGFzdCAxMDAgTGlua3MKTW9uLCAxNyBB"
                         "dWcgMjAxNSAxNDozNjoxOSArMDAwMAoKaHR0cDovL2V4YW1wbGUu"
                         "Y29tL2JhZC9wcm9ncmFtLmV4ZQ==",
                  "__type": "Report",
                  "time.observation": "2015-01-01T00:00:00+00:00",
                  }
EXAMPLE_EVENT = {"feed.name": "VxVault",
                 "feed.url": "http://vxvault.siri-urz.net/URL_List.php",
                 "source.url": "http://example.com/bad/program.exe",
                 "classification.type": "malware-distribution",
                 "__type": "Event",
                 "raw": "aHR0cDovL2V4YW1wbGUuY29tL2JhZC9wcm9ncmFtLmV4ZQ==",
                 "source.fqdn": "example.com",
                 "time.source": "2015-08-17T14:36:19+00:00",
                 }


class TestVXVaultParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for VXVaultParserBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = VXVaultParserBot
        cls.default_input_message = EXAMPLE_REPORT

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_EVENT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
