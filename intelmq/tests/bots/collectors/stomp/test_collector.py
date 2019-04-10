# -*- coding: utf-8 -*-
"""
Testing stomp collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.stomp.collector
