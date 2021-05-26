# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from intelmq.bots.experts.misp.expert import MISPExpertBot
from intelmq.lib.test import BotTestCase

import unittest

class TestMISPExpertBot(BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = MISPExpertBot
