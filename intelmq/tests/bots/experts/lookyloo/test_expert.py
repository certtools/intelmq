# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
import unittest
import json
import re

import intelmq.lib.test as test
from intelmq.bots.experts.lookyloo.expert import LookyLooExpertBot


EXAMPLE_INPUT = {"__type": "Event",
                 "source.url": "https://cert.at/",
                 "time.observation": "2015-01-01T00:00:00+00:00"
                 }
EXAMPLE_OUTPUT = {"__type": "Event",
                  "source.url": "https://cert.at/",
                  "screenshot_url": "http://localhost:5100", # will be replaced in the code below
                  "time.observation": "2015-01-01T00:00:00+00:00"
                  }


@test.skip_exotic()
@unittest.skipIf(not os.environ.get('INTELMQ_LOOKYLOO_TEST'), "LookyLoo test skipped, as we dont wanna overload public instance")
class TestLookyLooExpertBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = LookyLooExpertBot

    def test(self):
        self.input_message = EXAMPLE_INPUT
        self.run_bot()
        event = self.get_output_queue()[0]
        self.assertIsInstance(event, str)
        event = json.loads(event)
        match = re.match(r"(.*?)tree/([A-Za-z0-9\-]+)", event['screenshot_url'])
        if match is not None:
            EXAMPLE_OUTPUT['screenshot_url'] = event['screenshot_url']
        self.assertMessageEqual(0, EXAMPLE_OUTPUT)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
