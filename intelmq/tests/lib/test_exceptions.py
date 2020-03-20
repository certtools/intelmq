# -*- coding: utf-8 -*-
"""
Testing the IntelMQ-specific exceptions
"""
import unittest

import intelmq.lib.exceptions as excs


class TestUtils(unittest.TestCase):

    def test_MissingDependencyError(self):
        depname = 'libname'
        version = '1.2.3'
        installed = '1.0.0'
        additional = 'This is the end.'

        exc = excs.MissingDependencyError(depname)
        self.assertIn(repr(depname), str(exc))

        exc = excs.MissingDependencyError(depname, version)
        self.assertIn(repr(depname), str(exc))
        self.assertIn(version, str(exc))

        exc = excs.MissingDependencyError(depname, version, installed)
        self.assertIn(repr(depname), str(exc))
        self.assertIn(version, str(exc))
        self.assertIn(repr(installed), str(exc))

        # installed should not show up if version is not given
        exc = excs.MissingDependencyError(depname, installed=installed)
        self.assertIn(repr(depname), str(exc))
        self.assertNotIn(version, str(exc))
        self.assertNotIn(repr(installed), str(exc))

        # additional text at the end
        exc = excs.MissingDependencyError(depname, additional_text=additional)
        self.assertIn(repr(depname), str(exc))
        self.assertTrue(str(exc).endswith(" %s" % additional))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
