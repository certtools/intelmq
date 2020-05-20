# -*- coding: utf-8 -*-
import os
import tempfile
import shutil
import unittest
import json
import os.path as pth

import intelmq.lib.test as test
from intelmq.bots.outputs.files.output import FilesOutputBot


class TestFilesOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = FilesOutputBot
        cls.base_dir = tempfile.TemporaryDirectory()
        cls.incoming_path = pth.join(cls.base_dir.name, "incoming")
        cls.tmp_path = pth.join(cls.base_dir.name, "incoming")

    def setUp(self):
        self.test_output = json.dumps({"asdf": "ghjk"})
        self.input_message = {"__type": "Event", "output": self.test_output}

    def tearDown(self):
        shutil.rmtree(self.incoming_path, ignore_errors=True)
        shutil.rmtree(self.tmp_path, ignore_errors=True)

    def test_event_single_key(self):
        self.sysconfig = {"hierarchical_output": True,
                          "dir": self.incoming_path,
                          "tmp": self.tmp_path,
                          "single_key": "output",
                          "suffix": ""}
        self.run_bot()
        name = os.listdir(self.incoming_path)[0]
        with open(pth.join(self.incoming_path, name), encoding="utf-8") as f:
            data = f.read()
            self.assertEqual(self.test_output, data)

    def test_event_whole(self):
        self.sysconfig = {"hierarchical_output": False,
                          "dir": self.incoming_path,
                          "tmp": self.tmp_path,
                          "single_key": None,
                          "suffix": ""}
        self.run_bot()
        name = os.listdir(self.incoming_path)[0]
        with open(pth.join(self.incoming_path, name), encoding="utf-8") as f:
            data = f.read()
            event = json.loads(data)
            self.assertDictEqual({"output": self.test_output}, event)

    def test_path_error(self):
        self.sysconfig = {"hierarchical_output": False,
                          "dir": self.incoming_path,
                          "tmp": self.tmp_path,
                          "single_key": None,
                          "suffix": ""}
        with open(self.incoming_path, "a"):
            pass
        with self.assertRaises(FileExistsError):
            self.run_bot()

    @classmethod
    def tearDownClass(cls):
        cls.base_dir.cleanup()
        super().tearDownClass()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
