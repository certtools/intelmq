"""
© 2021 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0-or-later

This unittest can test the bot against a read tuency instance as well as using requests mock.
The latter is the default while the first is only in use if a tunency instance URL and authentication token is given a environment variable.
"""
import os
import unittest

from intelmq.lib.test import BotTestCase
from intelmq.bots.experts.tuency.expert import TuencyExpertBot

import requests_mock


INPUT = {'__type': 'Event',
         'classification.taxonomy': 'availability',
         'classification.type': 'system-compromise',
         'feed.provider': 'Some Provider',
         'feed.name': 'FTP',
         'source.ip': '123.123.123.23',
         'source.fqdn': 'www.example.at'
         }
INPUT_IP = INPUT.copy()
del INPUT_IP['source.fqdn']
INPUT_IP['source.abuse_contact'] = 'abuse@example.com'
INPUT_DOMAIN = INPUT.copy()
del INPUT_DOMAIN['source.ip']
OUTPUT = INPUT.copy()
OUTPUT_IP = INPUT_IP.copy()
OUTPUT_IP['extra.notify'] = False
OUTPUT_IP['source.abuse_contact'] = 'test@ntvtn.de'
OUTPUT_IP_NO_OVERWRITE = OUTPUT_IP.copy()
OUTPUT_IP_NO_OVERWRITE['source.abuse_contact'] = 'abuse@example.com'
OUTPUT_DOMAIN = INPUT_DOMAIN.copy()
OUTPUT_DOMAIN['extra.ttl'] = 24*60*60  # 1 day
OUTPUT_DOMAIN['source.abuse_contact'] = 'abuse+www@example.at'
OUTPUT_BOTH = OUTPUT.copy()
OUTPUT_BOTH['extra.ttl'] = 24*60*60  # 1 day
OUTPUT_BOTH['source.abuse_contact'] = 'test@ntvtn.de,abuse+www@example.at'
EMPTY = {'__type': 'Event', 'comment': 'foobar'}
UNKNOWN_IP = INPUT_IP.copy()
UNKNOWN_IP['source.ip'] = '10.0.0.1'


PREFIX = 'http://localhost/intelmq/lookup?classification_taxonomy=availability&classification_type=system-compromise&feed_provider=Some+Provider&feed_name=FTP&feed_status=production'


def prepare_mocker(mocker):
    # IP address
    mocker.get(f'{PREFIX}&ip=123.123.123.23',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@ntvtn.de"}]}]},"suppress":True,"interval":{"unit":"days","length":1}})
    # Domain:
    mocker.get(f'{PREFIX}&domain=www.example.at',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"domain":{"destinations":[{"source":"portal","name":"EineOrganisation","contacts":[{"email":"abuse+www@example.at"}]}]},"suppress":False,"interval":{"unit":"days","length":1}})
    # Both
    mocker.get(f'{PREFIX}&ip=123.123.123.23&domain=www.example.at',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@ntvtn.de"}]}]},"domain":{"destinations":[{"source":"portal","name":"EineOrganisation","contacts":[{"email":"abuse+www@example.at"}]}]},"suppress":False,"interval":{"unit":"day","length":1}})

    # Unknown IP address
    mocker.get(f'{PREFIX}&ip=10.0.0.1',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={'ip': {'destinations': [], 'netobject': None}})


@requests_mock.Mocker()
class TestTuencyExpertBot(BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = TuencyExpertBot
        if not os.environ.get("INTELMQ_TEST_TUNECY_URL") or not os.environ.get("INTELMQ_TEST_TUNECY_TOKEN"):
            cls.mock = True
            cls.sysconfig = {"url": 'http://localhost/',
                             "authentication_token": 'Lorem ipsum',
                             }
        else:
            cls.mock = False
            cls.sysconfig = {"url": os.environ["INTELMQ_TEST_TUNECY_URL"],
                             "authentication_token": os.environ["INTELMQ_TEST_TUNECY_TOKEN"],
                             }
        cls.default_input_message = INPUT

    def test_both(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_BOTH)

    def test_ip(self, mocker):
        """
        Using an IP address as input. Existing source.abuse_contact should be overwritten.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_IP
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_IP)

    def test_ip_no_overwrite(self, mocker):
        """
        Using an IP address as input. Existing source.abuse_contact should not be overwritten.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_IP
        self.run_bot(parameters={'overwrite': False})
        self.assertMessageEqual(0, OUTPUT_IP_NO_OVERWRITE)

    def test_domain(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_DOMAIN
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_DOMAIN)

    def test_empty(self, mocker):
        """
        A message with neither an IP address nor a domain, should be ignored and just passed on.
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = EMPTY
        self.run_bot()
        self.assertMessageEqual(0, EMPTY)

    def test_no_result(self, mocker):
        """
        This IP address is not in the database
        """
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = UNKNOWN_IP
        self.run_bot()
        self.assertMessageEqual(0, UNKNOWN_IP)
