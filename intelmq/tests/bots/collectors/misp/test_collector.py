# -*- coding: utf-8 -*-
"""
Testing MISP collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.misp.collector
