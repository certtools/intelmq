# -*- coding: utf-8 -*-
import unittest

import intelmq.bin.intelmqdump


class TestCompleter(unittest.TestCase):
    """
    A TestCase for Completer.
    """

    def test_simple(self):
        comp = intelmq.bin.intelmqdump.Completer(['foo', 'foobar', 'else'])
        self.assertEqual(comp.complete('', 0), 'else')
        self.assertEqual(comp.complete('', 2), 'foobar')
        self.assertEqual(comp.complete('f', 0), 'foo')
        self.assertEqual(comp.complete('f', 1), 'foobar')
        self.assertEqual(comp.complete('a', 0), None)

    def test_queues(self):
        comp = intelmq.bin.intelmqdump.Completer(['r ', 'a '],
                                                 queues={'some-parser-queue', 'some-expert-queue'})
        self.assertEqual(comp.complete('r ', 0), 'r ')
        self.assertEqual(comp.complete('r 1 ', 0), 'r 1 some-expert-queue')
        self.assertEqual(comp.complete('r 1 ', 1), 'r 1 some-parser-queue')
        self.assertEqual(comp.complete('r 1 ', 2), None)
        self.assertEqual(comp.complete('r 2', 0), None)
        self.assertEqual(comp.complete('a  ', 0), 'a  some-expert-queue')
        self.assertEqual(comp.complete('a  ', 2), None)
        self.assertEqual(comp.complete('r  34 some-p', 0), 'r  34 some-parser-queue')
        self.assertEqual(comp.complete('a some-e', 0), 'a some-expert-queue')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
