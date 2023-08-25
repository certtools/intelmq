# SPDX-FileCopyrightText: 2023 The Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:44:44 2023

"""

import unittest
import os
import tempfile
import logging
import intelmq.bots.parsers.shadowserver._config as config
import intelmq.lib.utils as utils
import intelmq.lib.test as test

@test.skip_internet()
class TestShadowserverSchemaDownload(unittest.TestCase):

    def test_download(self):
        if not os.environ.get('INTELMQ_SKIP_INTERNET'):
            with tempfile.TemporaryDirectory() as tmp_dir:
                schema_file = config.prepare_update_schema_test(tmp_dir)
                config.set_logger(utils.log('test-bot', log_path=None, log_level=logging.DEBUG))
                self.assertEqual(True, config.update_schema())
                self.assertEqual(True, os.path.exists(schema_file))
