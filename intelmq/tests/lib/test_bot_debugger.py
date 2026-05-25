# SPDX-FileCopyrightText: 2026 Mirochill
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from intelmq.lib import utils
from intelmq.lib.bot_debugger import BotDebugger


class TestBotDebugger(unittest.TestCase):

    def test_generate_get_runtime_adds_missing_parameters(self):
        runtime = {
            "collector": {"module": "intelmq.bots.collectors.http.collector_http"},
            "parser": {
                "module": "intelmq.bots.parsers.generic.parser_csv",
                "parameters": None,
            },
            "expert": {
                "module": "intelmq.bots.experts.filter.expert",
                "parameters": {"field": "source.ip"},
            },
        }
        debugger = BotDebugger.__new__(BotDebugger)

        with mock.patch.object(utils, "load_configuration", return_value=runtime):
            config = debugger.generate_get_runtime("DEBUG")()

        self.assertEqual(config["collector"]["parameters"], {"logging_level": "DEBUG"})
        self.assertEqual(config["parser"]["parameters"], {"logging_level": "DEBUG"})
        self.assertEqual(
            config["expert"]["parameters"],
            {"field": "source.ip", "logging_level": "DEBUG"},
        )
        self.assertEqual(config["global"], {"logging_level": "DEBUG"})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
