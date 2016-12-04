# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.malc0de.parser import Malc0deParserBot

with open(os.path.join(os.path.dirname(__file__), 'BOOT')) as handle:
    BOOT_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'ZONE')) as handle:
    ZONE_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'IP_Blacklist.txt')) as handle:
    IP_BLACKLIST_FILE = handle.read()

BOOT_REPORT = {'feed.name': 'Windows Format',
               'feed.url': 'http://malc0de.com/bl/BOOT',
               '__type': 'Report',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'raw': utils.base64_encode(BOOT_FILE)
              }

BOOT_EVENT = [{'feed.name': 'Windows Format',
               'feed.url': 'http://malc0de.com/bl/BOOT',
               '__type': 'Event',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'time.source': '2016-11-10T00:00:00+00:00',
               'raw': 'UFJJTUFSWSBleGFtcGxlLmNvbSBibG9ja2VkZG9tYWluLmhvc3Rz',
               'source.fqdn': 'example.com',
               'event_description.url': 'http://malc0de.com/database/index.php?search=example.com',
               'classification.type': 'malware'
              },
              {'feed.name': 'Windows Format',
               'feed.url': 'http://malc0de.com/bl/BOOT',
               '__type': 'Event',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'time.source': '2016-11-10T00:00:00+00:00',
               'raw': 'UFJJTUFSWSBleGFtcGxlLm9yZyBibG9ja2VkZG9tYWluLmhvc3Rz',
               'source.fqdn': 'example.org',
               'event_description.url': 'http://malc0de.com/database/index.php?search=example.org',
               'classification.type': 'malware'
              }]

ZONE_REPORT = {'feed.name': 'Bind Format',
               'feed.url': 'http://malc0de.com/bl/ZONES',
               '__type': 'Report',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'raw': utils.base64_encode(ZONE_FILE)
              }

ZONE_EVENT = [{'feed.name': 'Bind Format',
               'feed.url': 'http://malc0de.com/bl/ZONES',
               '__type': 'Event',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'time.source': '2016-11-10T00:00:00+00:00',
               'raw': 'em9uZSAiZXhhbXBsZS5jb20iICB7dHlwZSBtYXN0ZXI7IGZpbGUgIi9ldGMvbmFtZWRiL2Jsb2NrZWRkb21haW4uaG9zdHMiO307',
               'source.fqdn': 'example.com',
               'event_description.url': 'http://malc0de.com/database/index.php?search=example.com',
               'classification.type': 'malware'
              },
              {'feed.name': 'Bind Format',
               'feed.url': 'http://malc0de.com/bl/ZONES',
               '__type': 'Event',
               'time.observation': '2016-12-4T14:16:25+00:00',
               'time.source': '2016-11-10T00:00:00+00:00',
               'raw': 'em9uZSAiZXhhbXBsZS5vcmciICB7dHlwZSBtYXN0ZXI7IGZpbGUgIi9ldGMvbmFtZWRiL2Jsb2NrZWRkb21haW4uaG9zdHMiO307',
               'source.fqdn': 'example.org',
               'event_description.url': 'http://malc0de.com/database/index.php?search=example.org',
               'classification.type': 'malware'
              }]

IP_BLACKLIST_REPORT = {'feed.name': 'IP Blacklist',
                       'feed.url': 'http://malc0de.com/bl/IP_Blacklist.txt',
                       '__type': 'Report',
                       'time.observation': '2016-12-4T14:16:25+00:00',
                       'raw': utils.base64_encode(IP_BLACKLIST_FILE)
                      }

IP_BLACKLIST_EVENT = [{'feed.name': 'IP Blacklist',
                       'feed.url': 'http://malc0de.com/bl/IP_Blacklist.txt',
                       '__type': 'Event',
                       'time.observation': '2016-12-4T14:16:25+00:00',
                       'time.source': '2016-11-10T00:00:00+00:00',
                       'raw': 'MTkyLjg4Ljk5LjQ=',
                       'source.ip': '192.88.99.4',
                       'event_description.url': 'http://malc0de.com/database/index.php?search=192.88.99.4',
                       'classification.type': 'malware'
                      },
                      {'feed.name': 'IP Blacklist',
                       'feed.url': 'http://malc0de.com/bl/IP_Blacklist.txt',
                       '__type': 'Event',
                       'time.observation': '2016-12-4T14:16:25+00:00',
                       'time.source': '2016-11-10T00:00:00+00:00',
                       'raw': 'MTkyLjAuMC41',
                       'source.ip': '192.0.0.5',
                       'event_description.url': 'http://malc0de.com/database/index.php?search=192.0.0.5',
                       'classification.type': 'malware'
                      }]


class TestMalc0deParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase of Malc0de with Windows, Bind, and IP Address Feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = Malc0deParserBot
        cls.default_input_message = BOOT_REPORT

    def test_boot(self):
        """ Test if correct BOOT event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, BOOT_EVENT[0])
        self.assertMessageEqual(1, BOOT_EVENT[1])

    def test_zone(self):
        """ Test if correct ZONE event has been produced. """
        self.input_message = ZONE_REPORT
        self.run_bot()
        self.assertMessageEqual(0, ZONE_EVENT[0])
        self.assertMessageEqual(1, ZONE_EVENT[1])

    def test_ip_blacklist(self):
        """" Test if correct IP event has been produced. """
        self.input_message = IP_BLACKLIST_REPORT
        self.run_bot()
        self.assertMessageEqual(0, IP_BLACKLIST_EVENT[0])
        self.assertMessageEqual(1, IP_BLACKLIST_EVENT[1])

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
