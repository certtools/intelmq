#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import importlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from collections import OrderedDict

import pkg_resources
import psutil

from intelmq import (DEFAULTS_CONF_FILE, PIPELINE_CONF_FILE, RUNTIME_CONF_FILE,
                     VAR_RUN_PATH, BOTS_FILE, HARMONIZATION_CONF_FILE,
                     DEFAULT_LOGGING_LEVEL)
from intelmq.lib import utils
from intelmq.lib.bot_debugger import BotDebugger
from intelmq.lib.pipeline import PipelineFactory


class Parameters(object):
    pass


STATUSES = {
    'starting': 0,
    'running': 1,
    'stopping': 2,
    'stopped': 3,
}

MESSAGES = {
    'disabled': 'Bot %s is disabled.',
    'starting': 'Starting %s...',
    'running': 'Bot %s is running.',
    'stopped': 'Bot %s is stopped.',
    'stopping': 'Stopping bot %s...',
    'reloading': 'Reloading bot %s ...',
    'reloaded': 'Bot %s is reloaded.',
}

ERROR_MESSAGES = {
    'starting': 'Bot %s failed to START.',
    'running': 'Bot %s is still running.',
    'stopped': 'Bot %s was NOT RUNNING.',
    'stopping': 'Bot %s failed to STOP.',
    'not found': 'Bot %s failed to START because the file cannot be found.',
    'access denied': 'Bot %s failed to %s because of missing permissions.',
    'unknown': 'Status of Bot %s is unknown: %r.',
}

LOG_LEVEL = OrderedDict([
    ('DEBUG', 0),
    ('INFO', 1),
    ('WARNING', 2),
    ('ERROR', 3),
    ('CRITICAL', 4),
])

RETURN_TYPES = ['text', 'json']
RETURN_TYPE = None
QUIET = False

BOT_GROUP = {"collectors": "Collector", "parsers": "Parser", "experts": "Expert", "outputs": "Output"}


def log_list_queues(queues):
    if RETURN_TYPE == 'text':
        for queue, counter in sorted(queues.items(), key=lambda x: str.lower(x[0])):
            if counter or not QUIET:
                logger.info("%s - %s", queue, counter)


def log_bot_error(status, *args):
    if RETURN_TYPE == 'text':
        logger.error(ERROR_MESSAGES[status], *args)


def log_bot_message(status, *args):
    if QUIET:
        return
    if RETURN_TYPE == 'text':
        logger.info(MESSAGES[status], *args)


def log_botnet_error(status, group=None):
    if RETURN_TYPE == 'text':
        logger.error(ERROR_MESSAGES[status], BOT_GROUP[group] + (" group" if group else ""))


def log_botnet_message(status, group=None):
    if QUIET:
        return
    if RETURN_TYPE == 'text':
        if group:
            logger.info(MESSAGES[status], BOT_GROUP[group] + " group")
        else:
            logger.info(MESSAGES[status], 'Botnet')


def log_log_messages(messages):
    if RETURN_TYPE == 'text':
        for message in messages:
            print(' - '.join([message['date'], message['bot_id'],
                              message['log_level'], message['message']]))
            try:
                print(message['extended_message'])
            except KeyError:
                pass


class IntelMQProcessManager:
    PIDDIR = VAR_RUN_PATH
    PIDFILE = os.path.join(PIDDIR, "{}.pid")

    def __init__(self, runtime_configuration, logger, controller):
        self.__runtime_configuration = runtime_configuration
        self.logger = logger
        self.controller = controller

        if not os.path.exists(self.PIDDIR):
            try:
                os.makedirs(self.PIDDIR)
            except PermissionError as exc:  # pragma: no cover
                self.logger.error('Directory %s does not exist and cannot be '
                                  'created: %s.', self.PIDDIR, exc)

    def bot_run(self, bot_id, run_subcommand=None, console_type=None, message_action_kind=None, dryrun=None, msg=None,
                show_sent=None, loglevel=None):
        pid = self.__check_pid(bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        status = self.__status_process(pid, module, bot_id) if pid else False
        if pid and status is True:
            self.logger.warning("Main instance of the bot is running in the background and will be stopped; "
                                "when finished, we try to relaunch it again. "
                                "You may want to launch: 'intelmqctl stop {}' to prevent this message."
                                .format(bot_id))
            paused = True
            self.bot_stop(bot_id)
        elif status is False:
            paused = False
        else:
            self.logger.error(status)
            return 1

        log_bot_message('starting', bot_id)
        filename = self.PIDFILE.format(bot_id)
        with open(filename, 'w') as fp:
            fp.write(str(os.getpid()))

        try:
            BotDebugger(self.__runtime_configuration[bot_id], bot_id, run_subcommand,
                        console_type, message_action_kind, dryrun, msg, show_sent,
                        loglevel=loglevel)
            retval = 0
        except KeyboardInterrupt:
            print('Keyboard interrupt.')
            retval = 0
        except SystemExit as exc:
            print('Bot exited with code %s.' % exc.code)
            retval = exc.code

        self.__remove_pidfile(bot_id)
        if paused:
            self.bot_start(bot_id)
        return retval

    def bot_start(self, bot_id, getstatus=True):
        pid = self.__check_pid(bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        if pid:
            status = self.__status_process(pid, module, bot_id)
            if status is True:
                log_bot_message('running', bot_id)
                return 'running'
            elif status is False:
                self.__remove_pidfile(bot_id)
            else:
                self.logger.error(status)
                return 1

        log_bot_message('starting', bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        cmdargs = [module, bot_id]
        try:
            proc = psutil.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            log_bot_error("not found", bot_id)
            return 'stopped'
        else:
            filename = self.PIDFILE.format(bot_id)
            with open(filename, 'w') as fp:
                fp.write(str(proc.pid))

        if getstatus:
            time.sleep(0.5)
            return self.bot_status(bot_id, proc=proc)

    def bot_stop(self, bot_id, getstatus=True):
        pid = self.__check_pid(bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        if not pid:
            if self.controller._is_enabled(bot_id):
                log_bot_error('stopped', bot_id)
                return 'stopped'
            else:
                log_bot_message('disabled', bot_id)
                return 'disabled'
        status = self.__status_process(pid, module, bot_id)
        if status is False:
            self.__remove_pidfile(bot_id)
            log_bot_error('stopped', bot_id)
            return 'stopped'
        elif status is not True:
            log_bot_error('unknown', bot_id, status)
            return 'unknown'
        log_bot_message('stopping', bot_id)
        proc = psutil.Process(int(pid))
        try:
            proc.send_signal(signal.SIGTERM)
        except psutil.AccessDenied:
            log_bot_error('access denied', bot_id, 'STOP')
            return 'running'
        else:
            if getstatus:
                time.sleep(0.5)
                status = self.__status_process(pid, module, bot_id)
                if status is True:
                    log_bot_error('running', bot_id)
                    return 'running'
                elif status is not False:
                    log_bot_error('unknown', bot_id, status)
                    return 'unknown'
                try:
                    self.__remove_pidfile(bot_id)
                except FileNotFoundError:  # Bot was running interactively and file has been removed already
                    pass
                log_bot_message('stopped', bot_id)
                return 'stopped'

    def bot_reload(self, bot_id, getstatus=True):
        pid = self.__check_pid(bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        if not pid:
            if self.controller._is_enabled(bot_id):
                log_bot_error('stopped', bot_id)
                return 'stopped'
            else:
                log_bot_message('disabled', bot_id)
                return 'disabled'
        status = self.__status_process(pid, module, bot_id)
        if status is False:
            self.__remove_pidfile(bot_id)
            log_bot_error('stopped', bot_id)
            return 'stopped'
        elif status is not True:
            log_bot_error('unknown', bot_id, status)
            return 'unknown'
        log_bot_message('reloading', bot_id)
        proc = psutil.Process(int(pid))
        try:
            proc.send_signal(signal.SIGHUP)
        except psutil.AccessDenied:
            log_bot_error('access denied', bot_id, 'RELOAD')
            return 'running'
        else:
            if getstatus:
                time.sleep(0.5)
                status = self.__status_process(pid, module, bot_id)
                if status is True:
                    log_bot_message('running', bot_id)
                    return 'running'
                elif status is False:
                    log_bot_error('stopped', bot_id)
                    return 'stopped'
                else:
                    log_bot_error('unknown', bot_id, status)
                    return 'unknown'

    def bot_status(self, bot_id, *, proc=None):
        if proc:
            if proc.status() not in [psutil.STATUS_STOPPED, psutil.STATUS_DEAD, psutil.STATUS_ZOMBIE]:
                log_bot_message('running', bot_id)
                return 'running'
        else:
            pid = self.__check_pid(bot_id)
            module = self.__runtime_configuration[bot_id]['module']
            status = self.__status_process(pid, module, bot_id) if pid else False
            if pid and status is True:
                log_bot_message('running', bot_id)
                return 'running'
            elif status is not False:
                log_bot_error('unknown', bot_id, status)
                return 'unknown'

        if self.controller._is_enabled(bot_id):
            if not proc and pid:
                self.__remove_pidfile(bot_id)
            log_bot_message('stopped', bot_id)
            if proc and RETURN_TYPE == 'text':
                log = proc.stderr.read().decode()
                if not log:  # if nothing in stderr, print stdout
                    log = proc.stdout.read().decode()
                print(log.strip(), file=sys.stderr)
            return 'stopped'
        else:
            log_bot_message('disabled', bot_id)
            return 'disabled'

    def __check_pid(self, bot_id):
        filename = self.PIDFILE.format(bot_id)
        if os.path.isfile(filename):
            with open(filename, 'r') as fp:
                pid = fp.read()
            try:
                return int(pid.strip())
            except ValueError:
                return None
        return None

    def __remove_pidfile(self, bot_id):
        filename = self.PIDFILE.format(bot_id)
        os.remove(filename)

    def __status_process(self, pid, module, bot_id):
        which = shutil.which(module)
        if not which:
            return 'Could not get path to the excutable (%r). Check your PATH variable (%r).' % (module, os.environ.get('PATH'))
        try:
            proc = psutil.Process(int(pid))
            if len(proc.cmdline()) > 1 and proc.cmdline()[1] == shutil.which(module):
                return True
            elif (len(proc.cmdline()) > 3 and proc.cmdline()[1] == shutil.which('intelmqctl') and
                  proc.cmdline()[2] == 'run' and proc.cmdline()[3] == bot_id):
                return True
            elif len(proc.cmdline()) > 1:
                return 'Commandline of the program %r does not match expected value %r.' % (proc.cmdline()[1], shutil.which(module))
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied:
            return 'Could not get status of process: Access denied.'
        except:
            raise


PROCESS_MANAGER = {'intelmq': IntelMQProcessManager}


class IntelMQController():

    def __init__(self, interactive: bool = False, return_type: str = "python", quiet: bool = False):
        """
        Initializes intelmqctl.

        Parameters:
            interactive: for cli-interface true, functions can exits, parameters are used
            return_type: 'python': no special treatment, can be used for use by other
                python code
                'text': user-friendly output for cli, default for interactive use
                'json': machine-readable output for managers
            quiet: False by default, can be activated for cron jobs etc.
        """
        global RETURN_TYPE
        RETURN_TYPE = return_type
        global logger
        global QUIET
        QUIET = quiet
        self.parameters = Parameters()

        # Try to get log_level from defaults_configuration, else use default
        try:
            self.load_defaults_configuration()
        except Exception:
            log_level = DEFAULT_LOGGING_LEVEL
        else:
            log_level = self.parameters.logging_level

        try:
            logger = utils.log('intelmqctl', log_level=log_level)
        except (FileNotFoundError, PermissionError) as exc:
            logger = utils.log('intelmqctl', log_level=log_level, log_path=False)
            logger.error('Not logging to file: %s', exc)
        self.logger = logger
        self.interactive = interactive
        if os.geteuid() == 0:
            logger.warning('Running intelmqctl as root is highly discouraged!')

        APPNAME = "intelmqctl"
        try:
            VERSION = pkg_resources.get_distribution("intelmq").version
        except pkg_resources.DistributionNotFound:  # pragma: no cover
            # can only happen in interactive mode
            self.logger.error('No valid IntelMQ installation found: DistributionNotFound')
            sys.exit(1)
        DESCRIPTION = """
        description: intelmqctl is the tool to control intelmq system.

        Outputs are logged to /opt/intelmq/var/log/intelmqctl"""
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

Outputs are additionally logged to /opt/intelmq/var/log/intelmqctl'''

        # stolen functions from the bot file
        # this will not work with various instances of REDIS
        self.load_defaults_configuration()
        try:
            self.pipeline_configuration = utils.load_configuration(PIPELINE_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort('Error loading %r: %s' % (PIPELINE_CONF_FILE, exc))

        try:
            self.runtime_configuration = utils.load_configuration(RUNTIME_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort('Error loading %r: %s' % (RUNTIME_CONF_FILE, exc))

        process_manager = getattr(self.parameters, 'process_manager', 'intelmq')
        if process_manager not in PROCESS_MANAGER:
            self.abort('Invalid process manager given: %r, should be one of %r.'
                       '' % (process_manager, list(PROCESS_MANAGER.keys())))
        self.bot_process_manager = PROCESS_MANAGER[process_manager](
            self.runtime_configuration,
            logger,
            self
        )

        if self.interactive:
            parser = argparse.ArgumentParser(
                prog=APPNAME,
                description=DESCRIPTION,
                epilog=EPILOG,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )

            parser.add_argument('-v', '--version',
                                action='version', version=VERSION)
            parser.add_argument('--type', '-t', choices=RETURN_TYPES,
                                default=RETURN_TYPES[0],
                                help='choose if it should return regular text '
                                     'or other machine-readable')

            parser.add_argument('--quiet', '-q', action='store_const',
                                help='Quiet mode, useful for reloads initiated '
                                     'scripts like logrotate',
                                const=True)

            subparsers = parser.add_subparsers(title='subcommands')

            parser_list = subparsers.add_parser('list', help='Listing bots or queues')
            parser_list.add_argument('kind', choices=['bots', 'queues', 'queues-and-status'])
            parser_list.add_argument('--quiet', '-q', action='store_const',
                                     help='Only list non-empty queues '
                                          'or the IDs of enabled bots.',
                                     const=True)
            parser_list.set_defaults(func=self.list)

            parser_clear = subparsers.add_parser('clear', help='Clear a queue')
            parser_clear.add_argument('queue', help='queue name',
                                      choices=self.get_queues()[3])
            parser_clear.set_defaults(func=self.clear_queue)

            parser_log = subparsers.add_parser('log', help='Get last log lines of a bot')
            parser_log.add_argument('bot_id', help='bot id')
            parser_log.add_argument('number_of_lines', help='number of lines',
                                    default=10, type=int, nargs='?')
            parser_log.add_argument('log_level', help='logging level',
                                    choices=LOG_LEVEL.keys(), default='INFO', nargs='?')
            parser_log.set_defaults(func=self.read_bot_log)

            parser_run = subparsers.add_parser('run', help='Run a bot interactively')
            parser_run.add_argument('bot_id',
                                    choices=self.runtime_configuration.keys())
            parser_run.add_argument('--loglevel', '-l',
                                    nargs='?', default=None,
                                    choices=LOG_LEVEL.keys())
            parser_run_subparsers = parser_run.add_subparsers(title='run-subcommands')

            parser_run_console = parser_run_subparsers.add_parser('console', help='Get a ipdb live console.')
            parser_run_console.add_argument('console_type', nargs='?',
                                            help='You may specify which console should be run. Default is ipdb (if installed)'
                                                 ' or pudb (if installed) or pdb but you may want to use another one.')
            parser_run_console.set_defaults(run_subcommand="console")

            parser_run_message = parser_run_subparsers.add_parser('message',
                                                                  help='Debug bot\'s pipelines. Get the message in the'
                                                                       ' input pipeline, pop it (cut it) and display it, or'
                                                                       ' send the message directly to bot\'s output pipeline.')
            parser_run_message.add_argument('message_action_kind', choices=["get", "pop", "send"])
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
            parser_check.add_argument('--quiet', '-q', action='store_const',
                                      help='Only print warnings and errors.',
                                      const=True)
            parser_check.add_argument('--no-connections', '-C', action='store_const',
                                      help='Do not test the connections to services like redis.',
                                      const=True)
            parser_check.set_defaults(func=self.check)

            parser_help = subparsers.add_parser('help',
                                                help='Show the help')
            parser_help.set_defaults(func=parser.print_help)

            parser_start = subparsers.add_parser('start', help='Start a bot or botnet')
            parser_start.add_argument('bot_id', nargs='?',
                                      choices=self.runtime_configuration.keys())
            parser_start.add_argument('--group', help='Start a group of bots',
                                      choices=BOT_GROUP.keys())
            parser_start.set_defaults(func=self.bot_start)

            parser_stop = subparsers.add_parser('stop', help='Stop a bot or botnet')
            parser_stop.add_argument('bot_id', nargs='?',
                                     choices=self.runtime_configuration.keys())
            parser_stop.add_argument('--group', help='Stop a group of bots',
                                     choices=BOT_GROUP.keys())
            parser_stop.set_defaults(func=self.bot_stop)

            parser_restart = subparsers.add_parser('restart', help='Restart a bot or botnet')
            parser_restart.add_argument('bot_id', nargs='?',
                                        choices=self.runtime_configuration.keys())
            parser_restart.add_argument('--group', help='Restart a group of bots',
                                        choices=BOT_GROUP.keys())
            parser_restart.set_defaults(func=self.bot_restart)

            parser_reload = subparsers.add_parser('reload', help='Reload a bot or botnet')
            parser_reload.add_argument('bot_id', nargs='?',
                                       choices=self.runtime_configuration.keys())
            parser_reload.add_argument('--group', help='Reload a group of bots',
                                       choices=BOT_GROUP.keys())
            parser_reload.set_defaults(func=self.bot_reload)

            parser_status = subparsers.add_parser('status', help='Status of a bot or botnet')
            parser_status.add_argument('bot_id', nargs='?',
                                       choices=self.runtime_configuration.keys())
            parser_status.add_argument('--group', help='Get status of a group of bots',
                                       choices=BOT_GROUP.keys())
            parser_status.set_defaults(func=self.bot_status)

            parser_status = subparsers.add_parser('enable', help='Enable a bot')
            parser_status.add_argument('bot_id',
                                       choices=self.runtime_configuration.keys())
            parser_status.set_defaults(func=self.bot_enable)

            parser_status = subparsers.add_parser('disable', help='Disable a bot')
            parser_status.add_argument('bot_id',
                                       choices=self.runtime_configuration.keys())
            parser_status.set_defaults(func=self.bot_disable)

            self.parser = parser

    def load_defaults_configuration(self, silent=False):
        # Load defaults configuration
        try:
            config = utils.load_configuration(DEFAULTS_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            if not silent:
                self.abort('Error loading %r: %s' % (DEFAULTS_CONF_FILE, exc))
        for option, value in config.items():
            setattr(self.parameters, option, value)

    def run(self):
        results = None
        args = self.parser.parse_args()
        if 'func' not in args:
            sys.exit(self.parser.print_help())
        args_dict = vars(args).copy()

        global RETURN_TYPE, QUIET
        RETURN_TYPE, QUIET = args.type, args.quiet
        del args_dict['type'], args_dict['quiet'], args_dict['func']
        retval, results = args.func(**args_dict)

        if RETURN_TYPE == 'json':
            print(json.dumps(results))
        return retval

    def bot_run(self, **kwargs):
        return self.bot_process_manager.bot_run(**kwargs), None

    def bot_start(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_start(group=group)
        else:
            status = self.bot_process_manager.bot_start(bot_id, getstatus)
            if status in ['running']:
                return 0, status
            else:
                return 1, status

    def bot_stop(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_stop(group=group)
        else:
            status = self.bot_process_manager.bot_stop(bot_id, getstatus)
            if status in ['stopped', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_reload(self, bot_id, getstatus=True, group=None):
        if bot_id is None:
            return self.botnet_reload(group=group)
        else:
            status = self.bot_process_manager.bot_reload(bot_id, getstatus)
            if status in ['running']:
                return 0, status
            else:
                return 1, status

    def bot_restart(self, bot_id, group=None):
        if bot_id is None:
            return self.botnet_restart(group=group)
        else:
            status_stop = self.bot_stop(bot_id)
            status_start = self.bot_start(bot_id)
            return status_stop[0] | status_start[0], [status_stop[1], status_start[1]]

    def bot_status(self, bot_id, group=None):
        if bot_id is None:
            return self.botnet_status(group=group)
        else:
            status = self.bot_process_manager.bot_status(bot_id)
            if status in ['running', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_enable(self, bot_id):
        self.runtime_configuration[bot_id]['enabled'] = True
        self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def bot_disable(self, bot_id):
        self.runtime_configuration[bot_id]['enabled'] = False
        self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def _is_enabled(self, bot_id):
        return self.runtime_configuration[bot_id].get('enabled', True)

    def botnet_start(self, group=None):
        botnet_status = {}

        if group:
            bots = sorted(k_v[0] for k_v in filter(lambda x: x[1]["group"] == BOT_GROUP[group], self.runtime_configuration.items()))
        else:
            bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            if self.runtime_configuration[bot_id].get('enabled', True):
                self.bot_start(bot_id, getstatus=False)
            else:
                log_bot_message('disabled', bot_id)
                botnet_status[bot_id] = 'disabled'

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            if self.runtime_configuration[bot_id].get('enabled', True):
                botnet_status[bot_id] = self.bot_status(bot_id)[1]
                if botnet_status[bot_id] not in ['running', 'disabled']:
                    retval = 1
                    if RETURN_TYPE == 'text':
                        print(bot_id, botnet_status[bot_id])

        log_botnet_message('running', group)
        return retval, botnet_status

    def botnet_stop(self, group=None):
        botnet_status = {}
        log_botnet_message('stopping', group)

        if group:
            bots = sorted(k_v[0] for k_v in filter(lambda x: x[1]["group"] == BOT_GROUP[group], self.runtime_configuration.items()))
        else:
            bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            self.bot_stop(bot_id, getstatus=False)

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['stopped', 'disabled']:
                retval = 1

        log_botnet_message('stopped', group)
        return retval, botnet_status

    def botnet_reload(self, group=None):
        botnet_status = {}
        log_botnet_message('reloading', group)

        if group:
            bots = sorted(k_v[0] for k_v in filter(lambda x: x[1]["group"] == BOT_GROUP[group], self.runtime_configuration.items()))
        else:
            bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            self.bot_reload(bot_id, getstatus=False)

        retval = 0
        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['running', 'disabled']:
                retval = 1
        log_botnet_message('reloaded', group)
        return retval, botnet_status

    def botnet_restart(self, group=None):
        retval_stop, _ = self.botnet_stop(group=group)
        retval_start, status = self.botnet_start(group=group)
        if retval_stop > retval_start:  # In case the stop operation was not successful, exit 1
            retval_start = retval_stop
        return retval_start, status

    def botnet_status(self, group=None):
        retval = 0
        botnet_status = {}
        if group:
            bots = sorted(k_v[0] for k_v in filter(lambda x: x[1]["group"] == BOT_GROUP[group], self.runtime_configuration.items()))
        else:
            bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)[1]
            if botnet_status[bot_id] not in ['running', 'disabled']:
                retval = 1
        return retval, botnet_status

    def list(self, kind=None):
        if kind == 'queues':
            return self.list_queues()
        elif kind == 'bots':
            return self.list_bots()
        elif kind == 'queues-and-status':
            q = self.list_queues()
            b = self.botnet_status()
            return q[0] | b[0], [q[1], b[1]]

    def abort(self, message):
        if self.interactive:
            sys.exit(message)
        else:
            raise ValueError(message)

    def write_updated_runtime_config(self, filename=RUNTIME_CONF_FILE):
        try:
            with open(RUNTIME_CONF_FILE, 'w') as handle:
                json.dump(self.runtime_configuration, fp=handle, indent=4, sort_keys=True,
                          separators=(',', ': '))
        except PermissionError:
            self.abort('Can\'t update runtime configuration: Permission denied.')
        return True

    def list_bots(self):
        """
        Lists all configured bots from runtime.conf with bot id and
        description.

        If description is not set, None is used instead.
        """
        if RETURN_TYPE == 'text':
            for bot_id in sorted(self.runtime_configuration.keys(), key=str.lower):
                if QUIET and not self.runtime_configuration[bot_id].get('enabled'):
                    continue
                if QUIET:
                    print(bot_id)
                else:
                    print("Bot ID: {}\nDescription: {}"
                          "".format(bot_id, self.runtime_configuration[bot_id].get('description')))
        return 0, [{'id': bot_id,
                    'description': self.runtime_configuration[bot_id].get('description')}
                   for bot_id in sorted(self.runtime_configuration.keys())]

    def get_queues(self):
        """
        :return: 4-tuple of source, destination, internal queues, and all queues combined.
        The returned values are only queue names, not their paths. I.E. if there is a bot with
        destination queues = {"_default": "one", "other": ["two", "three"]}, only set of {"one", "two", "three"} gets returned.
        (Note that the "_default" path has single string and the "other" path has a list that gets flattened.)
        """
        source_queues = set()
        destination_queues = set()
        internal_queues = set()

        for botid, value in self.pipeline_configuration.items():
            if 'source-queue' in value:
                source_queues.add(value['source-queue'])
                internal_queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                # flattens ["one", "two"] → {"one", "two"}, {"_default": "one", "other": ["two", "three"]} → {"one", "two", "three"}
                destination_queues.update(utils.flatten_queues(value['destination-queues']))

        all_queues = source_queues.union(destination_queues).union(internal_queues)

        return source_queues, destination_queues, internal_queues, all_queues

    def list_queues(self):
        source_queues, destination_queues, internal_queues, all_queues = self.get_queues()
        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(None, "source")
        pipeline.connect()

        counters = pipeline.count_queued_messages(*all_queues)
        log_list_queues(counters)

        return_dict = {}
        for bot_id, info in self.pipeline_configuration.items():
            return_dict[bot_id] = {}

            if 'source-queue' in info:
                return_dict[bot_id]['source_queue'] = (
                    info['source-queue'], counters[info['source-queue']])
                return_dict[bot_id]['internal_queue'] = counters[info['source-queue'] + '-internal']

            if 'destination-queues' in info:
                return_dict[bot_id]['destination_queues'] = []
                for dest_queue in utils.flatten_queues(info['destination-queues']):
                    return_dict[bot_id]['destination_queues'].append((dest_queue, counters[dest_queue]))

        return 0, return_dict

    def clear_queue(self, queue):
        """
        Clears an exiting queue.

        First checks if the queue does exist in the pipeline configuration.
        """
        if RETURN_TYPE == 'text':
            logger.info("Clearing queue %s.", queue)
        queues = set()
        for key, value in self.pipeline_configuration.items():
            if 'source-queue' in value:
                queues.add(value['source-queue'])
                queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                queues.update(value['destination-queues'])

        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(None, "source")
        pipeline.connect()

        if queue not in queues:
            if RETURN_TYPE == 'text':
                logger.error("Queue %s does not exist!", queue)
            return 2, 'not-found'

        try:
            pipeline.clear_queue(queue)
            if RETURN_TYPE == 'text':
                logger.info("Successfully cleared queue %s.", queue)
            return 0, 'success'
        except Exception:  # pragma: no cover
            logger.exception("Error while clearing queue %s.",
                             queue)
            return 1, 'error'

    def read_bot_log(self, bot_id, log_level, number_of_lines):
        if self.parameters.logging_handler == 'file':
            bot_log_path = os.path.join(self.parameters.logging_path,
                                        bot_id + '.log')
            if not os.path.isfile(bot_log_path):
                logger.error("Log path not found: %s", bot_log_path)
                return 2, []
        elif self.parameters.logging_handler == 'syslog':
            bot_log_path = '/var/log/syslog'
        else:
            self.abort("Unknow logging handler %r" % self.parameters.logging_handler)

        if not os.access(bot_log_path, os.R_OK):
            self.logger.error('File %r is not readable.', bot_log_path)
            return 1, 'error'

        messages = []

        message_overflow = ''
        message_count = 0

        for line in utils.reverse_readline(bot_log_path):
            if self.parameters.logging_handler == 'file':
                log_message = utils.parse_logline(line)
            if self.parameters.logging_handler == 'syslog':
                log_message = utils.parse_logline(line, regex=utils.SYSLOG_REGEX)

            if type(log_message) is not dict:
                if self.parameters.logging_handler == 'file':
                    message_overflow = '\n'.join([line, message_overflow])
                continue
            if log_message['bot_id'] != bot_id:
                continue
            if LOG_LEVEL[log_message['log_level']] < LOG_LEVEL[log_level]:
                continue

            if message_overflow:
                log_message['extended_message'] = message_overflow
                message_overflow = ''

            if self.parameters.logging_handler == 'syslog':
                log_message['message'] = log_message['message'].replace('#012', '\n')

            message_count += 1
            messages.append(log_message)

            if message_count >= number_of_lines and number_of_lines != -1:
                break

        log_log_messages(messages[::-1])
        return 0, messages[::-1]

    def check(self, no_connections=False):
        retval = 0
        if RETURN_TYPE == 'json':
            output = []
        if QUIET:
            logger.setLevel('WARNING')

        # loading files and syntax check
        files = {DEFAULTS_CONF_FILE: None, PIPELINE_CONF_FILE: None,
                 RUNTIME_CONF_FILE: None, BOTS_FILE: None,
                 HARMONIZATION_CONF_FILE: None}
        if RETURN_TYPE == 'json':
            output.append(['info', 'Reading configuration files.'])
        else:
            self.logger.info('Reading configuration files.')
        for filename in files:
            try:
                with open(filename) as file_handle:
                    files[filename] = json.load(file_handle)
            except (IOError, ValueError) as exc:  # pragma: no cover
                if RETURN_TYPE == 'json':
                    output.append(['error', 'Coud not load %r: %s.' % (filename, exc)])
                else:
                    self.logger.error('Coud not load %r: %s.', filename, exc)
                retval = 1
        if retval:
            if RETURN_TYPE == 'json':
                return 1, {'status': 'error', 'lines': output}
            else:
                self.logger.error('Fatal errors occurred.')
                return 1, retval

        if RETURN_TYPE == 'json':
            output.append(['info', 'Checking defaults configuration.'])
        else:
            self.logger.info('Checking defaults configuration.')
        try:
            with open(pkg_resources.resource_filename('intelmq', 'etc/defaults.conf')) as fh:
                defaults = json.load(fh)
        except FileNotFoundError:
            pass
        else:
            keys = set(defaults.keys()) - set(files[DEFAULTS_CONF_FILE].keys())
            if keys:
                if RETURN_TYPE == 'json':
                    output.append(['error', "Keys missing in your 'defaults.conf' file: %r" % keys])
                else:
                    self.logger.error("Keys missing in your 'defaults.conf' file: %r", keys)

        if RETURN_TYPE == 'json':
            output.append(['info', 'Checking runtime configuration.'])
        else:
            self.logger.info('Checking runtime configuration.')
        http_proxy = files[DEFAULTS_CONF_FILE].get('http_proxy')
        https_proxy = files[DEFAULTS_CONF_FILE].get('https_proxy')
        # Either both are given or both are not given
        if (not http_proxy or not https_proxy) and not (http_proxy == https_proxy):
            if RETURN_TYPE == 'json':
                output.append(['warning', 'Incomplete configuration: Both http and https proxies must be set.'])
            else:
                self.logger.warning('Incomplete configuration: Both http and https proxies must be set.')
            retval = 1

        if RETURN_TYPE == 'json':
            output.append(['info', 'Checking runtime and pipeline configuration.'])
        else:
            self.logger.info('Checking runtime and pipeline configuration.')
        all_queues = set()
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # pipeline keys
            for field in ['description', 'group', 'module', 'name']:
                if field not in bot_config:
                    if RETURN_TYPE == 'json':
                        output.append(['warning', 'Bot %r has no %r.' % (bot_id, field)])
                    else:
                        self.logger.warning('Bot %r has no %r.', bot_id, field)
                    retval = 1
            if 'module' in bot_config and bot_config['module'] == 'bots.collectors.n6.collector_stomp':
                if RETURN_TYPE == 'json':
                    output.append(['warning',
                                   "The module 'bots.collectors.n6.collector_stomp' is deprecated and will be removed in "
                                   "version 2.0. Please use intelmq.bots.collectors."
                                   "stomp.collector instead for bot %r." % bot_id])
                else:
                    self.logger.warning("The module 'bots.collectors.n6.collector_stomp' is deprecated and will be removed in "
                                        "version 2.0. Please use intelmq.bots.collectors."
                                        "stomp.collector instead for bot %r." % bot_id)
            if 'run_mode' in bot_config and bot_config['run_mode'] not in ['continuous', 'scheduled']:
                message = "Bot %r has invalid `run_mode` %r. Must be 'continuous' or 'scheduled'."
                if RETURN_TYPE == 'json':
                    output.append(['warning', message % (bot_id, bot_config['run_mode'])])
                else:
                    self.logger.warning(message, bot_id, bot_config['run_mode'])
                    retval = 1
            if bot_id not in files[PIPELINE_CONF_FILE]:
                if RETURN_TYPE == 'json':
                    output.append(['error', 'Misconfiguration: No pipeline configuration found for %r.' % bot_id])
                else:
                    self.logger.error('Misconfiguration: No pipeline configuration found for %r.', bot_id)
                retval = 1
            else:
                if ('group' in bot_config and
                        bot_config['group'] in ['Collector', 'Parser', 'Expert']):
                    if ('destination-queues' not in files[PIPELINE_CONF_FILE][bot_id] or
                            (isinstance(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'], list) and
                             len(files[PIPELINE_CONF_FILE][bot_id]['destination-queues']) < 1) or
                            (isinstance(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'], dict) and
                             '_default' not in files[PIPELINE_CONF_FILE][bot_id]['destination-queues'])):
                        if RETURN_TYPE == 'json':
                            output.append(['error', 'Misconfiguration: No (default) destination queue for %r.' % bot_id])
                        else:
                            self.logger.error('Misconfiguration: No (default) destination queue for %r.', bot_id)
                        retval = 1
                    else:
                        all_queues = all_queues.union(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'])
                if ('group' in bot_config and
                        bot_config['group'] in ['Parser', 'Expert', 'Output']):
                    if ('source-queue' not in files[PIPELINE_CONF_FILE][bot_id] or
                            not isinstance(files[PIPELINE_CONF_FILE][bot_id]['source-queue'], str)):
                        if RETURN_TYPE == 'json':
                            output.append(['error', 'Misconfiguration: No source queue for %r.' % bot_id])
                        else:
                            self.logger.error('Misconfiguration: No source queue for %r.', bot_id)
                        retval = 1
                    else:
                        all_queues.add(files[PIPELINE_CONF_FILE][bot_id]['source-queue'])
                        all_queues.add(files[PIPELINE_CONF_FILE][bot_id]['source-queue'] + '-internal')
        if not no_connections:
            try:
                pipeline = PipelineFactory.create(self.parameters)
                pipeline.set_queues(None, "source")
                pipeline.connect()
                orphan_queues = "', '".join({a.decode() for a in pipeline.pipe.keys()} - all_queues)
            except Exception as exc:
                error = utils.error_message_from_exc(exc)
                if RETURN_TYPE == 'json':
                    output.append(['error',
                                   'Could not connect to redis pipeline: %s' % error])
                else:
                    self.logger.error('Could not connect to redis pipeline: %s', error)
                retval = 1
            else:
                if orphan_queues:
                    if RETURN_TYPE == 'json':
                        output.append(['warning', "Orphaned queues found: '%s'. Possible leftover from past reconfigurations "
                                       "without cleanup. Have a look at the FAQ at "
                                       "https://github.com/certtools/intelmq/blob/master/docs/FAQ.md" % orphan_queues])
                    else:
                        self.logger.warning("Orphaned queues found: '%s'. Possible leaftover from past reconfigurations "
                                            "without cleanup. Have a look at the FAQ at "
                                            "https://github.com/certtools/intelmq/blob/master/docs/FAQ.md", orphan_queues)

        if RETURN_TYPE == 'json':
            output.append(['info', 'Checking harmonization configuration.'])
        else:
            self.logger.info('Checking harmonization configuration.')
        for event_type, event_type_conf in files[HARMONIZATION_CONF_FILE].items():
            for harm_type_name, harm_type in event_type_conf.items():
                if "description" not in harm_type:
                    if RETURN_TYPE == 'json':
                        output.append(['warn', 'Missing description for type %r.' % harm_type_name])
                    else:
                        self.logger.warn('Missing description for type %r.', harm_type_name)
                if "type" not in harm_type:
                    if RETURN_TYPE == 'json':
                        output.append(['error', 'Missing type for type %r.' % harm_type_name])
                    else:
                        self.logger.error('Missing type for type %r.', harm_type_name)
                    retval = 1
                    continue
                if "regex" in harm_type:
                    try:
                        re.compile(harm_type['regex'])
                    except Exception as e:
                        if RETURN_TYPE == 'json':
                            output.append(['error', 'Invalid regex for type %r: %r.' % (harm_type_name, str(e))])
                        else:
                            self.logger.error('Invalid regex for type %r: %r.', harm_type_name, str(e))
                        retval = 1
                        continue
        extra_type = files[HARMONIZATION_CONF_FILE].get('event', {}).get('extra', {}).get('type')
        if extra_type != 'JSONDict':
            if RETURN_TYPE == 'json':
                output.append(['warning', "'extra' field needs to be of type 'JSONDict'."])
            else:
                self.logger.warning("'extra' field needs to be of type 'JSONDict'.")
            retval = 1

        if RETURN_TYPE == 'json':
            output.append(['info', 'Checking for bots.'])
        else:
            self.logger.info('Checking for bots.')
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # importable module
            try:
                bot_module = importlib.import_module(bot_config['module'])
            except ImportError as exc:
                if RETURN_TYPE == 'json':
                    output.append(['error', 'Incomplete installation: Bot %r not importable: %r.' % (bot_id, exc)])
                else:
                    self.logger.error('Incomplete installation: Bot %r not importable: %r.', bot_id, exc)
                retval = 1
                continue
            bot = getattr(bot_module, 'BOT')
            bot_parameters = files[DEFAULTS_CONF_FILE].copy()
            bot_parameters.update(bot_config['parameters'])
            bot_check = bot.check(bot_parameters)
            if bot_check:
                for log_line in bot_check:
                    if RETURN_TYPE == 'json':
                        output.append([log_line[0], "Bot %r: %s" % (bot_id, log_line[1])])
                    else:
                        getattr(self.logger, log_line[0])("Bot %r: %s" % (bot_id, log_line[1]))
        for group in files[BOTS_FILE].values():
            for bot_id, bot in group.items():
                if subprocess.call(['which', bot['module']], stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL):
                    if RETURN_TYPE == 'json':
                        output.append(['error', 'Incomplete installation: Executable %r for %r not found.' %
                                       (bot['module'], bot_id)])
                    else:
                        self.logger.error('Incomplete installation: Executable %r for %r not found.',
                                          bot['module'], bot_id)
                    retval = 1

        if RETURN_TYPE == 'json':
            if retval:
                return 0, {'status': 'error', 'lines': output}
            else:
                return 1, {'status': 'success', 'lines': output}
        else:
            if retval:
                self.logger.error('Some issues have been found, please check the above output.')
                return retval, 'error'
            else:
                self.logger.info('No issues found.')
                return retval, 'success'


def main():  # pragma: no cover
    x = IntelMQController(interactive=True)
    return x.run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
