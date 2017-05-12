# -*- coding: utf-8 -*-
"""
Utilities for debugging intelmq bots.

BotDebugger is called via intelmqctl. It starts a live running bot instance,
leverages logging to DEBUG level and permits even a non-skilled programmer
who may find themselves puzzled with Python nuances and server deployment twists
to see what's happening in the bot and where's the error.

Depending on the subcommand received, the class either
 * starts the bot as is (default)
 * processes single message, either injected or from default pipeline (process subcommand)
 * reads the message from input pipeline or send a message to output pipeline (message subcommand)
"""
import logging
import json

from intelmq.lib.message import Event
from importlib import import_module
from intelmq.lib.utils import StreamHandler
from intelmq.lib.message import Event


class BotDebugger:
        def leverageLogger(self, level = logging.DEBUG):
            self.instance.logger.setLevel(level)
            for h in self.instance.logger.handlers:
                if isinstance(h, StreamHandler):
                    h.setLevel(level)

        def __init__(self, module_path, bot_id, run_subcommand = None, message_kind = None, dryrun = None, msg = None):
            module = import_module(module_path)
            bot = getattr(module, 'BOT')
            self.instance = bot(bot_id)
            self.leverageLogger()

            if not run_subcommand:
                self.instance.start()
            else:
                self.instance._Bot__connect_pipelines()
                if run_subcommand == "process":
                    self._process(dryrun, msg)
                elif run_subcommand == "message":
                    self.leverageLogger(level = logging.INFO)
                    self._message(message_kind, msg)
                else:
                    print("Subcommand {} not known.".format(run_subcommand))

        def _process(self, dryrun, msg):
            if msg:
                self.instance._Bot__source_pipeline.receive = lambda: msg
                self.instance.logger.info("Message from cli will be used when processing.")

            if dryrun:
                self.instance.send_message = lambda msg: self.instance.logger.info("DRYRUN: Message would be sent now!")
                self.instance.acknowledge_message = lambda: self.instance.logger.info("DRYRUN: Message would be acknowledged now!")
                print("Dryrun only, no message will be really sent through.")

            self.instance.logger.info("Processing...")
            self.instance.process() # normal run - bot loads and parses its next msg from pipeline

        def _message(self, message_action_kind, msg):
            if message_action_kind == "get":
                self.instance.logger.info("Trying to get the message...")
                msg = self.instance.receive_message()
                print(msg)
            elif message_action_kind == "pop":
                self.instance.logger.info("Trying to pop the message...")
                print(self.instance.receive_message())
                self.instance.acknowledge_message()
            elif message_action_kind == "send":
                if msg:
                    try:
                        msg = Event(json.loads(msg))
                    except:
                        print("Wrong formatted msg.")
                        return
                    self.instance.send_message(msg)
                    self.instance.logger.info("Message send to output pipelines.")
                else:
                    self.instance.logger.info("Message missing!")