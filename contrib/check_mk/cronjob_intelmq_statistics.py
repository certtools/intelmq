#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:52:19 2019

@author: sebastian
"""
from intelmq import DEFAULTS_CONF_FILE
from intelmq.lib.utils import load_configuration

import redis

config = load_configuration(DEFAULTS_CONF_FILE)

db = redis.Redis(host=config.get('statistics_host', '127.0.0.1'),
                 port=config.get("statistics_port", 6379),
                 db=config.get("statistics_database", 3),
                 password=config.get("statistics_password"),
                 )

with open('/var/lib/check_mk_agent/spool/70_intelmq-statistics.txt', 'w') as handle:
    handle.write("<<<local>>>\nP intelmq-statistics ")
    stats = []
    for key in db.keys():
        value = db.get(key)
        if value is None:
            value = '0'
        else:
            value = value.decode()
        stats.append("%s=%s" % (key.decode(), value))
    handle.write("|".join(stats))
    handle.write('\n')
