# -*- coding: utf-8 -*-
import os
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

import intelmq.lib.test as test
from intelmq.bots.outputs.touch.output import TouchOutputBot


class TestTouchOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = TouchOutputBot
        cls.directory = TemporaryDirectory()

    def test_event(self):
        with NamedTemporaryFile(dir=self.directory.name, delete=False) as handle:
            handle.close()
            original = os.path.getmtime(handle.name)
            self.prepare_bot(parameters={'path': handle.name})
            self.run_bot(prepare=False)
            modified = os.path.getmtime(handle.name)
            self.assertGreater(modified, original,
                               msg="File's mtime is not greater as before.")

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
