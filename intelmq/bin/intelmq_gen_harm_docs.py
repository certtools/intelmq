#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import json
import textwrap

import pkg_resources

import intelmq.lib.harmonization


HEADER = """
Harmonization field names
=========================

|Section|Name|Type|Description|
|:------|:---|:---|:----------|
"""
HEADER_1 = """

Harmonization types
-------------------

"""
TYPE_SECTION = """### {}
{}

"""


def main():
    output = HEADER

    HARM_CONF = pkg_resources.resource_filename('intelmq', 'etc/harmonization.conf')
    with open(HARM_CONF) as fhandle:
        HARM = json.load(fhandle)['event']

    for key, value in sorted(HARM.items()):
        section = ' '.join([sec.title() for sec in key.split('.')[:-1]])
        output += '|{}|{}|[{}](#{})|{}|\n'.format(' ' if not section else section,  # needed for GitHub
                                                  key, value['type'],
                                                  value['type'].lower(),
                                                  value['description'])

    output += HEADER_1

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
                output += TYPE_SECTION.format(value, doc)
        except TypeError:
            pass

    return output


if __name__ == '__main__':  # pragma: no cover
    print(main())
