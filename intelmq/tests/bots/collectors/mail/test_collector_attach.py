# -*- coding: utf-8 -*-
"""
Testing Mail Attach collector
"""
import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.collectors.mail.collector_mail_attach
