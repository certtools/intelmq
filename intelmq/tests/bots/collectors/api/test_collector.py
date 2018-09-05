# -*- coding: utf-8 -*-
"""
Testing API collector
"""

import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    from intelmq.bots.collectors.api.collector_api import APICollectorBot
