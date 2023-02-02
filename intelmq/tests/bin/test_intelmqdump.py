# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import termstyle

from intelmq.bin import intelmqdump


class TestCompleter(unittest.TestCase):
    """
    A TestCase for Completer.
    """

    def test_simple(self):
        comp = intelmqdump.Completer(['foo', 'foobar', 'else'])
        self.assertEqual(comp.complete('', 0), 'else')
        self.assertEqual(comp.complete('', 2), 'foobar')
        self.assertEqual(comp.complete('f', 0), 'foo')
        self.assertEqual(comp.complete('f', 1), 'foobar')
        self.assertEqual(comp.complete('a', 0), None)

    def test_queues(self):
        comp = intelmqdump.Completer(['r ', 'a '],
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


class TestIntelMQDump(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tmp_log_dir = tempfile.TemporaryDirectory()
        self.global_config = {}
        self.runtime_config = {}
        self.bot_configs = {}

        self.config_patcher = mock.patch.multiple(
            intelmqdump.utils,
            get_global_settings=mock.Mock(side_effect=self._mocked_global_config),
            get_runtime=mock.Mock(side_effect=self._mocked_runtime_config),
            get_bots_settings=mock.Mock(side_effect=self._mocked_bots_config))
        self.config_patcher.start()

        self.ctl_config_patcher = mock.patch.multiple(
            intelmqdump.intelmqctl.utils,
            load_configuration=mock.Mock(side_effect=self._mocked_runtime_config))
        self.ctl_config_patcher.start()

        # Coloring output makes asserts unnecessary complicated
        termstyle.disable()

    def _mocked_global_config(self):
        return self.global_config

    def _mocked_runtime_config(self, *args):
        return {"global": self.global_config, **self.runtime_config}

    def _mocked_bots_config(self, bot_id):
        return self.bot_configs[bot_id]

    def _prepare_empty_dump(self, filename: str):
        path = Path(f"{self.tmp_log_dir.name}/{filename}.dump")
        path.parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch()

    def tearDown(self) -> None:
        self.ctl_config_patcher.stop()
        self.config_patcher.stop()
        self.tmp_log_dir.cleanup()
        termstyle.auto()
        return super().tearDown()

    def _run_main(self, argv: list) -> str:
        """Helper for running intelmqdump.main and capturing output"""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with contextlib.suppress(SystemExit):
                intelmqdump.main(argv)
        return output.getvalue().split("\n")

    @mock.patch.object(intelmqdump, "input", return_value='q')
    def test_list_dumps_for_all_bots_from_default_log_path(self, _):
        self._prepare_empty_dump('test-1')
        self._prepare_empty_dump('test-2')

        with mock.patch.object(intelmqdump, "DEFAULT_LOGGING_PATH", self.tmp_log_dir.name):
            output = self._run_main([])

        self.assertIn("0: test-1 empty file", output[1])
        self.assertIn("1: test-2 empty file", output[2])

    @mock.patch.object(intelmqdump, "input", return_value='q')
    def test_list_dumps_for_all_bots_from_custom_locations(self, _):
        self.global_config = {"logging_path": self.tmp_log_dir.name}
        self._prepare_empty_dump('bot-1/test-1')
        self._prepare_empty_dump('bot-2/test-2')

        self.runtime_config = {
            "bot-1": {
                "parameters": {
                    "logging_path": f"{self.tmp_log_dir.name}/bot-1"
                }
            },
            "bot-2": {
                "parameters": {
                    "logging_path": f"{self.tmp_log_dir.name}/bot-2"
                }
            }
        }

        output = self._run_main([])

        self.assertIn("0: test-1 empty file", output[1])
        self.assertIn("1: test-2 empty file", output[2])

    @mock.patch.object(intelmqdump, "input")
    def test_list_and_select_dump_from_global_location(self, input_mock):
        self._prepare_empty_dump('test-1')

        self.global_config = {"logging_path": self.tmp_log_dir.name}

        for selector in ['0', 'test-1']:
            with self.subTest(selector):
                input_mock.side_effect = [selector, 'q']
                output = self._run_main([])

                self.assertIn("0: test-1 empty file", output[1])
                # Enough to check that the correct file path was used
                self.assertIn("Processing test-1: empty file", output[2])

    @mock.patch.object(intelmqdump, "input")
    def test_list_and_select_dump_from_custom_location(self, input_mock):
        self.global_config = {"logging_path": self.tmp_log_dir.name}
        self._prepare_empty_dump('/bot-1/test-1')

        self.runtime_config = {
            "bot-1": {
                "parameters": {
                    "logging_path": f"{self.tmp_log_dir.name}/bot-1"
                }
            },
        }
        for selector in ['0', 'test-1']:
            with self.subTest(selector):
                input_mock.side_effect = [selector, 'q']
                output = self._run_main([])

                self.assertIn("0: test-1 empty file", output[1])
                # Enough to check that the correct file path was used
                self.assertIn("Processing test-1: empty file", output[2])

    @mock.patch.object(intelmqdump, "input")
    def test_selecting_dump_warns_when_filename_is_ambiguous(self, input_mock):
        """With different locations used, there could be a case of dumps with the same
            filename. Then, if user tried to select using filename, warn and exit.
            Selecting using numbers should be supported"""

        self._prepare_empty_dump('test-1')
        self._prepare_empty_dump('bot-1/test-1')

        self.global_config = {"logging_path": self.tmp_log_dir.name}
        self.runtime_config = {
            "bot-1": {
                "parameters": {
                    "logging_path": f"{self.tmp_log_dir.name}/bot-1"
                }
            },
        }

        with self.subTest("warn on ambiguous filename"):
            input_mock.side_effect = ['test-1']
            output = self._run_main([])

            self.assertIn("0: test-1 empty file", output[1])
            self.assertIn("1: test-1 empty file", output[2])
            self.assertIn("Given filename is not unique, please use number", output[3])

        with self.subTest("allow selecting using number"):
            input_mock.side_effect = ['1', 'q']
            output = self._run_main([])
            self.assertIn("Processing test-1: empty file", output[3])

    @mock.patch.object(intelmqdump, "input", return_value='q')
    def test_get_dump_for_one_bot(self, _):
        self._prepare_empty_dump("bot/bot-1")
        self.global_config = {"logging_path": self.tmp_log_dir.name}
        self.bot_configs = {"bot-1": {"parameters": {"logging_path": f"{self.tmp_log_dir.name}/bot"}}}

        output = self._run_main(["bot-1"])
        self.assertIn("Processing bot-1: empty file", output[0])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
