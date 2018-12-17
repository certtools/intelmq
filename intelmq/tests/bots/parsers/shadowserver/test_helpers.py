# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 15:18:24 2018

@author: sebastian
"""

import unittest
from intelmq.bots.parsers.shadowserver.config import validate_to_none, convert_bool


class TestShadowserverHelpers(unittest.TestCase):

    def test_none(self):
        self.assertEqual(None, validate_to_none(''))
        self.assertEqual(None, validate_to_none('0'))
        self.assertEqual(None, validate_to_none('0'))
        self.assertEqual('1', validate_to_none('1'))
        self.assertEqual('foobar', validate_to_none('foobar'))

    def test_bool(self):
        self.assertEqual(True, convert_bool('true'))
        self.assertEqual(True, convert_bool('y'))
        self.assertEqual(True, convert_bool('yes'))
        self.assertEqual(True, convert_bool('enabled'))
        self.assertEqual(True, convert_bool('1'))
        self.assertEqual(False, convert_bool('false'))
        self.assertEqual(False, convert_bool('n'))
        self.assertEqual(False, convert_bool('no'))
        self.assertEqual(False, convert_bool('disabled'))
        self.assertEqual(False, convert_bool('0'))
