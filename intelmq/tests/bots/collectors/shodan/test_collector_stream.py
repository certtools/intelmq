# -*- coding: utf-8 -*-
"""
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.shodan.collector_stream
