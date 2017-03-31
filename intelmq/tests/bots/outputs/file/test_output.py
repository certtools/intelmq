# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.file.output import FileOutputBot


class TestFileOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FileOutputBot
        cls.os_fp, cls.filename = tempfile.mkstemp()
        cls.sysconfig = {"hierarchical_output": True,
                         "file": cls.filename}

    def test_event(self):
        self.run_bot()
        filepointer = os.fdopen(self.os_fp, 'rt')
        filepointer.seek(0)

        self.assertEqual('{}\n', filepointer.read())
        filepointer.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
