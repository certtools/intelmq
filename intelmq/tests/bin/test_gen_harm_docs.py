# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:04:13 2016

@author: sebastian
"""
import os
import unittest

import intelmq.bin.intelmq_gen_harm_docs as gen_harm_docs


class TestGenHarmDocs(unittest.TestCase):
    """
    A TestCase for intelmq_psql_initdb.
    """

    def test_output(self):
        """ Compare output to cached one. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../../../docs/Harmonization-fields.md')) as handle:
            expected = handle.read()
        self.assertEqual(gen_harm_docs.main().strip(), expected.strip())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
