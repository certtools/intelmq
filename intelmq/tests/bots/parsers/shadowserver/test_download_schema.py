# SPDX-FileCopyrightText: 2023 The Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:44:44 2023

"""

import logging
import unittest
import unittest.mock as mock
from intelmq.bots.parsers.shadowserver.parser import ShadowserverParserBot
import intelmq.lib.utils as utils
import intelmq.lib.test as test


@test.skip_internet()
class TestShadowserverSchemaDownload(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = ShadowserverParserBot
        cls.sysconfig = {"logging_level": "DEBUG"}

    def test_download(self):
        self.prepare_bot(prepare_source_queue=False, parameters={'test_mode': True})
        result = False
        with mock.patch('intelmq.lib.utils.load_configuration', new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.get_mocked_logger(self.logger)):
                result = self.bot.test_update_schema()
                self.bot.stop(exitcode=0)
        self.assertEqual(True, result)
