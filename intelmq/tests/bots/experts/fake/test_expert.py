# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
from json import loads as json_loads
from ipaddress import ip_network, ip_address

import pkg_resources

import intelmq.lib.test as test
from intelmq.bots.experts.fake.expert import FakeExpertBot

FAKE_DB = pkg_resources.resource_filename('intelmq', 'tests/bots/experts/fake/data.json')
EXAMPLE_INPUT = {"__type": "Event",
                 "source.ip": "93.184.216.34",  # example.com
                 }
NETWOK_EXISTS = {"__type": "Event",
                 "source.network": "93.184.216.0/24",
                 }

class TestFakeExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FakeExpertBot
        cls.sysconfig = {'database': FAKE_DB}

    def test_nochange(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_INPUT)

    def test_overwrite(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot(parameters={'overwrite': True})
        msg = json_loads(self.get_output_queue()[0])
        self.assertIn(ip_address(msg['source.ip']), ip_network("10.0.0.0/8"))
        self.assertEqual(msg['source.network'], "10.0.0.0/8")

    def test_network_exists(self):
        self.input_message = NETWOK_EXISTS
        self.run_bot(parameters={'overwrite': False})
        msg = json_loads(self.get_output_queue()[0])
        self.assertIn(ip_address(msg['source.ip']), ip_network("10.0.0.0/8"))
        self.assertEqual(msg['source.network'], "10.0.0.0/8")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
