# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import unittest

import json


def to_json(obj):
    return json.dumps(obj, indent=4, sort_keys=True,
                      separators=(',', ': ')) + '\n'


class TestConf(unittest.TestCase):
    """
    A TestCase for configutation files.
    """

    def test_defaults_syntax(self):
        """ Test if defaults.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/defaults.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_harmonization_syntax(self):
        """ Test if harmonization.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/harmonization.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_pipeline_syntax(self):
        """ Test if pipeline.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/pipeline.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_runtime_syntax(self):
        """ Test if runtime.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/runtime.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_startup_syntax(self):
        """ Test if startup.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/startup.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_system_syntax(self):
        """ Test if system.conf has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../conf/system.conf')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)

    def test_BOTS_syntax(self):
        """ Test if BOTS has correct syntax. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../bots/BOTS')) as fhandle:
            fcontent = fhandle.read()
        interpreted = json.loads(fcontent)
        self.assertEqual(to_json(interpreted), fcontent)


if __name__ == '__main__':
    unittest.main()
