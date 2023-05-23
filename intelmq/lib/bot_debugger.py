# SPDX-FileCopyrightText: 2017 Edvard Rejthar
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
import json
import sys
from importlib import import_module
from os.path import exists

import time

from intelmq import RUNTIME_CONF_FILE
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.message import MessageFactory
from intelmq.lib.pipeline import Pipeline
from intelmq.lib.utils import StreamHandler, error_message_from_exc


class BotDebugger:
    EXAMPLE = """\nThe message may look like:
    '{"source.network": "178.72.192.0/18", "time.observation": "2017-05-12T05:23:06+00:00"}' """

    load_configuration = utils.load_configuration
    logging_level = None
    output = []
    instance = None

    def __init__(self, runtime_configuration, bot_id, run_subcommand=None, console_type=None,
                 message_kind=None, dryrun=None, msg=None, show=None, loglevel=None):
        self.runtime_configuration = runtime_configuration
        self.bot_id = bot_id
        self.run_subcommand = run_subcommand
        self.console_type = console_type
        self.message_kind = message_kind
        self.dryrun = dryrun
        self.msg = msg
        self.show = show
        module = import_module(self.runtime_configuration['module'])

        if loglevel:
            self.leverageLogger(loglevel)
        elif run_subcommand == "console":
            self.leverageLogger("DEBUG")

        bot = getattr(module, 'BOT')
        if run_subcommand == "message":
            bot.init = lambda *args, **kwargs: None

        if self.logging_level:
            # Set's the bot's default and initial value for the logging_level to the value we want
            bot.logging_level = self.logging_level

        self.instance = bot(bot_id, disable_multithreading=True,
                            standalone=True,  # instruct the bot to call SystemExit exception at the end or in case of errors
                            )

    def run(self) -> str:
        if not self.run_subcommand:
            self.instance.start()
        else:
            self.instance._Bot__connect_pipelines()
            if self.run_subcommand == "console":
                self._console(self.console_type)
            elif self.run_subcommand == "message":
                self._message(self.message_kind, self.msg)
            elif self.run_subcommand == "process":
                self._process(self.dryrun, self.msg, self.show)
            else:
                self.outputappend(f"Subcommand {self.run_subcommand} not known.")

        return '\n'.join(self.output) or ""

    def _console(self, console_type):
        consoles = [console_type, "ipdb", "pudb", "pdb"]
        for console in consoles:
            try:
                module = import_module(console)
            except Exception:
                pass
            else:
                if console_type and console != console_type:
                    print(f"Console {console_type} not available.")
                print("*** Using console {}. Please use 'self' to access to the bot instance properties."
                      "You may exit the console by 'c' command (like continue). ***"
                      .format(module.__name__))
                break
        else:
            print("Can't run console.")
            return

        self = self.instance
        module.set_trace()

    def _message(self, message_action_kind, msg):
        if message_action_kind == "send":
            if self.instance.group == "Output":
                self.outputappend("Output bots can't send message.")
                return
            if not bool(self.instance.destination_queues):
                self.outputappend("Bot has no destination queues.")
                return
            if msg:
                msg = self.arg2msg(msg)
                self.instance.send_message(msg)
                self.outputappend("Message sent to output pipelines.")
            else:
                self.messageWizzard("Message missing!")
        elif self.instance.group == "Collector":
            self.outputappend("Collector bots have no input queue.")
        elif message_action_kind == "get":
            self.outputappend("Waiting for a message to get...")
            if not self.instance.source_queue:
                self.outputappend("Bot has no source queue.")
                return

            # Never pops from source to internal queue, thx to disabling brpoplpush operation.
            # However, we have to wait manually till there is the message in the queue.
            pl = self.instance._Bot__source_pipeline
            pl.pipe.brpoplpush = lambda source_q, inter_q, i: pl.pipe.lindex(source_q, -1)
            while not (pl.pipe.llen(pl.source_queue) or pl.pipe.llen(pl.internal_queue)):
                time.sleep(1)
            self.outputappend(self.pprint(self.instance.receive_message()))
        elif message_action_kind == "pop":
            self.instance.logger.info("Waiting for a message to pop...")
            self.outputappend(self.pprint(self.instance.receive_message()))
            self.instance.acknowledge_message()

    def _process(self, dryrun, msg, show):
        if msg:
            msg = MessageFactory.serialize(self.arg2msg(msg))
            if not self.instance._Bot__source_pipeline:
                # is None if source pipeline does not exist
                self.instance._Bot__source_pipeline = Pipeline(None)
            self.instance._Bot__source_pipeline.receive = lambda *args, **kwargs: msg
            self.instance._Bot__source_pipeline.acknowledge = lambda *args, **kwargs: None
            self.outputappend(" * Message from cli will be used when processing.")

        if dryrun:
            self.instance.send_message = lambda *args, **kwargs: self.outputappend(
                "DRYRUN: Message would be sent now to %r!" % kwargs.get('path', "_default"))
            self.instance.acknowledge_message = lambda *args, **kwargs: self.outputappend(
                "DRYRUN: Message would be acknowledged now!")
            self.outputappend(" * Dryrun only, no message will be really sent through.")

        if show:
            fn = self.instance.send_message
            self.instance.send_message = lambda *args, **kwargs: [self.outputappend(self.pprint(args or "No message generated")),
                                                                  fn(*args, **kwargs)]

        self.outputappend("Processing...")
        self.instance.process()

    def outputappend(self, msg):
        self.output.append(msg)

    def arg2msg(self, msg):
        default_type = "Report" if (self.runtime_configuration.get("group", None) == "Parser" or isinstance(self.instance, ParserBot)) else "Event"
        try:
            msg = MessageFactory.unserialize(msg, default_type=default_type)
        except (Exception, KeyError, TypeError, ValueError) as exc:
            if exists(msg):
                with open(msg) as f:
                    return self.arg2msg(f.read())
            self.messageWizzard(f"Message can not be parsed from JSON: {error_message_from_exc(exc)}")
            sys.exit(1)
        return msg

    def leverageLogger(self, level):
        utils.load_configuration = BotDebugger.load_configuration_patch
        self.logging_level = level
        if self.instance:
            self.instance.logger.setLevel(level)
            for h in self.instance.logger.handlers:
                if isinstance(h, StreamHandler):
                    h.setLevel(level)

    @staticmethod
    def load_configuration_patch(configuration_filepath: str, *args, **kwargs) -> dict:
        """
        Mock function for utils.load_configuration which ensures the logging level parameter is set to the value we want.
        If Runtime configuration is detected, the logging_level parameter is
        - inserted in all bot's parameters. bot_id is not accessible here, hence we add it everywhere
        - inserted in the global parameters (ex-defaults).
        Maybe not everything is necessary, but we can make sure the logging_level is just everywhere where it might be relevant, also in the future.
        """
        config = BotDebugger.load_configuration(configuration_filepath=configuration_filepath, *args, **kwargs)
        if BotDebugger.logging_level and configuration_filepath == RUNTIME_CONF_FILE:
            for bot_id in config.keys():
                if bot_id == "global":
                    config[bot_id]["logging_level"] = BotDebugger.logging_level
                else:
                    config[bot_id]['parameters']["logging_level"] = BotDebugger.logging_level
            if "global" not in config:
                config["global"] = {"logging_level": BotDebugger.logging_level}
        return config

    def messageWizzard(self, msg):
        self.instance.logger.error(msg)
        print(self.EXAMPLE)
        if input("Do you want to display current harmonization (available fields)? y/[n]: ") == "y":
            print(self.pprint(self.instance.harmonization))

    @staticmethod
    def pprint(msg) -> str:
        """ We can't use standard pprint as JSON standard asks for double quotes. """
        return json.dumps(msg, indent=4, sort_keys=True)

    def __del__(self):
        # prevents a SystemExit Exception at object deletion
        # remove once PR#2358 (library mode) is merged
        if self.instance:
            setattr(self.instance, 'testing', True)
