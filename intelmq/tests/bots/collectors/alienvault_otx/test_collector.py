# -*- coding: utf-8 -*-
"""
Testing Alienvault OTX collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.alienvault_otx.collector
