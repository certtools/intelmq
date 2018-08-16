# -*- coding: utf-8 -*-
"""
Tests if configuration in /etc is valid
"""
import collections
import importlib
import json
import os
import pkgutil
import pprint
import re
import unittest

import cerberus
import pkg_resources
import yaml

import intelmq.bots
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

    def test_modules_in_bots(self):
        """ Test if all bot modules are mentioned BOTS file. """
        with open(pkg_resources.resource_filename('intelmq',
                                                  'bots/BOTS')) as fhandle:
            fcontent = fhandle.read()

        interpreted = json.loads(fcontent,
                                 object_pairs_hook=collections.OrderedDict)
        modules = set(['intelmq.bots.collectors.n6.collector_stomp'])

        for groupname, group in interpreted.items():
            for bot_name, bot_config in group.items():
                modules.add(bot_config['module'])

        for _, groupname, _ in pkgutil.iter_modules(path=intelmq.bots.__path__):
            group = importlib.import_module('intelmq.bots.%s' % groupname)
            for _, providername, _ in pkgutil.iter_modules(path=group.__path__):
                provider = importlib.import_module('intelmq.bots.%s.%s' % (groupname, providername))
                for _, botname, _ in pkgutil.iter_modules(path=provider.__path__):
                    classname = 'intelmq.bots.%s.%s.%s' % (groupname, providername, botname)
                    self.assertFalse(classname not in modules and '_' in botname,
                                    msg="Bot %r not found in BOTS file." % classname)


class CerberusTests(unittest.TestCase):
    def test_bots(self):
        with open(os.path.join(os.path.dirname(__file__), 'assets/bots.schema.json')) as handle:
            schema = json.load(handle)
        with open(pkg_resources.resource_filename('intelmq',
                                                  'bots/BOTS')) as handle:
            bots = json.load(handle)

        v = cerberus.Validator(schema)

        self.assertTrue(v.validate(bots),
                        msg='Invalid BOTS file:\n%s' % pprint.pformat(v.errors))

    def test_feeds(self):
        with open(os.path.join(os.path.dirname(__file__), 'assets/feeds.schema.json')) as handle:
            schema = json.load(handle)
        with open(pkg_resources.resource_filename('intelmq',
                                                  'etc/feeds.yaml')) as handle:
            feeds = yaml.load(handle)

        v = cerberus.Validator(schema)

        self.assertTrue(v.validate(feeds),
                        msg='Invalid feeds.yaml file:\n%s' % pprint.pformat(v.errors))



if __name__ == '__main__':  # pragma: no cover
    unittest.main()
