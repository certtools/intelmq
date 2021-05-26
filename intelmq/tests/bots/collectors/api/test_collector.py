# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing API collector
"""

import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    from intelmq.bots.collectors.api.collector_api import APICollectorBot
