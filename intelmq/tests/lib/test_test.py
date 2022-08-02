# SPDX-FileCopyrightText: 2022 Intevation GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import unittest

from intelmq.lib.test import BOT_INIT_REGEX


BOT_INIT_LINES = (
    # Ubuntu 22.04 https://github.com/certtools/intelmq/issues/2185
    'BOTNAME initialized with id BOTID and intelmq 3.0.2 and python 3.10.4 (main, Apr  2 2022, 09:04:19) [GCC 11.2.0] as process 10051.',
)


class TestBotTestCase(unittest.TestCase):
    def test_bot_init_regex(self):
        for line in BOT_INIT_LINES:
            self.assertRegex(line, BOT_INIT_REGEX.format('BOTNAME', 'BOTID'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
