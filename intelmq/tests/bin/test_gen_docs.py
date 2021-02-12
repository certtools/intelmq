# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 14:04:13 2016

@author: sebastian
"""
import codecs
import os
import unittest

import intelmq.bin.intelmq_gen_docs as gen_docs


class TestGenDocs(unittest.TestCase):
    """
    A TestCase for intelmq_gen_docs.
    """

    def test_harmonization_docs(self):
        """ Check if harmonization docs are up to date. """
        with codecs.open(os.path.join(os.path.dirname(__file__),
                                      '../../../docs/Harmonization-fields.md'),
                         encoding='UTF-8') as handle:
            expected = handle.read()
        self.assertEqual(gen_docs.harm_docs().strip(), expected.strip(),
                         "docs/Harmonization-fields.md does not match the output of "
                         "`intelmq/bin/intelmq_gen_docs.py`. Call it directly to "
                         "update the file.")

    def test_feeds_docs(self):
        """ Check if feeds docs are up to date. """
        with open(os.path.join(os.path.dirname(__file__),
                               '../../../docs/Feeds.md')) as handle:
            expected = handle.read()
        self.assertEqual(gen_docs.feeds_docs().strip(), expected.strip(),
                         "docs/Feeds.md does not match the output of "
                         "`intelmq/bin/intelmq_gen_docs.py`. Call it directly to "
                         "update the file.")


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
