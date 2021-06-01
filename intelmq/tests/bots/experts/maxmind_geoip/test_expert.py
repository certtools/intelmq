# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.experts.maxmind_geoip.expert
