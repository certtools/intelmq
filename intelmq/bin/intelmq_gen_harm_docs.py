#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import json
import textwrap

import intelmq.lib.harmonization
import pkg_resources

print("""
Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|""")

HARM_CONF = pkg_resources.resource_filename('intelmq', 'etc/harmonization.conf')
with open(HARM_CONF) as fhandle:
    HARM = json.load(fhandle)['event']

for key, value in sorted(HARM.items()):
    section = ' '.join([sec.title() for sec in key.split('.')[:-1]])
    print('|{}|{}|[{}](#{})|{}|'.format(section, key, value['type'],
                                        value['type'].lower(),
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
