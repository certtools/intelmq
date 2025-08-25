"""
SPDX-FileCopyrightText: 2025 Institute for Common Good Technology & Malawi CERT
SPDX-License-Identifier: AGPL-3.0-or-later
"""

import os
import unittest

import intelmq.lib.test as test

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    from intelmq.bots.collectors.shodan.collector_alert import ShodanAlertCollectorBot


@test.skip_exotic()
class TestShodanAlertCollectorBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShodanAlertCollectorBot
        cls.sysconfig = {'api_key': 'dummy'}


if __name__ == '__main__':
    unittest.main()
