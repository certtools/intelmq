# -*- coding: utf-8 -*-

"""
Testing annotations
"""

import json

import unittest

from intelmq.bots.experts.certbund_contact.annotations import from_json, \
     Annotation, AnnotationError


class TestAnnotations(unittest.TestCase):

    def test_tag(self):
        annotation = from_json(json.loads('{"tag": "daily"}'))
        self.assertEqual(annotation.tag, "daily")

    def test_tag_equality(self):
        annotation1 = from_json(json.loads('{"tag": "daily"}'))
        annotation2 = from_json(json.loads('{"tag": "daily"}'))
        self.assertTrue(annotation1 == annotation2)
        self.assertFalse(annotation1 != annotation2)
        self.assertTrue(hash(annotation1) == hash(annotation2))

    def test_tag_inequality(self):
        annotation1 = from_json(json.loads('{"tag": "hourly"}'))
        annotation2 = from_json(json.loads('{"tag": "daily"}'))
        self.assertTrue(annotation1 != annotation2)
        self.assertFalse(annotation1 == annotation2)

    def test_tag_condition(self):
        annotation = from_json(json.loads('{"tag": "test-condition"'
                                          ',"condition":'
                                          '["eq"'
                                          ', ["event_field"'
                                          '  , "classification.identifier"'
                                          '  ]'
                                          ', "opensnmp"]'
                                          '}'))
        self.assertEqual(annotation.tag, "test-condition")
        self.assertTrue(annotation.matches({"classification.identifier":
                                            "opensnmp"}))

    def test_tag_default_condition(self):
        annotation = from_json(json.loads('{"tag": "test-default-condition"}'))
        self.assertEqual(annotation.tag, "test-default-condition")
        self.assertTrue(annotation.matches({}))

    def test_tag_always_true(self):
        annotation = from_json(json.loads('{"tag": "test-always-true"'
                                          ',"condition": true'
                                          '}'))
        self.assertEqual(annotation.tag, "test-always-true")
        self.assertTrue(annotation.matches({}))

    def test_annotation_no_tag(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"abc": "123"}'))

    def test_tag_non_string_value(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"tag": 123}'))

    def test_inhibition(self):
        annotation = from_json(json.loads('{"tag": "inhibition"'
                                          ',"condition":'
                                          '["eq"'
                                          ', ["event_field"'
                                          '  , "classification.identifier"'
                                          '  ]'
                                          ', "openportmapper"]'
                                          '}'))
        self.assertTrue(annotation.matches({"classification.identifier":
                                            "openportmapper"}))
        self.assertFalse(annotation.matches({"classification.identifier":
                                             "openmongodb"}))

    def test_inhibition_equality(self):
        annotation1 = from_json(json.loads('{"tag": "inhibition"'
                                           ',"condition":'
                                           '["eq"'
                                           ', ["event_field"'
                                           '  , "classification.identifier"'
                                           '  ]'
                                           ', "openportmapper"]'
                                           '}'))
        annotation2 = from_json(json.loads('{"tag": "inhibition"'
                                           ',"condition":'
                                           '["eq"'
                                           ', ["event_field"'
                                           '  , "classification.identifier"'
                                           '  ]'
                                           ', "openportmapper"]'
                                           '}'))
        self.assertTrue(annotation1 == annotation2)
        self.assertFalse(annotation1 != annotation2)
        self.assertTrue(hash(annotation1) == hash(annotation2))

    def test_inhibition_inequality(self):
        annotation1 = from_json(json.loads('{"tag": "inhibition"'
                                           ',"condition":'
                                           '["eq"'
                                           ', ["event_field"'
                                           '  , "classification.identifier"'
                                           '  ]'
                                           ', "openportmapper"]'
                                           '}'))
        annotation2 = from_json(json.loads('{"tag": "inhibition"'
                                           ',"condition":'
                                           '["eq"'
                                           ', ["event_field"'
                                           '  , "classification.identifier"'
                                           '  ]'
                                           ', "openmongodb"]'
                                           '}'))
        self.assertFalse(annotation1 == annotation2)
        self.assertTrue(annotation1 != annotation2)

    def test_inhibition_true(self):
        annotation = from_json(json.loads('{"tag": "inhibition"'
                                          ',"condition": true}'))
        self.assertTrue(annotation.matches({}))

    def test_inhibition_unknown_function(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"tag": "inhibition"'
                                 ',"condition": ["some_function", 1, "value"]'
                                 '}'))

    def test_inhibition_eq_missing_parameters(self):
        with self.assertRaises(AnnotationError):
            from_json(json.loads('{"tag": "inhibition"'
                                   ',"condition":'
                                 '["eq", "openportmapper"]'
                                 '}'))

    def test_annotation_class_instantiation_no_condition(self):
        # Annotation objects have a default condition that matches all
        # events:
        self.assertTrue(Annotation("a tag").matches({}))



if __name__ == "__main__":
    unittest.main()
