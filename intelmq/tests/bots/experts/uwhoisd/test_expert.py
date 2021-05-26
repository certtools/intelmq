# SPDX-FileCopyrightText: 2021 Raphaël Vinot
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
import unittest
import json

import intelmq.lib.test as test
from intelmq.bots.experts.uwhoisd.expert import UniversalWhoisExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://www.cert.at/",
                 "source.ip": "131.130.249.233",
                 "source.asn": "AS760",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }


@test.skip_exotic()
@unittest.skipIf(not os.environ.get('INTELMQ_UNIVERSALWHOIS_TEST'), "UniversalWhois test skipped, as we dont wanna overload public instance")
class TestUniversalWhoisExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = UniversalWhoisExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        event = self.get_output_queue()[0]
        self.assertIsInstance(event, str)
        event = json.loads(event)
        self.assertTrue('NG8867695-NICAT' in event['extra.whois.fqdn'], event['extra.whois.fqdn'])
        self.assertTrue('ORG-VUCC1-RIPE' in event['extra.whois.ip'], event['extra.whois.ip'])
        self.assertTrue('ORG-VUCC1-RIPE' in event['extra.whois.asn'], event['extra.whois.asn'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
