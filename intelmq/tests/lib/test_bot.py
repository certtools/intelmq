# -*- coding: utf-8 -*-
"""
Tests the Bot class itself.
"""

import io
import json
import logging
import os
import unittest
import unittest.mock as mock

import pkg_resources

import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
from intelmq import (PIPELINE_CONF_FILE, RUNTIME_CONF_FILE, CONFIG_DIR)
from intelmq.lib.test import mocked_logger, BOT_CONFIG


def mocked_config(bot_id='', src_name='', dst_names=(),
                  raise_on_connect=False):

    def load_conf(conf_file):
        if conf_file == PIPELINE_CONF_FILE:
            return {bot_id: {"source-queue": src_name,
                             "destination-queues": dst_names},
                    }
        elif conf_file == RUNTIME_CONF_FILE:
            conf = BOT_CONFIG.copy()
            conf.update({"raise_on_connect": raise_on_connect})
            return {bot_id: conf}
        elif conf_file.startswith(CONFIG_DIR):
            confname = os.path.join('etc/', os.path.split(conf_file)[-1])
            fname = pkg_resources.resource_filename('intelmq',
                                                    confname)
            with open(fname, 'rt') as fpconfig:
                return json.load(fpconfig)
        else:
            with open(conf_file, 'r') as fpconfig:
                return json.load(fpconfig)
    return load_conf

with mock.patch('intelmq.lib.utils.load_configuration', new=mocked_config()):
    from intelmq.tests.bots import test_dummy_bot


class TestBot(unittest.TestCase):
    """ Testing generic funtionalties of Bot base class. """

    def prepare_bot(self, raise_on_connect=False):
        self.log_stream = io.StringIO()
        self.bot_id = 'test-bot'

        src_name = "{}-input".format(self.bot_id)
        dst_name = "{}-output".format(self.bot_id)

        self.mocked_config = mocked_config(self.bot_id,
                                           src_name,
                                           [dst_name],
                                           raise_on_connect)
        logger = logging.getLogger(self.bot_id)
        logger.setLevel("DEBUG")
        console_formatter = logging.Formatter(utils.LOG_FORMAT)
        console_handler = logging.StreamHandler(self.log_stream)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        self.mocked_log = mocked_logger(logger)

        class Parameters(object):
            source_queue = src_name
            destination_queues = [dst_name]
        parameters = Parameters()
        pipe = pipeline.Pythonlist(parameters)
        pipe.set_queues(parameters.source_queue, "source")
        pipe.set_queues(parameters.destination_queues, "destination")

        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
                with mock.patch('intelmq.lib.utils.write_pidfile', lambda x: True):
                    self.bot = self.bot_reference(self.bot_id)
        self.pipe = pipe

    def run_bot(self, raise_on_connect=False):
        self.prepare_bot(raise_on_connect=raise_on_connect)
        with mock.patch('intelmq.lib.utils.load_configuration',
                        new=self.mocked_config):
            with mock.patch('intelmq.lib.utils.log', self.mocked_log):
                self.bot.start()

    def test_pipeline_raising(self):
        self.bot_reference = test_dummy_bot.DummyParserBot
        self.run_bot(raise_on_connect=True)
        self.assertIn('ERROR - Pipeline failed', self.log_stream.getvalue())

    def test_pipeline_empty(self):
        self.bot_reference = test_dummy_bot.DummyParserBot
        self.run_bot()
        self.assertIn('ERROR - Bot has found a problem',
                      self.log_stream.getvalue())


if __name__ == '__main__':
    unittest.main()
