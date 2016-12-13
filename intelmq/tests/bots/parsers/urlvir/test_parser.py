# -*- coding: utf-8 -*-

import os
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils

from intelmq.bots.parsers.urlvir.parser import URLVirParserBot

with open(os.path.join(os.path.dirname(__file__), 'export-hosts.txt')) as handle:
    HOSTS_FILE = handle.read()

with open(os.path.join(os.path.dirname(__file__), 'export-ip-addresses.txt')) as handle:
    IP_ADDRESSES_FILE = handle.read()

HOSTS_REPORT = {'feed.name': 'URLVir Export Hosts',
                'feed.url': 'http://www.urlvir.com/export-hosts/',
                '__type': 'Report',
                'time.observation': '2016-12-04T07:50:15+00:00',
                'raw': utils.base64_encode(HOSTS_FILE)
               }

HOSTS_EVENTS = [{'feed.name': 'URLVir Export Hosts',
                 'feed.url': 'http://www.urlvir.com/export-hosts/',
                 '__type': 'Event',
                 'time.observation': '2016-12-04T07:50:15+00:00',
                 'raw': 'aW5kaXJsaXZleHN0b3JlLmNvbQ==',
                 'time.source': '2016-12-04T12:29:00+00:00',
                 'source.fqdn': 'indirlivexstore.com',
                 'classification.type': 'malware',
                 'event_description.text': 'Active Malicious Hosts',
                 'event_description.url': 'http://www.urlvir.com/search-host/indirlivexstore.com/'
                },
                {'feed.name': 'URLVir Export Hosts',
                 'feed.url': 'http://www.urlvir.com/export-hosts/',
                 '__type': 'Event',
                 'time.observation': '2016-12-04T07:50:15+00:00',
                 'raw': 'MTg4LjEzOC42OC4xNzc=',
                 'time.source': '2016-12-04T12:29:00+00:00',
                 'source.ip': '188.138.68.177',
                 'classification.type': 'malware',
                 'event_description.text': 'Active Malicious Hosts',
                 'event_description.url': 'http://www.urlvir.com/search-ip-address/188.138.68.177/'
                }]

IP_ADDRESSES_REPORT = {'feed.name': 'URLVir Export IP Addresses',
                       'feed.url': 'http://www.urlvir.com/export-ip-addresses/',
                       '__type': 'Report',
                       'time.observation': '2016-12-04T07:50:15+00:00',
                       'raw': utils.base64_encode(IP_ADDRESSES_FILE)
                      }

IP_ADDRESS_EVENTS = {'feed.name': 'URLVir Export IP Addresses',
                     'feed.url': 'http://www.urlvir.com/export-ip-addresses/',
                     '__type': 'Event',
                     'time.observation': '2016-12-04T07:50:15+00:00',
                     'raw': 'MTAzLjYuMjQ2Ljgz',
                     'time.source': '2016-12-04T12:29:00+00:00',
                     'source.ip': '103.6.246.83',
                     'classification.type': 'malware',
                     'event_description.text': 'Active Malicious IP Addresses Hosting Malware',
                     'event_description.url': 'http://www.urlvir.com/search-ip-address/103.6.246.83/'
                    }


class TestURLVirParserBot(test.BotTestCase, unittest.TestCase):
    """ A TestCase of URLVirParserBot with Host and IP Address Feeds. """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = URLVirParserBot
        cls.default_input_message = HOSTS_REPORT

    def test_hosts(self):
        """ Test if correct Host Events have been produced. """
        self.run_bot()
        self.assertMessageEqual(0, HOSTS_EVENTS[0])
        self.assertMessageEqual(1, HOSTS_EVENTS[1])

    def test_ip_addresses(self):
        """ Test if coffect IP Address Events have been produced. """
        self.input_message = IP_ADDRESSES_REPORT
        self.run_bot()
        self.assertMessageEqual(0, IP_ADDRESS_EVENTS)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
