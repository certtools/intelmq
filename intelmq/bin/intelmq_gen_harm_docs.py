#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:11:06 2015

@author: sebastian
"""
from __future__ import print_function, unicode_literals

import json
import textwrap

import intelmq.lib.harmonization
from intelmq import HARMONIZATION_CONF_FILE


print("""
Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|""")


with open(HARMONIZATION_CONF_FILE) as fhandle:
    HARM = json.load(fhandle)['event']

for key, value in sorted(HARM.items()):
    section = ' '.join([sec.title() for sec in key.split('.')[:-1]])
    print('|{}|{}|{}|{}|'.format(section, key, value['type'],
                                 value['description']))

print("""

Harmonization types
-------------------

""")

for value in sorted(dir(intelmq.lib.harmonization)):
    if value == 'GenericType' or value.startswith('__'):
        continue
    obj = getattr(intelmq.lib.harmonization, value)
    try:
        if issubclass(obj, intelmq.lib.harmonization.GenericType):
            doc = getattr(obj, '__doc__', '')
            if doc is None:
                doc = ''
            else:
                doc = textwrap.dedent(doc)
            print("""### {}
{}

""".format(value, doc))
    except TypeError:
        pass
