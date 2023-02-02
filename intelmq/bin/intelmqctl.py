# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import argparse
import datetime
import importlib
import json
import logging
import os
import re
import subprocess
import sys
import textwrap
import traceback
import time

import pkg_resources
from ruamel.yaml import YAML

from intelmq import (DEFAULT_LOGGING_LEVEL,  # noqa: F401
                     HARMONIZATION_CONF_FILE,
                     RUNTIME_CONF_FILE, VAR_RUN_PATH, STATE_FILE_PATH,
                     DEFAULT_LOGGING_PATH, __version_info__,
                     CONFIG_DIR, ROOT_DIR)
from intelmq.lib import utils
from intelmq.lib.datatypes import ReturnType, MESSAGES, LogLevel
from intelmq.lib.processmanager import *
from intelmq.lib.pipeline import PipelineFactory
import intelmq.lib.upgrades as upgrades

yaml = YAML(typ="safe", pure=True)

try:
    import psutil
except ImportError:
    psutil = None


class Parameters:
    pass


STATUSES = {
    'starting': 0,
    'running': 1,
    'stopping': 2,
    'stopped': 3,
}

BOT_GROUP = {"collectors": "Collector", "parsers": "Parser", "experts": "Expert", "outputs": "Output"}


class IntelMQController():
    _returntype: ReturnType = ReturnType.PYTHON
    _quiet: bool = False
    _logger: logging.Logger
    _processmanagertype = "intelmq"
    _processmanager = None
    _interactive = False
    _logging_level = DEFAULT_LOGGING_LEVEL
    _parameters = Parameters()
    _runtime_configuration: dict = {}

    def __init__(self, interactive: bool = False, returntype: ReturnType = ReturnType.PYTHON, quiet: bool = False,
                 no_file_logging: bool = False, drop_privileges: bool = True) -> None:
        """
        Initializes intelmqctl.

        Parameters:
            interactive: for cli-interface true, functions can exits, parameters are used
            return_type:
            * ReturnType.PYTHON: no special treatment, can be used for use by other python code
            * ReturnType.TEXT: user-friendly output for cli, default for interactive use
            * ReturnType.JSON: machine-readable output for managers
            quiet: False by default, can be activated for cron jobs etc.
            no_file_logging: do not log to the log file
            drop_privileges: Drop privileges and fail if it did not work.
        """
        self._interactive = interactive
        self._returntype = returntype
        self._quiet = quiet

        # set default values for the logging handler
        self._parameters.logging_handler = 'file'
        self._parameters.logging_path = DEFAULT_LOGGING_PATH

        # Try to get logging_level from defaults configuration, else use default (defined above)
        defaults_loading_exc = None
        try:
            self.load_defaults_configuration()
        except Exception as exc:
            defaults_loading_exc = exc
            logging_level_stream = 'DEBUG'
        else:
            self._logging_level = getattr(self, 'logging_level', DEFAULT_LOGGING_LEVEL).upper()
        # make sure that logging_level_stream is always at least INFO or more verbose
        # otherwise the output on stdout/stderr is less than the user expects
        logging_level_stream = self._logging_level if self._logging_level == 'DEBUG' else 'INFO'

        if drop_privileges and not utils.drop_privileges():
            self.abort('IntelMQ must not run as root. Dropping privileges did not work.')

        try:
            if no_file_logging:
                raise FileNotFoundError('Logging to file disabled.')
            self._logger = utils.log('intelmqctl', log_level=self._logging_level,
                                     log_format_stream=utils.LOG_FORMAT_SIMPLE,
                                     logging_level_stream=logging_level_stream,
                                     log_max_size=getattr(self._parameters, "logging_max_size", 0),
                                     log_max_copies=getattr(self._parameters, "logging_max_copies", None))
        except (FileNotFoundError, PermissionError) as exc:
            self._logger = utils.log('intelmqctl', log_level=self._logging_level, log_path=False,
                                     log_format_stream=utils.LOG_FORMAT_SIMPLE,
                                     logging_level_stream=logging_level_stream)
            if not isinstance(exc, FileNotFoundError) and exc.args[0] != 'Logging to file disabled.':
                self._logger.error('Not logging to file: %s', exc)
        if defaults_loading_exc:
            self._logger.exception('Loading the defaults configuration failed!', exc_info=defaults_loading_exc)

        APPNAME = "intelmqctl"
        try:
            VERSION = pkg_resources.get_distribution("intelmq").version
        except pkg_resources.DistributionNotFound:  # pragma: no cover
            # can only happen in interactive mode
            self._logger.error('No valid IntelMQ installation found: DistributionNotFound')
            sys.exit(1)
        DESCRIPTION = """
        description: intelmqctl is the tool to control intelmq system.

        Outputs are logged to %s/intelmqctl.log""" % DEFAULT_LOGGING_PATH
        EPILOG = '''
        intelmqctl [start|stop|restart|status|reload] --group [collectors|parsers|experts|outputs]
        intelmqctl [start|stop|restart|status|reload] bot-id
        intelmqctl [start|stop|restart|status|reload]
        intelmqctl list [bots|queues|queues-and-status]
        intelmqctl log bot-id [number-of-lines [log-level]]
        intelmqctl run bot-id message [get|pop|send]
        intelmqctl run bot-id process [--msg|--dryrun]
        intelmqctl run bot-id console
        intelmqctl clear queue-id
        intelmqctl check
        intelmqctl upgrade-config
        intelmqctl debug

Starting a bot:
    intelmqctl start bot-id
Stopping a bot:
    intelmqctl stop bot-id
Reloading a bot:
    intelmqctl reload bot-id
Restarting a bot:
    intelmqctl restart bot-id
Get status of a bot:
    intelmqctl status bot-id

Run a bot directly for debugging purpose and temporarily leverage the logging level to DEBUG:
    intelmqctl run bot-id
Get a pdb (or ipdb if installed) live console.
    intelmqctl run bot-id console
See the message that waits in the input queue.
    intelmqctl run bot-id message get
See additional help for further explanation.
    intelmqctl run bot-id --help

Starting the botnet (all bots):
    intelmqctl start
    etc.

Starting a group of bots:
    intelmqctl start --group experts
    etc.

Get a list of all configured bots:
    intelmqctl list bots
If -q is given, only the IDs of enabled bots are listed line by line.

Get a list of all queues:
    intelmqctl list queues
If -q is given, only queues with more than one item are listed.

Get a list of all queues and status of the bots:
    intelmqctl list queues-and-status

Clear a queue:
    intelmqctl clear queue-id

Get logs of a bot:
    intelmqctl log bot-id number-of-lines log-level
Reads the last lines from bot log.
Log level should be one of DEBUG, INFO, ERROR or CRITICAL.
Default is INFO. Number of lines defaults to 10, -1 gives all. Result
can be longer due to our logging format!

Upgrade from a previous version:
    intelmqctl upgrade-config
Make a backup of your configuration first, also including bot's configuration files.

Get some debugging output on the settings and the environment (to be extended):
    intelmqctl debug --get-paths
    intelmqctl debug --get-environment-variables
'''

        try:
            self._runtime_configuration = utils.load_configuration(RUNTIME_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort(f'Error loading {RUNTIME_CONF_FILE!r}: {exc}')

        self._processmanagertype = getattr(self._parameters, 'process_manager', 'intelmq')
        if self._processmanagertype not in process_managers():
            self.abort('Invalid process manager given: %r, should be one of %r.' '' % (self._processmanagertype, list(process_managers().keys())))

        if self._interactive:
            parser = argparse.ArgumentParser(
                prog=APPNAME,
                description=DESCRIPTION,
                epilog=EPILOG,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )

            parser.add_argument('--version', '-v', action='version', version=VERSION)
            parser.add_argument('--type', '-t', choices=[i.name.lower() for i in ReturnType], default='text', help='choose if it should return regular text or other machine-readable')
            parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode, useful for reloads initiated scripts like logrotate')

            subparsers = parser.add_subparsers(title='subcommands')

            parser_list = subparsers.add_parser('list', help='Listing bots or queues')
            parser_list.add_argument('kind', choices=['bots', 'queues', 'queues-and-status'])
            parser_list.add_argument('--non-zero', '--quiet', '-q', action='store_true',
                                     help='Only list non-empty queues '
                                          'or the IDs of enabled bots.')
            parser_list.add_argument('--count', '--sum', '-s', action='store_true',
                                     help='Only show the total '
                                          'number of messages in queues. '
                                          'Only valid for listing queues.')
            parser_list.add_argument('--configured', '-c', action='store_true',
                                     help='Only show configured bots')
            parser_list.set_defaults(func=self.list)

            parser_clear = subparsers.add_parser('clear', help='Clear a queue')
            parser_clear.add_argument('queue', help='queue name')
            parser_clear.set_defaults(func=self.clear_queue)

            parser_log = subparsers.add_parser('log', help='Get last log lines of a bot')
            parser_log.add_argument('bot_id', help='bot id', choices=self._configured_bots_list())
            parser_log.add_argument('number_of_lines', help='number of lines',
                                    default=10, type=int, nargs='?')
            parser_log.add_argument('log_level', help='logging level', choices=[i.name for i in LogLevel], default='INFO', nargs='?')
            parser_log.set_defaults(func=self.read_bot_log)

            parser_run = subparsers.add_parser('run', help='Run a bot interactively')
            parser_run.add_argument('bot_id', choices=self._configured_bots_list())
            parser_run.add_argument('--loglevel', '-l', nargs='?', default=None, choices=[i.name for i in LogLevel])
            parser_run_subparsers = parser_run.add_subparsers(title='run-subcommands')

            parser_run_console = parser_run_subparsers.add_parser('console', help='Get a ipdb live console.')
            parser_run_console.add_argument('console_type', nargs='?',
                                            help='You may specify which console should be run. Default is ipdb (if installed)'
                                                 ' or pudb (if installed) or pdb but you may want to use another one.')
            parser_run_console.set_defaults(run_subcommand="console")

            parser_run_message = parser_run_subparsers.add_parser('message',
                                                                  help='Debug bot\'s pipelines. Get the message in the'
                                                                       ' input pipeline, pop it (cut it) and display it, or'
                                                                       ' send the message directly to bot\'s output pipeline(s).')
            parser_run_message.add_argument('message_action_kind',
                                            choices=["get", "pop", "send"],
                                            help='get: show the next message in the source pipeline. '
                                                 'pop: show and delete the next message in the source pipeline '
                                                 'send: Send the given message to the destination pipeline(s).')
            parser_run_message.add_argument('msg', nargs='?', help='If send was chosen, put here the message in JSON.')
            parser_run_message.set_defaults(run_subcommand="message")

            parser_run_process = parser_run_subparsers.add_parser('process', help='Single run of bot\'s process() method.')
            parser_run_process.add_argument('--show-sent', '-s', action='store_true',
                                            help='If message is sent through, displays it.')
            parser_run_process.add_argument('--dryrun', '-d', action='store_true',
                                            help='Never really pop the message from the input pipeline '
                                                 'nor send to output pipeline.')
            parser_run_process.add_argument('--msg', '-m',
                                            help='Trick the bot to process this JSON '
                                                 'instead of the Message in its pipeline.')
            parser_run_process.set_defaults(run_subcommand="process")
            parser_run.set_defaults(func=self.bot_run)

            parser_check = subparsers.add_parser('check',
                                                 help='Check installation and configuration')
            parser_check.add_argument('--quiet', '-q', action='store_true',
                                      help='Only print warnings and errors.')
            parser_check.add_argument('--no-connections', '-C', action='store_true',
                                      help='Do not test the connections to services like redis.')
            parser_check.set_defaults(func=self.check)

            parser_help = subparsers.add_parser('help',
                                                help='Show the help')
            parser_help.set_defaults(func=parser.print_help)

            parser_start = subparsers.add_parser('start', help='Start a bot or botnet')
            parser_start.add_argument('bot_id', nargs='?',
                                      choices=self._configured_bots_list())
            parser_start.add_argument('--group', help='Start a group of bots',
                                      choices=BOT_GROUP.keys())
            parser_start.set_defaults(func=self.bot_start)

            parser_stop = subparsers.add_parser('stop', help='Stop a bot or botnet')
            parser_stop.add_argument('bot_id', nargs='?',
                                     choices=self._configured_bots_list())
            parser_stop.add_argument('--group', help='Stop a group of bots',
                                     choices=BOT_GROUP.keys())
            parser_stop.set_defaults(func=self.bot_stop)

            parser_restart = subparsers.add_parser('restart', help='Restart a bot or botnet')
            parser_restart.add_argument('bot_id', nargs='?',
                                        choices=self._configured_bots_list())
            parser_restart.add_argument('--group', help='Restart a group of bots',
                                        choices=BOT_GROUP.keys())
            parser_restart.set_defaults(func=self.bot_restart)

            parser_reload = subparsers.add_parser('reload', help='Reload a bot or botnet')
            parser_reload.add_argument('bot_id', nargs='?',
                                       choices=self._configured_bots_list())
            parser_reload.add_argument('--group', help='Reload a group of bots',
                                       choices=BOT_GROUP.keys())
            parser_reload.set_defaults(func=self.bot_reload)

            parser_status = subparsers.add_parser('status', help='Status of a bot or botnet')
            parser_status.add_argument('bot_id', nargs='?',
                                       choices=self._configured_bots_list())
            parser_status.add_argument('--group', help='Get status of a group of bots',
                                       choices=BOT_GROUP.keys())
            parser_status.set_defaults(func=self.bot_status)

            parser_status = subparsers.add_parser('enable', help='Enable a bot')
            parser_status.add_argument('bot_id',
                                       choices=self._configured_bots_list())
            parser_status.set_defaults(func=self.bot_enable)

            parser_status = subparsers.add_parser('disable', help='Disable a bot')
            parser_status.add_argument('bot_id',
                                       choices=self._configured_bots_list())
            parser_status.set_defaults(func=self.bot_disable)

            parser_upgrade_conf = subparsers.add_parser('upgrade-config',
                                                        help='Upgrade IntelMQ configuration to a newer version.')
            parser_upgrade_conf.add_argument('-p', '--previous',
                                             help='Use this version as the previous one.')
            parser_upgrade_conf.add_argument('-d', '--dry-run',
                                             action='store_true', default=False,
                                             help='Do not write any files.')
            parser_upgrade_conf.add_argument('-u', '--function',
                                             help='Run this upgrade function.',
                                             choices=upgrades.__all__)
            parser_upgrade_conf.add_argument('-f', '--force',
                                             action='store_true',
                                             help='Force running the upgrade procedure.')
            parser_upgrade_conf.add_argument('--state-file',
                                             help='The state file location to use.',
                                             default=STATE_FILE_PATH)
            parser_upgrade_conf.add_argument('--no-backup',
                                             help='Do not create backups of state and configuration files.',
                                             action='store_true')
            parser_upgrade_conf.set_defaults(func=self.upgrade_conf)

            parser_debug = subparsers.add_parser('debug', help='Get debugging output.')
            parser_debug.add_argument('--get-paths', help='Give all paths',
                                      action='append_const', dest='sections',
                                      const='paths')
            parser_debug.add_argument('--get-environment-variables',
                                      help='Give environment variables',
                                      action='append_const', dest='sections',
                                      const='environment_variables')
            parser_debug.set_defaults(func=self.debug)

            self.parser = parser
        else:
            self._processmanager = process_managers()[self._processmanagertype](
                self._interactive,
                self._runtime_configuration,
                self._logger,
                self._returntype,
                self._quiet
            )

    def load_defaults_configuration(self, silent=False):
        for option, value in utils.get_global_settings().items():
            setattr(self._parameters, option, value)

        # copied from intelmq.lib.bot, should be refactored to e.g. intelmq.lib.config
        intelmq_environment = [elem for elem in os.environ if elem.startswith('INTELMQ_')]
        for elem in intelmq_environment:
            option = elem[8:].lower()
            value = os.environ[elem]
            # do some conversions:
            if value == 'True':
                value = True
            elif value == 'False':
                value = False
            elif value.isnumeric():
                value = int(value)

            setattr(self._parameters, option, value)

    def run(self):
        results = None
        args = self.parser.parse_args()
        if 'func' not in args:
            sys.exit(self.parser.print_help())
        args_dict = vars(args).copy()

        self._quiet = args.quiet
        self._returntype = ReturnType[args.type.upper()]
        del args_dict['type'], args_dict['quiet'], args_dict['func']

        self._logging_level = 'WARNING' if self._quiet else 'INFO'
        self._logger.setLevel(self._logging_level)

        # initialize the processmanager
        # this has to happen *after* we set `_quiet` and `_returntype` using values from argv
        self._processmanager = process_managers()[self._processmanagertype](
            self._interactive,
            self._runtime_configuration,
            self._logger,
            self._returntype,
            self._quiet
        )

        retval, results = args.func(**args_dict)

        if self._returntype is ReturnType.JSON:
            print(json.dumps(results, indent=4))

        return retval

    def bot_run(self, **kwargs):
        # the bot_run method is special in that it mixes plain text
        # and json in its output, therefore it is printed here
        # and not in the calling `run` method.
        retval, results = self._processmanager.bot_run(**kwargs)
        print(results)
        return retval, None

    def bot_start(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_start(group=group)
        else:
            status = self._processmanager.bot_start(bot_id, getstatus)
            if status in ['running']:
                return 0, status
            else:
                return 1, status

    def bot_stop(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_stop(group=group)
        else:
            status = self._processmanager.bot_stop(bot_id, getstatus)
            if status in ['stopped', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_reload(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_reload(group=group)
        else:
            if self._processmanager.bot_status(bot_id) == 'disabled':
                return 0, 'disabled'
            status = self._processmanager.bot_reload(bot_id, getstatus)
            if status in ['running', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_restart(self, bot_id, group=None):
        if bot_id is None:
            return self.botnet_restart(group=group)
        else:
            status_stop = self.bot_stop(bot_id)
            # Exit if stopping the bot did not work, #1434
            if status_stop[0] != 0:
                return status_stop

            status_start = self.bot_start(bot_id)
            return status_stop[0] | status_start[0], [status_stop[1], status_start[1]]

    def bot_status(self, bot_id, group=None):
        if bot_id is None:
            return self.botnet_status(group=group)
        else:
            status = self._processmanager.bot_status(bot_id)
            if status in ['running', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_enable(self, bot_id):
        if self._is_enabled(bot_id):
            self.log_bot_message('enabled', bot_id)
        else:
            self.log_bot_message('enabling', bot_id)
            self._runtime_configuration[bot_id]['enabled'] = True
            self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def bot_disable(self, bot_id):
        """
        If Bot is already disabled, the "Bot ... is disabled" message is
        printed by the wrapping function already.
        """
        if self._is_enabled(bot_id):
            self.log_bot_message('disabling', bot_id)
            self._runtime_configuration[bot_id]['enabled'] = False
            self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def _is_enabled(self, bot_id):
        return self._runtime_configuration[bot_id].get('enabled', True)

    def _configured_bots_list(self, group=None):
        if group is not None:
            bots = sorted(k_v[0] for k_v in filter(lambda bot: bot[0] != 'global' and bot[1]["group"] == BOT_GROUP[group], self._runtime_configuration.items()))
        else:
            bots = sorted(self._runtime_configuration.keys())
        if 'global' in bots:
            bots.remove('global')
        return bots

    def botnet_start(self, group=None):
        botnet_status = {}
        self.log_botnet_message('starting', group)

        bots = self._configured_bots_list(group=group)

        for bot_id in bots:
            if self._runtime_configuration[bot_id].get('enabled', True):
                self.bot_start(bot_id, getstatus=False)
            else:
                self.log_bot_message('disabled', bot_id)
                botnet_status[bot_id] = 'disabled'

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            if self._runtime_configuration[bot_id].get('enabled', True):
                botnet_status[bot_id] = self.bot_status(bot_id)[1]
                if botnet_status[bot_id] not in ['running', 'disabled']:
                    retval = 1
                    if self._returntype is ReturnType.TEXT:
                        print(bot_id, botnet_status[bot_id])

        self.log_botnet_message('running', group)
        return retval, botnet_status

    def botnet_stop(self, group=None):
        botnet_status = {}
        self.log_botnet_message('stopping', group)

        bots = self._configured_bots_list(group=group)

        for bot_id in bots:
            self.bot_stop(bot_id, getstatus=False)

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['stopped', 'disabled']:
                retval = 1

        self.log_botnet_message('stopped', group)
        return retval, botnet_status

    def botnet_reload(self, group=None):
        botnet_status = {}
        self.log_botnet_message('reloading', group)

        bots = sorted(self._configured_bots_list(group=group))
        for bot_id in bots:
            self.bot_reload(bot_id, getstatus=False)

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['running', 'disabled']:
                retval = 1
        self.log_botnet_message('reloaded', group)
        return retval, botnet_status

    def botnet_restart(self, group=None):
        self.log_botnet_message('restarting')
        retval_stop, _ = self.botnet_stop(group=group)
        retval_start, status = self.botnet_start(group=group)
        if retval_stop > retval_start:  # In case the stop operation was not successful, exit 1
            retval_start = retval_stop
        return retval_start, status

    def botnet_status(self, group=None):
        retval = 0
        botnet_status = {}
        bots = sorted(self._configured_bots_list(group=group))
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['running', 'disabled']:
                retval = 1
        return retval, botnet_status

    def list(self, kind=None, non_zero=False, count=False, configured=False):
        if kind == 'queues':
            return self.list_queues(non_zero=non_zero, count=count)
        elif kind == 'bots':
            return self.list_bots(non_zero=non_zero, configured=configured)
        elif kind == 'queues-and-status':
            q = self.list_queues()
            b = self.botnet_status()
            return q[0] | b[0], [q[1], b[1]]

    def abort(self, message):
        if self._interactive:
            sys.exit(message)
        else:
            raise ValueError(message)

    def write_updated_runtime_config(self, filename=RUNTIME_CONF_FILE):
        try:
            utils.write_configuration(filename, self._runtime_configuration)
        except PermissionError:
            self.abort('Can\'t update runtime configuration: Permission denied.')
        return True

    def list_bots(self, non_zero=False, configured=False):
        """
        Lists all (configured) bots from runtime configuration or generated on demand
        with bot id/module and description and parameters.

        If description is not set, None is used instead.
        """
        if configured:
            if self._returntype is ReturnType.TEXT:
                for bot_id in self._configured_bots_list():
                    if non_zero and not self._runtime_configuration[bot_id].get('enabled'):
                        continue
                    if self._quiet:
                        print(bot_id)
                    else:
                        print("Bot ID: {}\nDescription: {}"
                              "".format(bot_id, self._runtime_configuration[bot_id].get('description')))
            return 0, [{'id': bot_id,
                        'description': self._runtime_configuration[bot_id].get('description')}
                       for bot_id in sorted(self._configured_bots_list())]
        else:
            bots = utils.list_all_bots()
            if self._returntype is ReturnType.TEXT:
                for bot_type in bots:
                    print(f"\n======== {bot_type} ========\n")
                    for bot in bots[bot_type]:
                        print("Bot ID: {}\nDescription: {}"
                              "".format(bot, bots[bot_type][bot].get('description')))
            return 0, bots

    def _pipeline_configuration(self):
        pipeline_configuration = {}
        for botid, botconfig in self._runtime_configuration.items():
            if botid != 'global':
                pipeline_configuration[botid] = {"source_queue": f"{botid}-queue", "destination_queues": []}
                if 'parameters' in botconfig:
                    if 'source_queue' in botconfig['parameters']:
                        pipeline_configuration[botid]['source_queue'] = botconfig['parameters']['source_queue']
                    if 'destination_queues' in botconfig['parameters']:
                        pipeline_configuration[botid]['destination_queues'] = botconfig['parameters']['destination_queues']
        return pipeline_configuration

    def get_queues(self, with_internal_queues=False):
        """
        :return: 4-tuple of source, destination, internal queues, and all queues combined.
        The returned values are only queue names, not their paths. I.E. if there is a bot with
        destination queues = {"_default": "one", "other": ["two", "three"]}, only set of {"one", "two", "three"} gets returned.
        (Note that the "_default" path has single string and the "other" path has a list that gets flattened.)
        """
        source_queues = set()
        destination_queues = set()
        internal_queues = set()

        for botid, value in self._pipeline_configuration().items():
            if 'source_queue' in value:
                source_queues.add(value['source_queue'])
                if with_internal_queues:
                    internal_queues.add(value['source_queue'] + '-internal')
            if 'destination_queues' in value:
                # flattens ["one", "two"] → {"one", "two"}, {"_default": "one", "other": ["two", "three"]} → {"one", "two", "three"}
                destination_queues.update(utils.flatten_queues(value['destination_queues']))

        all_queues = source_queues.union(destination_queues).union(internal_queues)

        return source_queues, destination_queues, internal_queues, all_queues

    def list_queues(self, non_zero=False, count=False):
        pipeline = PipelineFactory.create(logger=self._logger, pipeline_args=self._parameters.__dict__)
        pipeline.set_queues(None, "source")
        pipeline.connect()
        source_queues, destination_queues, internal_queues,\
            all_queues = self.get_queues(with_internal_queues=pipeline.has_internal_queues)

        counters = pipeline.count_queued_messages(*all_queues)
        pipeline.disconnect()
        if self._returntype is ReturnType.TEXT:
            for queue, counter in sorted(counters.items(), key=lambda x: str.lower(x[0])):
                if (counter or not non_zero) and not count:
                    self._logger.info("%s - %s", queue, counter)
            if count:
                self._logger.info("%s", sum(counters.values()))

        return_dict = {}
        if count:
            return_dict = {'total-messages': sum(counters.values())}
        else:
            for bot_id, info in self._pipeline_configuration().items():
                return_dict[bot_id] = {}

                # Do not report source queues for collectors
                if 'source_queue' in info and not (
                        self._runtime_configuration[bot_id].get('group', None) == 'Collector' or
                        self._runtime_configuration[bot_id].get('groupname', None) == 'collectors'):
                    return_dict[bot_id]['source_queue'] = (
                        info['source_queue'], counters[info['source_queue']])
                    if pipeline.has_internal_queues:
                        return_dict[bot_id]['internal_queue'] = counters[info['source_queue'] + '-internal']

                if 'destination_queues' in info:
                    return_dict[bot_id]['destination_queues'] = []
                    for dest_queue in utils.flatten_queues(info['destination_queues']):
                        return_dict[bot_id]['destination_queues'].append((dest_queue, counters[dest_queue]))

        return 0, return_dict

    def clear_queue(self, queue):
        """
        Clears an exiting queue.

        First checks if the queue does exist in the pipeline configuration.
        """
        pipeline = PipelineFactory.create(logger=self._logger, pipeline_args=self._parameters.__dict__)
        pipeline.set_queues(None, "source")
        pipeline.connect()

        if self._returntype is ReturnType.TEXT:
            self._logger.info("Clearing queue %s.", queue)
        queues = set()
        for key, value in self._pipeline_configuration().items():
            if 'source_queue' in value:
                queues.add(value['source_queue'])
                if pipeline.has_internal_queues:
                    queues.add(value['source_queue'] + '-internal')
            if 'destination_queues' in value:
                queues.update(value['destination_queues'])

        if queue not in queues:
            if self._returntype is ReturnType.TEXT:
                self._logger.error("Queue %s does not exist!", queue)
            return 2, 'not-found'

        try:
            pipeline.clear_queue(queue)
            if self._returntype is ReturnType.TEXT:
                self._logger.info("Successfully cleared queue %s.", queue)
            return 0, 'success'
        except Exception:  # pragma: no cover
            self._logger.exception("Error while clearing queue %s.", queue)
            return 1, 'error'

    def read_bot_log(self, bot_id, log_level, number_of_lines):
        if self._parameters.logging_handler == 'file':
            bot_log_path = os.path.join(self._parameters.logging_path,
                                        bot_id + '.log')
            if not os.path.isfile(bot_log_path):
                message = {'date': datetime.datetime.now().isoformat(), "bot_id": bot_id, "log_level": "INFO", "message": 'No log file exists (yet).'}
                self.log_log_messages([message])
                return 0, [message]
        elif self._parameters.logging_handler == 'syslog':
            bot_log_path = '/var/log/syslog'
        else:
            self.abort("Unknown logging handler %r" % self._parameters.logging_handler)

        if not os.access(bot_log_path, os.R_OK):
            self._logger.error('File %r is not readable.', bot_log_path)
            return 1, 'error'

        messages = []

        message_overflow = ''
        message_count = 0

        for line in utils.reverse_readline(bot_log_path):
            if self._parameters.logging_handler == 'file':
                log_message = utils.parse_logline(line)
            if self._parameters.logging_handler == 'syslog':
                log_message = utils.parse_logline(line, regex=utils.SYSLOG_REGEX)

            if type(log_message) is not dict:
                if self._parameters.logging_handler == 'file':
                    message_overflow = '\n'.join([line, message_overflow])
                continue
            if log_message['bot_id'] != bot_id:
                continue
            if LogLevel[log_message['log_level']].value > LogLevel[log_level].value:
                continue

            if message_overflow:
                log_message['extended_message'] = message_overflow
                message_overflow = ''

            if self._parameters.logging_handler == 'syslog':
                log_message['message'] = log_message['message'].replace('#012', '\n')

            message_count += 1
            messages.append(log_message)

            if message_count >= number_of_lines and number_of_lines != -1:
                break

        self.log_log_messages(messages[::-1])
        return 0, messages[::-1]

    def check(self, no_connections=False, check_executables=True):
        retval = 0
        if self._returntype is ReturnType.JSON:
            check_logger, list_handler = utils.setup_list_logging(name='check', logging_level=self._logging_level)
        else:
            check_logger = self._logger

        # loading files and syntax check
        files = {RUNTIME_CONF_FILE: None, HARMONIZATION_CONF_FILE: None}
        check_logger.info('Reading configuration files.')
        try:
            with open(HARMONIZATION_CONF_FILE) as file_handle:
                files[HARMONIZATION_CONF_FILE] = json.load(file_handle)
        except (OSError, ValueError) as exc:  # pragma: no cover
            check_logger.error('Could not load %r: %s.', HARMONIZATION_CONF_FILE, exc)
            retval = 1
        try:
            with open(RUNTIME_CONF_FILE) as file_handle:
                files[RUNTIME_CONF_FILE] = yaml.load(file_handle)
        except (OSError, ValueError) as exc:
            check_logger.error('Could not load %r: %s.', RUNTIME_CONF_FILE, exc)
            retval = 1
        if retval:
            if self._returntype is ReturnType.JSON:
                return 1, {'status': 'error', 'lines': list_handler.buffer}
            else:
                self._logger.error('Fatal errors occurred.')
                return 1, retval

        check_logger.info('Checking runtime and pipeline configuration.')
        all_queues = set()
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            if bot_id == 'global':
                continue
            # pipeline keys
            for field in ['description', 'group', 'module', 'name', 'enabled']:
                if field not in bot_config:
                    check_logger.warning('Bot %r has no %r.', bot_id, field)
                    retval = 1
            if 'run_mode' in bot_config and bot_config['run_mode'] not in ['continuous', 'scheduled']:
                message = "Bot %r has invalid `run_mode` %r. Must be 'continuous' or 'scheduled'."
                check_logger.warning(message, bot_id, bot_config['run_mode'])
                retval = 1
            if ('group' in bot_config and bot_config['group'] in ['Collector', 'Parser', 'Expert']):
                if ('parameters' not in bot_config or 'destination_queues' not in bot_config['parameters'] or
                   (isinstance(bot_config['parameters']['destination_queues'], list) and len(bot_config['parameters']['destination_queues']) < 1) or
                   (isinstance(bot_config['parameters']['destination_queues'], dict) and '_default' not in bot_config['parameters']['destination_queues'])):
                    check_logger.error('Misconfiguration: No (default) destination queue for %r.', bot_id)
                    retval = 1
                else:
                    all_queues = all_queues.union(bot_config['parameters']['destination_queues'])
            if ('group' in bot_config and bot_config['group'] in ['Parser', 'Expert', 'Output']):
                if ('parameters' in bot_config and 'source_queue' in bot_config['parameters'] and isinstance(bot_config['parameters']['source_queue'], str)):
                    all_queues.add(bot_config['parameters']['source_queue'])
                    all_queues.add(f"{bot_config['parameters']['source_queue']}-internal")
                else:
                    all_queues.add(f"{bot_id}-queue")
                    all_queues.add(f"{bot_id}-queue-internal")
        # ignore allowed orphaned queues
        allowed_orphan_queues = set(getattr(self._parameters, 'intelmqctl_check_orphaned_queues_ignore', ()))
        if not no_connections:
            try:
                pipeline = PipelineFactory.create(logger=self._logger, pipeline_args=self._parameters.__dict__)
                pipeline.set_queues(None, "source")
                pipeline.connect()
                orphan_queues = "', '".join(pipeline.nonempty_queues() - all_queues - allowed_orphan_queues)
            except Exception as exc:
                error = utils.error_message_from_exc(exc)
                check_logger.error('Could not connect to pipeline: %s', error)
                retval = 1
            else:
                if orphan_queues:
                    check_logger.warning("Orphaned queues found: '%s'. Possible leftover from past reconfigurations "
                                         "without cleanup. Have a look at the FAQ at "
                                         "https://intelmq.readthedocs.io/en/maintenance/user/FAQ.html"
                                         "#orphaned-queues", orphan_queues)

        check_logger.info('Checking harmonization configuration.')
        for event_type, event_type_conf in files[HARMONIZATION_CONF_FILE].items():
            for harm_type_name, harm_type in event_type_conf.items():
                if "description" not in harm_type:
                    check_logger.warning('Missing description for type %r.', harm_type_name)
                if "type" not in harm_type:
                    check_logger.error('Missing type for type %r.', harm_type_name)
                    retval = 1
                    continue
                if "regex" in harm_type:
                    try:
                        re.compile(harm_type['regex'])
                    except Exception as e:
                        check_logger.error('Invalid regex for type %r: %r.', harm_type_name, str(e))
                        retval = 1
                        continue
        extra_type = files[HARMONIZATION_CONF_FILE].get('event', {}).get('extra', {}).get('type')
        if extra_type != 'JSONDict':
            check_logger.warning("'extra' field needs to be of type 'JSONDict'.")
            retval = 1
        if upgrades.harmonization({}, files[HARMONIZATION_CONF_FILE],
                                  dry_run=True)[0]:
            check_logger.warning("Harmonization needs an upgrade, call "
                                 "intelmqctl upgrade-config.")

        check_logger.info('Checking for bots.')
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            if bot_id != 'global':
                # importable module
                try:
                    bot_module = importlib.import_module(bot_config['module'])
                except ImportError as exc:
                    check_logger.error('Incomplete installation: Bot %r not importable: %r.', bot_id, exc)
                    retval = 1
                    continue
                except SyntaxError as exc:
                    check_logger.error('SyntaxError in bot %r: %r', bot_id, exc)
                    retval = 1
                    continue
                bot = getattr(bot_module, 'BOT')
                bot_parameters = utils.get_global_settings()
                bot_parameters.update(bot_config.get('parameters', {}))  # the parameters field may not exist
                bot_check = bot.check(bot_parameters)
                if bot_check:
                    for log_line in bot_check:
                        getattr(check_logger, log_line[0])(f"Bot {bot_id!r}: {log_line[1]}")
        if check_executables:
            for group in utils.list_all_bots().values():
                for bot_id, bot in group.items():
                    if subprocess.call(['which', bot['module']], stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL):
                        check_logger.error('Incomplete installation: Executable %r for %r not found in $PATH (%r).',
                                           bot['module'], bot_id, os.getenv('PATH'))
                        retval = 1

        if os.path.isfile(STATE_FILE_PATH):
            state = utils.load_configuration(STATE_FILE_PATH)
            for functionname in upgrades.__all__:
                if not state['upgrades'].get(functionname, False):
                    check_logger.error("Upgrade function %s not completed (successfully). "
                                       "Please run 'intelmqctl upgrade-config'.",
                                       functionname)
        else:
            check_logger.error("No state file found. Please call 'intelmqctl upgrade-config'.")

        if self._returntype is ReturnType.JSON:
            if retval:
                return 1, {'status': 'error', 'lines': list_handler.buffer}
            else:
                return 0, {'status': 'success', 'lines': list_handler.buffer}
        else:
            if retval:
                self._logger.error('Some issues have been found, please check the above output.')
                return retval, 'error'
            else:
                self._logger.info('No issues found.')
                return retval, 'success'

    def upgrade_conf(self, previous=None, dry_run=None, function=None,
                     force=None, state_file: str = STATE_FILE_PATH,
                     no_backup=False):
        """
        Upgrade the IntelMQ configuration after a version upgrade.

        Parameters:
            previous: Assume the given version as the previous version
            function: Only execute this upgrade function
            force: Also upgrade if not necessary
            state_file: location of the state file
            no_backup: Do not create backups of state and configuration files

        state_file:

            .. code-block:: json

               version_history = [..., [2, 0, 0], [2, 0, 1]]
               upgrades = {
                   "v112_feodo_tracker_domains": true,
                   "v112_feodo_tracker_ips": false,
                   "v200beta1_ripe_expert": false
                   }
               results = [
                   {"function": "v112_feodo_tracker_domains",
                    "success": true,
                    "retval": null,
                    "time": "..."},
                   {"function": "v112_feodo_tracker_domains",
                    "success": false,
                    "retval": "fix it manually",
                    "message": "fix it manually",
                    "time": "..."},
                   {"function": "v200beta1_ripe_expert",
                    "success": false,
                    "traceback": "...",
                    "time": "..."}
                   ]

        """
        if os.path.isfile(state_file):
            if not os.access(state_file, os.W_OK) and not dry_run:
                self._logger.error("State file %r is not writable.", state_file)
                return 1, "State file %r is not writable." % state_file
            state = utils.load_configuration(state_file)
        else:
            """
            We create the state file directly before any upgrade function.
            Otherwise we might run into the situation, that we can't write the state but we already upgraded.
            """
            self._logger.info('Writing initial state file.')
            state = {"version_history": [],
                     "upgrades": {},
                     "results": []}
            if dry_run:
                self._logger.info('Would create state file now at %r.', state_file)
                return 0, 'success'
            try:
                utils.write_configuration(state_file, state, new=True, useyaml=False)
            except Exception as exc:
                self._logger.error('Error writing state file %r: %s.', state_file, exc)
                return 1, f'Error writing state file {state_file!r}: {exc}.'
            self._logger.info('Successfully wrote initial state file.')

        runtime = utils.load_configuration(RUNTIME_CONF_FILE)
        if 'global' not in runtime:
            runtime['global'] = {}
        harmonization = utils.load_configuration(HARMONIZATION_CONF_FILE)
        if dry_run:
            self._logger.info('Doing a dry run, not writing anything now.')

        if function:
            if not force and state['upgrades'].get(function, False):
                # already performed
                self._logger.info('This upgrade has been performed previously successfully already. Force with -f.')
                return 0, 'success'

            result = {"function": function,
                      "time": datetime.datetime.now().isoformat()
                      }
            if not hasattr(upgrades, function):
                self._logger.error('This function does not exist. Available functions are %s', ', '.join(upgrades.__all__))
                return 1, 'error'
            try:
                retval, runtime_new, harmonization_new = getattr(
                    upgrades, function)(runtime, harmonization, dry_run,
                                        version_history=state['version_history'])
                # Handle changed configurations
                if retval is True and not dry_run:
                    utils.write_configuration(RUNTIME_CONF_FILE, runtime_new,
                                              backup=not no_backup)
                    utils.write_configuration(HARMONIZATION_CONF_FILE, harmonization_new,
                                              backup=not no_backup, useyaml=False)
            except Exception:
                self._logger.exception('Upgrade %r failed, please report this bug with the shown traceback.', function)
                result['traceback'] = traceback.format_exc()
                result['success'] = False
            else:
                if type(retval) is str:
                    self._logger.error('Upgrade %r failed: %s', function, retval)
                    result['message'] = retval
                    result['success'] = False
                elif retval is None:
                    self._logger.info('Upgrade %r successful: Nothing to do.', function)
                    result['success'] = True
                elif retval is True:
                    self._logger.info('Upgrade %r successful.', function)
                    result['success'] = True
                else:
                    self._logger.error('Unknown return value %r for %r. Please report this as bug.', retval, function)
                    result['success'] = False

                result['retval'] = retval

            state['results'].append(result)
            state['upgrades'][function] = result['success']
            if not dry_run:
                utils.write_configuration(state_file, state,
                                          backup=not no_backup, useyaml=False)

            if result['success']:
                return 0, 'success'
            else:
                return 1, 'error'

        if previous:
            previous = tuple(utils.lazy_int(v) for v in previous.split('.'))
            self._logger.info("Using previous version %r from parameter.", '.'.join(str(x) for x in previous))

        if __version_info__ in state["version_history"] and not force:
            return 0, "Nothing to do."
        else:
            if state["version_history"] and not previous and not force:
                previous = state["version_history"][-1]
                self._logger.info("Found previous version %s in state file.", '.'.join(str(x) for x in previous))
            if previous:
                todo = []
                for version, functions in upgrades.UPGRADES.items():
                    if utils.version_smaller(tuple(previous), version):
                        todo.append((version, functions, True))
                    else:
                        funcs = []
                        for function in functions:
                            fname = function.__name__
                            if not state['upgrades'].get(fname, False):
                                self._logger.info("Catch up function %s from version %s.", fname, '.'.join(str(x) for x in version))
                                funcs.append(function)
                        if funcs:
                            todo.append((version, funcs, False))
            else:
                self._logger.info("Found no previous version or forced, doing all upgrades.")
                todo = [(version, bunch, True) for version, bunch in upgrades.UPGRADES.items()]

            todo.extend([(None, (function, ), False)
                         for function in upgrades.ALWAYS])

            """
            todo is now a list of tuples of functions.
            todo = [
                    (version, tuple of functions, bool if the version is new)
                    ...
                    ]
            all functions in a tuple (bunch) must be processed successfully to continue
            the third value is to catch some situations:
                if the function has been inserted later, we do not say this is an upgrade to a newer version
                and do not append the version to the version history again
            """

            error = False
            for version, bunch, version_new in todo:
                if version and version_new:
                    self._logger.info('Upgrading to version %s.', '.'.join(map(str, version)))
                for function in bunch:
                    if not force and state['upgrades'].get(function.__name__, False):
                        # already performed
                        continue

                    # shown text should have only one line
                    docstring = textwrap.dedent(function.__doc__).strip().replace('\n', ' ')
                    result = {"function": function.__name__,
                              "time": datetime.datetime.now().isoformat()
                              }
                    try:
                        retval, runtime, harmonization = function(runtime, harmonization, dry_run,
                                                                  version_history=state['version_history'])
                    except Exception:
                        self._logger.exception('%s: Upgrade failed, please report this bug with the traceback.', docstring)
                        result['traceback'] = traceback.format_exc()
                        result['success'] = False
                    else:
                        if type(retval) is str:
                            self._logger.error('%s: Upgrade failed: %s', docstring, retval)
                            result['message'] = retval
                            result['success'] = False
                        elif retval is None:
                            self._logger.info('%s: Nothing to do.', docstring)
                            result['success'] = True
                        elif retval is True:
                            self._logger.info('%s: Upgrade successful.', docstring)
                            result['success'] = True
                        else:
                            self._logger.error('%s: Unknown return value %r. Please report this as bug.', docstring, retval)
                            result['success'] = False
                        result['retval'] = retval

                    if version or retval is not None:
                        """
                        do not add it to the results if it is run always
                        and was a no-op.
                        """
                        state['results'].append(result)
                    if version:
                        """
                        Only add it to the upgrades list if it is specific to a function
                        """
                        state['upgrades'][function.__name__] = result['success']

                    if not result['success']:
                        error = True
                        break
                if error:
                    break
                if version and version_new:
                    state['version_history'].append(version)

            if error:
                # some upgrade function had a problem
                if not dry_run:
                    utils.write_configuration(state_file, state,
                                              backup=not no_backup, useyaml=False)
                self._logger.error('Some migration did not succeed or manual intervention is needed. '
                                   'Look at the output above. Afterwards, re-run this program.')

            try:
                if not dry_run:
                    utils.write_configuration(RUNTIME_CONF_FILE, runtime,
                                              backup=not no_backup)
                    utils.write_configuration(HARMONIZATION_CONF_FILE, harmonization,
                                              backup=not no_backup, useyaml=False)
            except Exception as exc:
                self._logger.error('Writing runtime configuration did not succeed: %s\nFix the '
                                   'problem and afterwards, re-run this program.', exc)
                return 1, 'error'

            if not error:
                if todo:
                    self._logger.info('Configuration upgrade successful!')
                else:
                    self._logger.info('Nothing to do!')

            if not dry_run:
                utils.write_configuration(state_file, state,
                                          backup=not no_backup, useyaml=False)

        if error:
            return 1, 'error'
        else:
            return 0, 'success'

    def debug(self, sections=None):
        """
        Give debugging output
        """

        output = {}
        if sections is None or 'paths' in sections:
            output['paths'] = {}
            variables = globals()
            if self._returntype is ReturnType.TEXT:
                print('Paths:')
            for path in ('HARMONIZATION_CONF_FILE',
                         'RUNTIME_CONF_FILE', 'VAR_RUN_PATH', 'STATE_FILE_PATH',
                         'DEFAULT_LOGGING_PATH', '__file__',
                         'CONFIG_DIR', 'ROOT_DIR'):
                output['paths'][path] = variables[path]
                if self._returntype is ReturnType.TEXT:
                    print(f'{path}: {variables[path]!r}')
        if sections is None or 'environment_variables' in sections:
            output['environment_variables'] = {}
            if self._returntype is ReturnType.TEXT:
                print('Environment variables:')
            for variable in ('INTELMQ_ROOT_DIR', 'INTELMQ_PATHS_NO_OPT',
                             'INTELMQ_PATHS_OPT', 'INTELMQ_MANAGER_CONTROLLER_CMD',
                             'PATH'):
                output['environment_variables'][variable] = os.getenv(variable)
                if self._returntype is ReturnType.TEXT:
                    print(f'{variable}: {os.getenv(variable)!r}')
        return 0, output

    def log_bot_message(self, status, *args):
        if self._returntype is ReturnType.TEXT and not self._quiet:
            self._logger.info(MESSAGES[status], *args)

    def log_botnet_message(self, status, group=None):
        if self._returntype is ReturnType.TEXT and not self._quiet:
            if group:
                self._logger.info(MESSAGES[status], BOT_GROUP[group] + " group")
            else:
                self._logger.info(MESSAGES[status], 'Botnet')

    def log_log_messages(self, messages):
        if self._returntype is ReturnType.TEXT:
            for message in messages:
                print(' - '.join([message['date'], message['bot_id'],
                                  message['log_level'], message['message']]))
                try:
                    print(message['extended_message'])
                except KeyError:
                    pass


def main():  # pragma: no cover
    x = IntelMQController(interactive=True)
    return x.run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
