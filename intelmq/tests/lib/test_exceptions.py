# -*- coding: utf-8 -*-
"""
Testing the IntelMQ-specific exceptions
"""
import unittest
import sys

import intelmq.lib.exceptions as excs


class TestUtils(unittest.TestCase):

    def test_PipelineError(self):
        message = 'some error'
        source = ValueError(message)
        try:
            try:
                raise source
            except ValueError as exc:
                raise excs.PipelineError(exc)
        except excs.PipelineError as exc:
            exception = exc
        if sys.version_info < (3, 7):
            self.assertEqual(exception.args, ('pipeline failed - ValueError(%r,)' % message, ))
        else:
            self.assertEqual(exception.args, ('pipeline failed - ValueError(%r)' % message, ))

        message = 'some error'
        notanexception = excs.PipelineError(message)
        self.assertEqual(notanexception.args, ('pipeline failed - %r' % message, ))

    def test_MissingDependencyError(self):
        depname = 'libname'
        version = '1.2.3'
        installed = '1.0.0'
        additional = 'This is the end.'

        exc = str(excs.MissingDependencyError(depname))
        self.assertIn(repr(depname), exc)

        exc = str(excs.MissingDependencyError(depname, version))
        self.assertIn(repr(depname), exc)
        self.assertIn(version, exc)
        self.assertIn('or higher', exc)

        exc = str(excs.MissingDependencyError(depname, '>1.0,<2.0'))
        self.assertIn(repr(depname), exc)
        self.assertNotIn('or higher', exc)

        exc = str(excs.MissingDependencyError(depname, version, installed))
        self.assertIn(repr(depname), exc)
        self.assertIn(version, exc)
        self.assertIn(repr(installed), exc)

        # installed should not show up if version is not given
        exc = str(excs.MissingDependencyError(depname, installed=installed))
        self.assertIn(repr(depname), exc)
        self.assertNotIn(version, exc)
        self.assertNotIn(repr(installed), exc)

        # additional text at the end
        exc = str(excs.MissingDependencyError(depname, additional_text=additional))
        self.assertIn(repr(depname), exc)
        self.assertTrue(exc.endswith(" %s" % additional))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
