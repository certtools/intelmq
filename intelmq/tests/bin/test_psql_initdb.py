# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:04:13 2016

@author: sebastian
"""
import os
import unittest

import pkg_resources

import intelmq.bin.intelmq_psql_initdb as psql_initd


class TestPsqlInit(unittest.TestCase):
    """
    A TestCase for intelmq_psql_initdb.
    """

    def test_output(self):
        """ Compare output to cached one. """
        with open(os.path.join(os.path.dirname(__file__),
                               'initdb.sql')) as handle:
            expected = handle.read()
        fname = pkg_resources.resource_filename('intelmq', 'etc/harmonization.conf')
        self.assertEqual(psql_initd.generate(fname).strip(), expected.strip())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
