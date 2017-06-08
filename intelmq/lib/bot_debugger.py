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
import time
import json
import logging
from os.path import exists
from importlib import import_module

from intelmq.lib import utils
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import StreamHandler
from intelmq.lib.utils import error_message_from_exc


class BotDebugger:

    EXAMPLE = """\nThe message may look like:
    '{"source.network": "178.72.192.0/18", "time.observation": "2017-05-12T05:23:06+00:00"}' """

    load_configuration = utils.load_configuration
    logging_level = "DEBUG"
    init_log_level = {"console": logging.DEBUG, "message": logging.WARNING, "process": logging.INFO, None: logging.INFO}

    def __init__(self, runtime_configuration, bot_id, run_subcommand=None, console_type=None,
                 dryrun=None, message_kind=None, msg=None):
        self.runtime_configuration = runtime_configuration
        self.leverageLogger(level=self.init_log_level[run_subcommand])
        module = import_module(self.runtime_configuration['module'])
        bot = getattr(module, 'BOT')
        if run_subcommand == "message":
            bot.init = lambda *args: None
        self.instance = bot(bot_id)

        if not run_subcommand:
            self.leverageLogger(logging.DEBUG)
            self.instance.start()
        else:
            self.instance._Bot__connect_pipelines()
            if run_subcommand == "console":
                self._console(console_type)
            elif run_subcommand == "message":
                self.leverageLogger(logging.INFO)
                self._message(message_kind, msg)
                return
            elif run_subcommand == "process":
                self.leverageLogger(logging.DEBUG)
                self._process(dryrun, msg)
            else:
                print("Subcommand {} not known.".format(run_subcommand))

    def _console(self, console_type):
        consoles = [console_type, "ipdb", "pudb", "pdb"]
        for console in consoles:
            try:
                module = import_module(console)
            except Exception as exc:
                pass
            else:
                if console_type and console != console_type:
                    print("Console {} not available.".format(console_type))
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
        if message_action_kind == "get":
            self.instance.logger.info("Waiting for a message to get...")
            if not bool(self.instance._Bot__source_queues):
                self.instance.logger.warning("Bot has no source queue.")
                return

            # Never pops from source to internal queue, thx to disabling brpoplpush operation.
            # However, we have to wait manually till there is the message in the queue.
            pl = self.instance._Bot__source_pipeline
            pl.pipe.brpoplpush = lambda source_q, inter_q, i: pl.pipe.lindex(source_q, -1)
            while not (pl.pipe.llen(pl.source_queue) or pl.pipe.llen(pl.internal_queue)):
                time.sleep(1)
            self.pprint(self.instance.receive_message())
        elif message_action_kind == "pop":
            self.instance.logger.info("Waiting for a message to pop...")
            self.pprint(self.instance.receive_message())
            self.instance.acknowledge_message()
        elif message_action_kind == "send":
            if not bool(self.instance._Bot__destination_queues):
                self.instance.logger.warning("Bot has no destination queues.")
                return
            if msg:
                msg = self.arg2msg(msg)
                self.instance.send_message(msg)
                self.instance.logger.info("Message sent to output pipelines.")
            else:
                self.messageWizzard("Message missing!")

    def _process(self, dryrun, msg):
        if msg:
            msg = MessageFactory.serialize(self.arg2msg(msg))
            self.instance._Bot__source_pipeline.receive = lambda: msg
            self.instance.logger.info(" * Message from cli will be used when processing.")

        if dryrun:
            self.instance.send_message = lambda msg: self.instance.logger.info("DRYRUN: Message would be sent now!")
            self.instance.acknowledge_message = lambda: self.instance.logger.info("DRYRUN: Message would be acknowledged now!")
            self.instance.logger.info(" * Dryrun only, no message will be really sent through.")

        self.instance.logger.info("Processing...")
        self.instance.process()

    def arg2msg(self, msg):
        try:
            default_type = "Report" if self.runtime_configuration["group"] is "Parser" else "Event"
            msg = MessageFactory.unserialize(msg, default_type=default_type)
        except (Exception, KeyError, TypeError, ValueError) as exc:
            if exists(msg):
                with open(msg, "r") as f:
                    return self.arg2msg(f.read())
            self.messageWizzard("Message can not be parsed from JSON: {}".format(error_message_from_exc(exc)))
            exit(1)
        return msg

    def leverageLogger(self, level):
        utils.load_configuration = BotDebugger.load_configuration_patch
        BotDebugger.logging_level = level
        if hasattr(self, "instance"):
            self.instance.logger.setLevel(level)
            for h in self.instance.logger.handlers:
                if isinstance(h, StreamHandler):
                    h.setLevel(level)

    @staticmethod
    def load_configuration_patch(*args, ** kwargs):
        d = BotDebugger.load_configuration(*args, ** kwargs)
        if "logging_level" in d:
            d["logging_level"] = BotDebugger.logging_level
        return d

    def messageWizzard(self, msg):
        self.instance.logger.error(msg)
        print(self.EXAMPLE)
        if input("Do you want to display current harmonization (available fields)? y/[n]: ") is "y":
            self.pprint(self.instance.harmonization)

    @staticmethod
    def pprint(msg):
        """ We can't use standard pprint as JSON standard asks for double quotes. """
        print(json.dumps(msg, indent=4, sort_keys=True))
