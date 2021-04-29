# -*- coding: utf-8 -*-
import os
import unittest
import json

import intelmq.lib.test as test
from intelmq.bots.experts.uwhoisd.expert import UniversalWhoisExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "http://www.cert.at/",
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
        self.assertTrue('NG8867695-NICAT' in event['extra.whois'], event['extra.whois'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
