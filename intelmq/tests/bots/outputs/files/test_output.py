# -*- coding: utf-8 -*-
import os
import tempfile
import unittest
import os.path as pth

import intelmq.lib.test as test
from intelmq.bots.outputs.files.output import FilesOutputBot


class TestFilesOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilesOutputBot
        cls.base_dir = tempfile.TemporaryDirectory()
        cls.sysconfig = {"hierarchical_output": True,
                         "dir": pth.join(cls.base_dir.name, "incoming"),
                         "tmp": pth.join(cls.base_dir.name, "tmp"),
                         "single_key": "output",
                         "suffix": ""}

    def test_event(self):
        test_string = "{\"asfd\":\"ghjk\"}"
        self.input_message = {"__type": "Event", "output": test_string}
        self.run_bot()
        dir = self.sysconfig["dir"]
        name = os.listdir(dir)[0]
        with open(pth.join(dir, name), encoding="utf-8") as f:
            data = f.read()
            self.assertEqual(test_string, data)

    @classmethod
    def tearDownClass(cls):
        cls.base_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
