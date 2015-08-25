# -*- coding: utf-8 -*-
"""
Testing harmonization classes
"""
from __future__ import unicode_literals

import unittest

import intelmq.lib.harmonization as harmonization


class TestHarmonization(unittest.TestCase):

    def test_boolean_valid_bool(self):
        """ Test Boolean.is_valid with bool values. """
        self.assertTrue(harmonization.Boolean.is_valid(True))
        self.assertTrue(harmonization.Boolean.is_valid(False))

    def test_boolean_valid_other(self):
        """ Test Boolean.is_valid with otehr invalid values. """
        self.assertFalse(harmonization.Boolean.is_valid(None))
        self.assertFalse(harmonization.Boolean.is_valid('True'))
        self.assertFalse(harmonization.Boolean.is_valid(0))
        self.assertFalse(harmonization.Boolean.is_valid(1))
        self.assertFalse(harmonization.Boolean.is_valid([]))

    def test_boolean_sanitize_bool(self):
        """ Test Boolean.sanitize with bool values. """
        self.assertTrue(harmonization.Boolean.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid(False, sanitize=True))

    def test_boolean_sanitize_valid(self):
        """ Test Boolean.sanitize with valid string and int values. """
        self.assertTrue(harmonization.Boolean.is_valid(0, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid(1, sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid('true', sanitize=True))
        self.assertTrue(harmonization.Boolean.is_valid('false', sanitize=True))

    def test_boolean_sanitize_invalid(self):
        """ Test Boolean.sanitize with invalid values. """
        self.assertFalse(harmonization.Boolean.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Boolean.is_valid([], sanitize=True))
        self.assertFalse(harmonization.Boolean.is_valid('test', sanitize=True))

    def test_integer_valid_int(self):
        """ Test Integer.is_valid with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(-4532))
        self.assertTrue(harmonization.Integer.is_valid(1337))

    def test_integer_valid_other(self):
        """ Test Integer.is_valid with invalid values. """
        self.assertFalse(harmonization.Integer.is_valid(-4532L))
        self.assertFalse(harmonization.Integer.is_valid('1337'))
        self.assertFalse(harmonization.Integer.is_valid(True))

    def test_integer_sanitize_int(self):
        """ Test Integer.sanitize with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(-4532, sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(1337, sanitize=True))

    def test_integer_sanitize_other(self):
        """ Test Integer.sanitize with integer values. """
        self.assertTrue(harmonization.Integer.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid('1337', sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(b'1337', sanitize=True))
        self.assertTrue(harmonization.Integer.is_valid(' 1337', sanitize=True))

    def test_integer_sanitize_invalid(self):
        """ Test Integer.sanitize with invalid values. """
        self.assertFalse(harmonization.Integer.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Integer.is_valid('b13', sanitize=True))

    def test_float_valid_flaot(self):
        """ Test Float.is_valid with flaot and integer values. """
        self.assertTrue(harmonization.Float.is_valid(-4532))
        self.assertTrue(harmonization.Float.is_valid(1337))
        self.assertTrue(harmonization.Float.is_valid(1337.2354))

    def test_float_valid_other(self):
        """ Test Float.is_valid with invalid values. """
        self.assertFalse(harmonization.Float.is_valid(-4532L))
        self.assertFalse(harmonization.Float.is_valid('1337.234'))
        self.assertFalse(harmonization.Float.is_valid(True))

    def test_float_sanitize_float(self):
        """ Test Float.sanitize with integer values. """
        self.assertTrue(harmonization.Float.is_valid(-4532.234, sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(13.234e-4, sanitize=True))

    def test_float_sanitize_other(self):
        """ Test Float.sanitize with integer values. """
        self.assertTrue(harmonization.Float.is_valid(True, sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('+137.23', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(b'17.234', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid(' 1337.2', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('3.31e+3', sanitize=True))
        self.assertTrue(harmonization.Float.is_valid('-31.e-2', sanitize=True))

    def test_float_sanitize_invalid(self):
        """ Test Float.sanitize with invalid values. """
        self.assertFalse(harmonization.Float.is_valid(None, sanitize=True))
        self.assertFalse(harmonization.Float.is_valid('b13.23', sanitize=True))

if __name__ == "__main__":
    unittest.main()
