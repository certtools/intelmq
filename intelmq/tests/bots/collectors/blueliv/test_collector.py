# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Testing Blueliv crimeserver collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.blueliv.collector_crimeserver
