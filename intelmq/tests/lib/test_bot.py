# -*- coding: utf-8 -*-
"""

"""
from __future__ import unicode_literals
import io
import logging
import unittest

import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
from intelmq.tests.bots.test_dummy_bot import DummyBot


class TestBot(unittest.TestCase):
    """ Testing generic funtionalties of Bot base class. """

    def reset_bot(self, raise_on_connect=False):
        self.log_stream = io.StringIO()

        src_name = "{}-input".format(self.bot_id)
        dst_name = "{}-output".format(self.bot_id)

        self.config = {}
        self.config["system"] = {"logging_level": "DEBUG",
                                 "http_proxy":  None,
                                 "https_proxy": None,
                                 'broker': 'pythonlist',
                                 'raise_on_connect': raise_on_connect,
                                 }

        self.config["runtime"] = {self.bot_id: {},
                                  "__default__": {"rate_limit": 0,
                                                  "retry_delay": 0,
                                                  "error_retry_delay": 0,
                                                  "error_max_retries": 0,
                                                  'exit_on_error': False,
                                                  }}
        self.config["pipeline"] = {self.bot_id: {"source-queue": (src_name),
                                                 "destination-queues": [dst_name]},
                                   }

        logger = logging.getLogger(self.bot_id)
        logger.setLevel("DEBUG")
        console_formatter = logging.Formatter(utils.LOG_FORMAT)
        console_handler = logging.StreamHandler(self.log_stream)
#        console_handler = logging.StreamHandler()  # TODO: remove
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        self.config["logger"] = logger

        class Parameters(object):
            source_queue = src_name
            destination_queues = [dst_name]
        parameters = Parameters()
        pipe = pipeline.Pythonlist(parameters)
        pipe.set_queues(parameters.source_queue, "source")
        pipe.set_queues(parameters.destination_queues, "destination")
        self.config["source_pipeline"] = pipe
        self.config["destination_pipeline"] = pipe

        self.bot = self.bot_reference(self.bot_id, config=self.config)
        self.pipe = self.config["source_pipeline"]
#        self.input_queue = [self.input_message]

    def test_pipeline_raising(self):
        self.bot_id = 'test-bot'
        self.bot_reference = DummyBot
        self.reset_bot(raise_on_connect=True)
        self.bot.start()
        self.assertIn('ERROR - Pipeline failed', self.log_stream.getvalue())

    def test_pipeline_empty(self):
        self.bot_id = 'test-bot'
        self.bot_reference = DummyBot
        self.reset_bot()
        self.bot.start()
        self.assertIn('ERROR - Bot has found a problem',
                      self.log_stream.getvalue())


if __name__ == '__main__':
    unittest.main()
