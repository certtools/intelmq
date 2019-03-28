#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:52:19 2019

@author: sebastian
"""
from intelmq import DEFAULTS_CONF_FILE
from intelmq.lib.utils import load_configuration

import redis

config = load_configuration(DEFAULTS_CONF_FILE)

db = redis.Redis(host=config.get('source_pipeline_host', '127.0.0.1'),
                 port=config.get("source_pipeline_port", "6379"),
                 db=3,
                 password=config.get("source_pipeline_password"),
                 )

with open('/var/lib/check_mk_agent/spool/70_intelmq-statistics.txt', 'w') as handle:
    handle.write("<<<local>>>\nP intelmq-statistics ")
    stats = []
    for key in db.keys():
        stats.append("%s=%s" % (key.decode(), db.get(key).decode()))
    handle.write("|".join(stats))
    handle.write('\n')
