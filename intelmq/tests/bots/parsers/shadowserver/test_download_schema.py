# SPDX-FileCopyrightText: 2023 The Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 19:44:44 2023

"""

import unittest
import os
import logging
from intelmq import VAR_STATE_PATH
import intelmq.bots.parsers.shadowserver._config as config
import intelmq.lib.utils as utils
import intelmq.lib.test as test

@test.skip_internet()
class TestShadowserverSchemaDownload(unittest.TestCase):

    def test_download(self):
        if os.path.isdir(VAR_STATE_PATH):
            schema_file = os.path.join(VAR_STATE_PATH, 'shadowserver-schema.json')
            config.set_logger(utils.log('test-bot', log_path=None))
            if os.path.exists(schema_file):
                os.unlink(schema_file)
            self.assertEqual(True, config.update_schema())
            self.assertEqual(True, os.path.exists(schema_file))
