# -*- coding: utf-8 -*-
"""
Tests if configuration in /etc is valid
"""
import collections
import importlib
import json
import re
import unittest

import pkg_resources

import intelmq.lib.harmonization as harmonization


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


CONF_NAMES = ['defaults', 'harmonization', 'pipeline', 'runtime', 'system']

CONF_FILES = {name: pkg_resources.resource_filename('intelmq',
                                                    'etc/' + name + '.conf')
              for name in CONF_NAMES}


class TestConf(unittest.TestCase):
    """
    A TestCase for configuration files.
    """

    def test_defaults_syntax(self):
        """ Test if defaults.conf has correct syntax. """
        with open(CONF_FILES['defaults']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_harmonization(self):
        """ Test if harmonization.conf has correct syntax and valid content. """
        with open(CONF_FILES['harmonization']) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        # Check Json syntax and style
        self.assertEqual(to_json(interpreted), fcontent)

        # check if everything from report is in event and equal, except raw-description
        del interpreted['report']['raw']['description']
        event_copy = interpreted['event'].copy()
        del event_copy['raw']['description']
        self.assertDictContainsSubset(interpreted['report'], event_copy)

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

    def test_bots(self):
        """ Test if BOTS has correct syntax and consistent content. """
        with open(pkg_resources.resource_filename('intelmq',
                                                  'bots/BOTS')) as fhandle:
            fcontent = fhandle.read()

        interpreted = json.loads(fcontent,
                                 object_pairs_hook=collections.OrderedDict)
        self.assertEqual(to_unsorted_json(interpreted), fcontent)

        for groupname, group in interpreted.items():
            for bot_name, bot_config in group.items():
                for field in ['description', 'module', 'parameters']:
                    self.assertIn(field, bot_config)
                importlib.import_module(bot_config['module'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
