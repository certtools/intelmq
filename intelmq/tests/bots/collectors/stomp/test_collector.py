# -*- coding: utf-8 -*-
"""
Testing n6 stomp collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.n6.collector_stomp
