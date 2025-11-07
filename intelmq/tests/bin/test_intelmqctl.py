# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
import unittest
from tempfile import TemporaryDirectory
from unittest import mock
from pathlib import Path

from pkg_resources import resource_filename

import intelmq.bin.intelmqctl as ctl
import intelmq.lib.utils as utils
from intelmq.lib.test import skip_installation


class TestIntelMQProcessManager(unittest.TestCase):
    def test_interpret_commandline(self):
        func = ctl.IntelMQProcessManager._interpret_commandline
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/local/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertFalse(func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http', 'test-collector'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))

        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertTrue(func(1, ('/usr/bin/python3', '/usr/local/bin/intelmqctl', 'run', 'test-collector'),
                             'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertFalse(func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run', 'test-collector'),
                              'intelmq.bots.collectors.http.collector_http', 'other-collector'))

        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl', 'run'),
                           'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmqctl'),
                           'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3'),
                           'intelmq.bots.collectors.http.collector_http', 'other-collector'))
        self.assertIn('could not be interpreted',
                      func(1, ('/usr/bin/python3', '/usr/bin/intelmq.bots.collectors.http.collector_http'),
                           'intelmq.bots.collectors.http.collector_http', 'test-collector'))
        self.assertIn('error',
                      func(1, (),
                           'intelmq.bots.collectors.http.collector_http', 'other-collector'))


class TestIntelMQController(unittest.TestCase):
    BOT_CONFIG = {"test-bot":
                  {
                      "bot-id": "bot-1",
                      "module": "sys",
                      "description": "Dummy bot",
                      "group": "expert",
                      "name": "DummyBot",
                      "enabled": False,
                  }
                  }

    def setUp(self):
        super().setUp()

        utils.drop_privileges()

        self.tmp_config_dir = TemporaryDirectory()

        self.tmp_runtime = f"{self.tmp_config_dir.name}/runtime.yaml"
        self._extend_config(self.tmp_runtime, {})

        self.tmp_harmonization = f"{self.tmp_config_dir.name}/harmonization.yaml"
        self._extend_config(self.tmp_harmonization, {}, useyaml=False)

        self.ctl_conf_patcher = mock.patch.multiple(ctl, RUNTIME_CONF_FILE=self.tmp_runtime,
                                                    HARMONIZATION_CONF_FILE=self.tmp_harmonization)
        self.ctl_conf_patcher.start()

        self.intelmqctl = ctl.IntelMQController()

    def _extend_config(self, path: str, to_extend: dict, useyaml: bool = True):
        if not os.path.exists(path):
            open(path, 'x').close()

        config = utils.load_configuration(path) or {}
        config.update(to_extend)
        utils.write_configuration(path, config, backup=False, useyaml=useyaml)

    def _load_default_harmonization(self):
        default = utils.load_configuration(resource_filename('intelmq',
                                                             'etc/harmonization.conf'))
        self._extend_config(self.tmp_harmonization, default, useyaml=False)

    def _load_default_runtime(self):
        default = utils.load_configuration(resource_filename('intelmq',
                                                             'etc/runtime.yaml'))
        self._extend_config(self.tmp_runtime, default)

    def tearDown(self):
        self.ctl_conf_patcher.stop()
        self.tmp_config_dir.cleanup()
        return super().tearDown()

    @skip_installation()
    def test_check_passed_with_default_harmonization_and_empty_runtime(self):
        self._load_default_harmonization()
        self.assertEqual((0, 'success'), self.intelmqctl.check(no_connections=True, check_executables=False))

    @skip_installation()
    def test_check_pass_with_default_runtime(self):
        with mock.patch.object(ctl.utils, "RUNTIME_CONF_FILE", self.tmp_runtime):
            self._load_default_harmonization()
            self._load_default_runtime()
            self.assertEqual((0, 'success'), self.intelmqctl.check(no_connections=True, check_executables=False))

    @skip_installation()
    @mock.patch.object(ctl.importlib, "import_module", mock.Mock(side_effect=SyntaxError))
    def test_check_handles_syntaxerror_when_importing_bots(self):
        self._load_default_harmonization()
        self._extend_config(self.tmp_runtime, self.BOT_CONFIG)

        with self.assertLogs() as captured:
            self.assertEqual((1, 'error'), self.intelmqctl.check(no_connections=True))

        self.assertIsNotNone(
            next(filter(lambda l: "SyntaxError in bot 'test-bot'" in l, captured.output)))

    @skip_installation()
    @mock.patch.object(utils, "get_bot_module_name", mock.Mock(return_value="mocked-module"))
    def test_check_imports_real_bot_module(self):
        self._load_default_harmonization()
        self._extend_config(self.tmp_runtime, self.BOT_CONFIG)

        # raise SyntaxError to stop checking after import
        with mock.patch.object(ctl.importlib, "import_module", mock.Mock(side_effect=SyntaxError)) as import_mock:
            self.intelmqctl.check(no_connections=True, check_executables=False)

        import_mock.assert_called_once_with("mocked-module")

    def test_intelmqctl_log(self):
        path = Path(__file__).absolute().parent / '../assets/'
        self.intelmqctl._parameters.logging_path = path
        retval, error_log = self.intelmqctl.read_bot_log('test-bot', 'ERROR', 10)
        assert retval == 0 and len(error_log) == 1
        assert error_log[0]['extended_message'].startswith('Traceback')
        del error_log[0]['extended_message']
        assert error_log[0] == {'date': '2025-04-23T23:17:52.240000',
                                'bot_id': 'test-bot', 'thread_id': None, 'log_level': 'ERROR',
                                'message': 'Bot initialization failed.'}
        for level, allowed_levels, number_messages in (
            ('DEBUG', ('DEBUG', 'INFO', 'WARNING', 'ERROR'), 26),
            ('INFO', ('INFO', 'WARNING', 'ERROR'), 9),
            ('WARNING', ('WARNING', 'ERROR'), 2),
            ('ERROR', ('ERROR', ), 1),
            ('CRITICAL', ('CRITICAL', ), 0),
        ):
            retval, log_messages = self.intelmqctl.read_bot_log('test-bot', level, 30)
            assert retval == 0 and len(log_messages) == number_messages
            for log_message in log_messages:
                assert log_message['log_level'] in allowed_levels


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
