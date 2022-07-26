#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:52:19 2019

@author: sebastian
"""
from intelmq.lib.utils import get_global_settings

import redis

config = get_global_settings()

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
        stats.append(f"{key.decode()}={value}")
    handle.write("|".join(stats))
    handle.write('\n')
