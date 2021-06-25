# SPDX-FileCopyrightText: 2015 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Tests if configuration in /etc is valid
"""
import collections
import importlib
import io
import json
import os
import pkgutil
import pprint
import re
import unittest

import cerberus
import pkg_resources
from ruamel.yaml import YAML

import intelmq.bots
import intelmq.lib.harmonization as harmonization


from intelmq.lib.utils import lazy_int

yaml = YAML(typ="safe", pure=True)

def to_json(obj):
    """
    Transforms object into JSON with intelmq-style.
    """
    return json.dumps(obj, indent=4, sort_keys=True,
                      separators=(',', ': ')) + '\n'


def to_unsorted_json(obj):
    """
    Transforms object into JSON with intelmq-style (without sorting).
    """
    return json.dumps(obj, indent=4, sort_keys=False,
                      separators=(',', ': ')) + '\n'


CONF_FILES = {'harmonization': pkg_resources.resource_filename('intelmq', 'etc/harmonization.conf'),
              'runtime': pkg_resources.resource_filename('intelmq', 'etc/runtime.yaml')}


class TestConf(unittest.TestCase):
    """
    A TestCase for configuration files.
    """

    def test_harmonization(self):
        """ Test if harmonization.conf has correct syntax and valid content. """
        with open(CONF_FILES['harmonization']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        # Check Json syntax and style
        self.assertEqual(to_json(interpreted), fcontent)

        # check if everything from report is in event and equal, except raw's and extra's description
        del interpreted['report']['raw']['description']
        del interpreted['report']['extra']['description']
        event_copy = interpreted['event'].copy()
        del event_copy['raw']['description']
        del event_copy['extra']['description']
        self.assertGreaterEqual(event_copy.items(), interpreted['report'].items())

        # check for valid regex, length and type
        for value in interpreted['event'].values():
            if 'regex' in value:
                re.compile(value['regex'])
            if 'iregex' in value:
                re.compile(value['iregex'])
            if 'length' in value:
                self.assertIsInstance(value['length'], int)
                self.assertGreater(value['length'], 0)
            getattr(harmonization, value['type'])

    def test_runtime_syntax(self):
        """ Test if runtime.yaml has correct syntax. """
        with open(CONF_FILES['runtime']) as fhandle:
            fcontent = fhandle.read()
        interpreted = yaml.load(fcontent)
        buf = io.BytesIO()
        yaml.dump(interpreted, buf)
        self.assertEqual(buf.getvalue().decode(), fcontent)


class CerberusTests(unittest.TestCase):

    cerberus_version = tuple(lazy_int(x) for x in cerberus.__version__.split('.'))

    def convert_cerberus_schema(self, schema: str) -> str:
        """
        > [...] code using prior versions of cerberus would not break, but bring up wrong results!
        > Rename keyschema to valueschema in your schemas. (0.9)
        > Rename propertyschema to keyschema in your schemas. (1.0)

        https://docs.python-cerberus.org/en/stable/upgrading.html
        """
        if self.cerberus_version >= (0, 9):
            schema = schema.replace('"keyschema"', '"valueschema"')
        if self.cerberus_version >= (1, 0):
            schema = schema.replace('"propertyschema"', '"keyschema"')
        return schema

    def test_feeds(self):
        with open(os.path.join(os.path.dirname(__file__), 'assets/feeds.schema.json')) as handle:
            schema = json.loads(self.convert_cerberus_schema(handle.read()))
        with open(pkg_resources.resource_filename('intelmq',
                                                  'etc/feeds.yaml'), encoding='UTF-8') as handle:
            feeds = yaml.load(handle)

        v = cerberus.Validator(schema)

        self.assertTrue(v.validate(feeds),
                        msg='Invalid feeds.yaml file:\n%s' % pprint.pformat(v.errors))



if __name__ == '__main__':  # pragma: no cover
    unittest.main()
