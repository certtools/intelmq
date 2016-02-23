# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import unittest

import pkg_resources


def to_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True,
                      separators=(',', ': ')) + '\n'


CONF_NAMES = ['defaults', 'harmonization', 'pipeline', 'runtime', 'startup',
              'system']

CONF_FILES = {name: pkg_resources.resource_filename('intelmq',
                                                    'etc/' + name + '.conf')
              for name in CONF_NAMES}


class TestConf(unittest.TestCase):
    """
    A TestCase for configutation files.
    """

    def test_defaults_syntax(self):
        """ Test if defaults.conf has correct syntax. """
        with open(CONF_FILES['defaults']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_harmonization_syntax(self):
        """ Test if harmonization.conf has correct syntax. """
        with open(CONF_FILES['harmonization']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_pipeline_syntax(self):
        """ Test if pipeline.conf has correct syntax. """
        with open(CONF_FILES['pipeline']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_runtime_syntax(self):
        """ Test if runtime.conf has correct syntax. """
        with open(CONF_FILES['runtime']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_startup_syntax(self):
        """ Test if startup.conf has correct syntax. """
        with open(CONF_FILES['startup']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_system_syntax(self):
        """ Test if system.conf has correct syntax. """
        with open(CONF_FILES['system']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_BOTS_syntax(self):
        """ Test if BOTS has correct syntax. """
        with open(pkg_resources.resource_filename('intelmq',
                                                  'bots/BOTS')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)


if __name__ == '__main__':
    unittest.main()
