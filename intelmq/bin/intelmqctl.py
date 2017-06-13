#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import importlib
import json
import os
import signal
import subprocess
import time

import pkg_resources
import psutil

from intelmq import (DEFAULTS_CONF_FILE, PIPELINE_CONF_FILE, RUNTIME_CONF_FILE,
                     STARTUP_CONF_FILE, SYSTEM_CONF_FILE, VAR_RUN_PATH,
                     BOTS_FILE)
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
    'disabled': '%s is disabled.',
    'starting': 'Starting %s...',
    'running': '%s is running.',
    'stopped': '%s is stopped.',
    'stopping': 'Stopping %s...',
    'reloading': 'Reloading %s ...',
    'reloaded': '%s is reloaded.',
}

ERROR_MESSAGES = {
    'starting': '%s failed to START.',
    'running': '%s is still running.',
    'stopped': '%s was NOT RUNNING.',
    'stopping': '%s failed to STOP.',
    'not found': '%s failed to START because the file cannot be found.',
}

LOG_LEVEL = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4,
}

RETURN_TYPES = ['text', 'json']
RETURN_TYPE = None
QUIET = False


def log_list_queues(queues):
    if RETURN_TYPE == 'text':
        for queue, counter in sorted(queues.items()):
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


def log_botnet_error(status):
    if RETURN_TYPE == 'text':
        logger.error(ERROR_MESSAGES[status], 'Botnet')


def log_botnet_message(status):
    if QUIET:
        return
    if RETURN_TYPE == 'text':
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

    def bot_run(self, bot_id, run_subcommand=None, console_type=None, message_action_kind=None, dryrun=None, msg=None):
        pid = self.__read_pidfile(bot_id)
        if pid and self.__status_process(pid):
            self.logger.warning("Main instance of the bot is running in the background and will be stopped; "
                                "when finished, we try to relaunch it again. "
                                "You may want to launch: 'intelmqctl stop {}' to prevent this message."
                                .format(bot_id))
            paused = True
            self.bot_stop(bot_id)
        else:
            paused = False

        log_bot_message('starting', bot_id)
        filename = self.PIDFILE.format(bot_id)
        with open(filename, 'w') as fp:
            fp.write(str(os.getpid()))

        try:
            BotDebugger(self.__runtime_configuration[bot_id], bot_id, run_subcommand,
                        console_type, dryrun, message_action_kind, msg)
            retval = 0
        except KeyboardInterrupt:
            print('Keyboard interrupt.')
            retval = 0
        except SystemExit as exc:
            print('Bot exited with code %s.' % exc)
            retval = exc

        self.__remove_pidfile(bot_id)
        if paused:
            self.bot_start(bot_id)
        return retval

    def bot_start(self, bot_id, getstatus=True):
        pid = self.__read_pidfile(bot_id)
        if pid:
            if self.__status_process(pid):
                log_bot_message('running', bot_id)
                return 'running'
            else:
                self.__remove_pidfile(bot_id)
        log_bot_message('starting', bot_id)
        module = self.__runtime_configuration[bot_id]['module']
        cmdargs = [module, bot_id]
        with open('/dev/null', 'w') as devnull:
            try:
                proc = psutil.Popen(cmdargs, stdout=devnull, stderr=devnull)
            except FileNotFoundError:
                log_bot_error("not found", bot_id)
                return 'stopped'
            else:
                filename = self.PIDFILE.format(bot_id)
                with open(filename, 'w') as fp:
                    fp.write(str(proc.pid))

        if getstatus:
            time.sleep(0.5)
            return self.bot_status(bot_id)

    def bot_stop(self, bot_id, getstatus=True):
        pid = self.__read_pidfile(bot_id)
        if not pid:
            if self.controller._is_enabled(bot_id):
                log_bot_error('stopped', bot_id)
                return 'stopped'
            else:
                log_bot_message('disabled', bot_id)
                return 'disabled'
        if not self.__status_process(pid):
            self.__remove_pidfile(bot_id)
            log_bot_error('stopped', bot_id)
            return 'stopped'
        log_bot_message('stopping', bot_id)
        proc = psutil.Process(int(pid))
        proc.send_signal(signal.SIGINT)

        if getstatus:
            time.sleep(0.5)
            if self.__status_process(pid):
                log_bot_error('running', bot_id)
                return 'running'
            self.__remove_pidfile(bot_id)
            log_bot_message('stopped', bot_id)
            return 'stopped'

    def bot_reload(self, bot_id, getstatus=True):
        pid = self.__read_pidfile(bot_id)
        if not pid:
            if self.controller._is_enabled(bot_id):
                log_bot_error('stopped', bot_id)
                return 'stopped'
            else:
                log_bot_message('disabled', bot_id)
                return 'disabled'
        if not self.__status_process(pid):
            self.__remove_pidfile(bot_id)
            log_bot_error('stopped', bot_id)
            return 'stopped'
        log_bot_message('reloading', bot_id)
        proc = psutil.Process(int(pid))
        proc.send_signal(signal.SIGHUP)
        if getstatus:
            time.sleep(0.5)
            if self.__status_process(pid):
                log_bot_message('running', bot_id)
                return 'running'
            log_bot_error('stopped', bot_id)
            return 'stopped'

    def bot_status(self, bot_id):
        pid = self.__read_pidfile(bot_id)
        if pid and self.__status_process(pid):
            log_bot_message('running', bot_id)
            return 'running'

        if self.controller._is_enabled(bot_id):
            log_bot_message('stopped', bot_id)
            return 'stopped'
        else:
            log_bot_message('disabled', bot_id)
            return 'disabled'

    def __read_pidfile(self, bot_id):
        filename = self.PIDFILE.format(bot_id)
        if self.__check_pidfile(bot_id):
            with open(filename, 'r') as fp:
                pid = fp.read()
            return pid.strip()
        return None

    def __check_pidfile(self, bot_id):
        filename = self.PIDFILE.format(bot_id)
        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as fp:
                    pid = fp.read()
                return int(pid.strip())
            except ValueError:
                return None
        return None

    def __remove_pidfile(self, bot_id):
        filename = self.PIDFILE.format(bot_id)
        os.remove(filename)

    def __status_process(self, pid):
        try:
            psutil.Process(int(pid))
            return True
        except psutil.NoSuchProcess:
            return False


PROCESS_MANAGER = {'intelmq': IntelMQProcessManager}


class IntelMQController():

    def __init__(self, interactive: bool=False, return_type: str="python", quiet: bool=False):
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
        try:
            logger = utils.log('intelmqctl', log_level='DEBUG')
        except (FileNotFoundError, PermissionError) as exc:
            logger = utils.log('intelmqctl', log_level='DEBUG', log_path=False)
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
            exit(1)
        DESCRIPTION = """
        description: intelmqctl is the tool to control intelmq system.

        Outputs are logged to /opt/intelmq/var/log/intelmqctl"""
        EPILOG = '''
        intelmqctl [start|stop|restart|status|reload] bot-id
        intelmqctl [start|stop|restart|status|reload]
        intelmqctl list [bots|queues]
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

Get a list of all configured bots:
    intelmqctl list bots

Get a list of all queues:
    intelmqctl list queues
If -q is given, only queues with more than one item are listed.

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
        self.parameters = Parameters()
        self.load_defaults_configuration()
        self.load_system_configuration()
        try:
            self.pipeline_configuration = utils.load_configuration(PIPELINE_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort('Error loading %r: %s' % (PIPELINE_CONF_FILE, exc))

        try:
            self.runtime_configuration = utils.load_configuration(RUNTIME_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort('Error loading %r: %s' % (RUNTIME_CONF_FILE, exc))

        if os.path.exists(STARTUP_CONF_FILE):
            self.logger.warning('Deprecated startup.conf file found, please migrate to runtime.conf soon.')
            with open(STARTUP_CONF_FILE, 'r') as fp:
                startup = json.load(fp)
                for bot_id, bot_values in startup.items():
                    if 'parameters' in self.runtime_configuration[bot_id]:  # pragma: no cover
                        self.abort('Mixed setup of new runtime.conf and old startup.conf'
                                   ' found. Ignoring startup.conf, please fix this!')
                    params = self.runtime_configuration[bot_id].copy()
                    self.runtime_configuration[bot_id].clear()
                    self.runtime_configuration[bot_id]['parameters'] = params
                    self.runtime_configuration[bot_id].update(bot_values)
            if self.write_updated_runtime_config(filename=RUNTIME_CONF_FILE + '.new'):
                self.logger.info('%r with new format written.', RUNTIME_CONF_FILE + '.new')

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
            parser_list.add_argument('kind', choices=['bots', 'queues'])
            parser_list.add_argument('--quiet', '-q', action='store_const',
                                     help='Only list non-empty queues',
                                     const=True)
            parser_list.set_defaults(func=self.list)

            subparsers.add_parser('check', help='Check installation and configuration')

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
            parser_check.set_defaults(func=self.check)

            parser_help = subparsers.add_parser('help',
                                                help='Show the help')
            parser_help.set_defaults(func=parser.print_help)

            parser_start = subparsers.add_parser('start', help='Start a bot or botnet')
            parser_start.add_argument('bot_id', nargs='?',
                                      choices=self.runtime_configuration.keys())
            parser_start.set_defaults(func=self.bot_start)

            parser_stop = subparsers.add_parser('stop', help='Stop a bot or botnet')
            parser_stop.add_argument('bot_id', nargs='?',
                                     choices=self.runtime_configuration.keys())
            parser_stop.set_defaults(func=self.bot_stop)

            parser_restart = subparsers.add_parser('restart', help='Restart a bot or botnet')
            parser_restart.add_argument('bot_id', nargs='?',
                                        choices=self.runtime_configuration.keys())
            parser_restart.set_defaults(func=self.bot_restart)

            parser_reload = subparsers.add_parser('reload', help='Reload a bot or botnet')
            parser_reload.add_argument('bot_id', nargs='?',
                                       choices=self.runtime_configuration.keys())
            parser_reload.set_defaults(func=self.bot_reload)

            parser_status = subparsers.add_parser('status', help='Status of a bot or botnet')
            parser_status.add_argument('bot_id', nargs='?',
                                       choices=self.runtime_configuration.keys())
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

    def load_system_configuration(self):
        if os.path.exists(SYSTEM_CONF_FILE):
            try:
                config = utils.load_configuration(SYSTEM_CONF_FILE)
            except ValueError as exc:  # pragma: no cover
                self.abort('Error loading %r: %s' % (SYSTEM_CONF_FILE, exc))
            for option, value in config.items():
                setattr(self.parameters, option, value)

    def load_defaults_configuration(self):
        # Load defaults configuration
        try:
            config = utils.load_configuration(DEFAULTS_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            self.abort('Error loading %r: %s' % (DEFAULTS_CONF_FILE, exc))
        for option, value in config.items():
            setattr(self.parameters, option, value)

    def run(self):
        results = None
        args = self.parser.parse_args()
        if 'func' not in args:
            exit(self.parser.print_help())
        args_dict = vars(args).copy()

        global RETURN_TYPE, QUIET
        RETURN_TYPE, QUIET = args.type, args.quiet
        del args_dict['type'], args_dict['quiet'], args_dict['func']
        results = args.func(**args_dict)

        if RETURN_TYPE == 'json':
            print(json.dumps(results))
        if type(results) is int:
            return results
        elif results == 'error':
            return 1

    def bot_run(self, **kwargs):
        return self.bot_process_manager.bot_run(**kwargs)

    def bot_start(self, bot_id, getstatus=True):
        if bot_id is None:
            return self.botnet_start()
        else:
            return self.bot_process_manager.bot_start(bot_id, getstatus)

    def bot_stop(self, bot_id, getstatus=True):
        if bot_id is None:
            return self.botnet_stop()
        else:
            return self.bot_process_manager.bot_stop(bot_id, getstatus)

    def bot_reload(self, bot_id, getstatus=True):
        if bot_id is None:
            return self.botnet_reload()
        else:
            return self.bot_process_manager.bot_reload(bot_id, getstatus)

    def bot_restart(self, bot_id):
        if bot_id is None:
            return self.botnet_restart()
        else:
            status_stop = self.bot_stop(bot_id)
            status_start = self.bot_start(bot_id)
            return (status_stop, status_start)

    def bot_status(self, bot_id):
        if bot_id is None:
            return self.botnet_status()
        else:
            return self.bot_process_manager.bot_status(bot_id)

    def bot_enable(self, bot_id):
        self.runtime_configuration[bot_id]['enabled'] = True
        self.write_updated_runtime_config()

    def bot_disable(self, bot_id):
        self.runtime_configuration[bot_id]['enabled'] = False
        self.write_updated_runtime_config()

    def _is_enabled(self, bot_id):
        return self.runtime_configuration[bot_id].get('enabled', True)

    def botnet_start(self):
        botnet_status = {}
        bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            if self.runtime_configuration[bot_id].get('enabled', True):
                self.bot_start(bot_id, getstatus=False)
            else:
                log_bot_message('disabled', bot_id)
                botnet_status[bot_id] = 'disabled'

        time.sleep(0.75)
        for bot_id in bots:
            if self.runtime_configuration[bot_id].get('enabled', True):
                botnet_status[bot_id] = self.bot_status(bot_id)

        log_botnet_message('running')
        return botnet_status

    def botnet_stop(self):
        botnet_status = {}
        log_botnet_message('stopping')
        bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            self.bot_stop(bot_id, getstatus=False)

        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)

        log_botnet_message('stopped')
        return botnet_status

    def botnet_reload(self):
        botnet_status = {}
        log_botnet_message('reloading')
        bots = sorted(self.runtime_configuration.keys())
        for bot_id in bots:
            self.bot_reload(bot_id, getstatus=False)

        time.sleep(0.75)
        for bot_id in bots:
            botnet_status[bot_id] = self.bot_status(bot_id)
        log_botnet_message('reloaded')
        return botnet_status

    def botnet_restart(self):
        self.botnet_stop()
        return self.botnet_start()

    def botnet_status(self):
        botnet_status = {}
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = self.bot_status(bot_id)
        return botnet_status

    def list(self, kind=None):
        if kind == 'queues':
            return self.list_queues()
        elif kind == 'bots':
            return self.list_bots()

    def abort(self, message):
        if self.interactive:
            exit(message)
        else:
            raise ValueError(message)

    def write_updated_runtime_config(self, filename=RUNTIME_CONF_FILE):
        if os.path.exists(STARTUP_CONF_FILE):
            self.abort('Can\'t update runtime configuration, startup.conf found.')
        try:
            with open(RUNTIME_CONF_FILE, 'w') as handle:
                json.dump(self.runtime_configuration, fp=handle, indent=4, sort_keys=True,
                          separators=(',', ': '))
        except PermissionError:
            self.abort('Can\'t update runtime configuration: Permission denied.')
        return True

    def list_bots(self):
        """
        Lists all configured bots from startup.conf with bot id and
        description.

        If description is not set, None is used instead.
        """
        if RETURN_TYPE == 'text':
            for bot_id in sorted(self.runtime_configuration.keys()):
                print("Bot ID: {}\nDescription: {}"
                      "".format(bot_id, self.runtime_configuration[bot_id].get('description')))
        return [{'id': bot_id,
                 'description': self.runtime_configuration[bot_id].get('description')}
                for bot_id in sorted(self.runtime_configuration.keys())]

    def get_queues(self):
        source_queues = set()
        destination_queues = set()
        internal_queues = set()

        for botid, value in self.pipeline_configuration.items():
            if 'source-queue' in value:
                source_queues.add(value['source-queue'])
                internal_queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                destination_queues.update(value['destination-queues'])

        all_queues = source_queues.union(destination_queues).union(internal_queues)

        return source_queues, destination_queues, internal_queues, all_queues

    def list_queues(self):
        source_queues, destination_queues, internal_queues, all_queues = self.get_queues()
        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(None, "source")
        pipeline.connect()

        counters = pipeline.count_queued_messages(*all_queues)
        log_list_queues(counters)

        return_dict = dict()
        for bot_id, info in self.pipeline_configuration.items():
            return_dict[bot_id] = dict()

            if 'source-queue' in info:
                return_dict[bot_id]['source_queue'] = (
                    info['source-queue'], counters[info['source-queue']])
                return_dict[bot_id]['internal_queue'] = counters[info['source-queue'] + '-internal']

            if 'destination-queues' in info:
                return_dict[bot_id]['destination_queues'] = list()
                for dest_queue in info['destination-queues']:
                    return_dict[bot_id]['destination_queues'].append(
                        (dest_queue, counters[dest_queue]))

        return return_dict

    def clear_queue(self, queue):
        """
        Clears an exiting queue.

        First checks if the queue does exist in the pipeline configuration.
        """
        logger.info("Clearing queue %s", queue)
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
            logger.error("Queue %s does not exist!", queue)
            return 'not-found'

        try:
            pipeline.clear_queue(queue)
            logger.info("Successfully cleared queue %s.", queue)
            return 'success'
        except Exception:  # pragma: no cover
            logger.exception("Error while clearing queue %s.",
                             queue)
            return 'error'

    def read_bot_log(self, bot_id, log_level, number_of_lines):
        if self.parameters.logging_handler == 'file':
            bot_log_path = os.path.join(self.parameters.logging_path,
                                        bot_id + '.log')
            if not os.path.isfile(bot_log_path):
                logger.error("Log path not found: %s", bot_log_path)
                return []
        elif self.parameters.logging_handler == 'syslog':
            bot_log_path = '/var/log/syslog'

        if not os.access(bot_log_path, os.R_OK):
            self.logger.error('File %r is not readable.', bot_log_path)
            return 'error'

        messages = list()

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
        return messages[::-1]

    def check(self):
        retval = 0
        # loading files and syntax check
        files = {DEFAULTS_CONF_FILE: None, PIPELINE_CONF_FILE: None,
                 RUNTIME_CONF_FILE: None, BOTS_FILE: None}
        self.logger.info('Reading configuration files.')
        for filename in files:
            try:
                with open(filename) as file_handle:
                    files[filename] = json.load(file_handle)
            except (IOError, ValueError) as exc:  # pragma: no cover
                self.logger.error('Coud not load %r: %s.', filename, exc)
                retval = 1
        if retval:
            self.logger.error('Fatal errors occurred.')
            return retval

        if os.path.exists(STARTUP_CONF_FILE):
            self.logger.warning('Deprecated startup.conf file found, migrate to runtime.conf.')
            retval = 1
        if os.path.exists(SYSTEM_CONF_FILE):
            self.logger.warning('Deprecated system.conf file found, migrate to defaults.conf.')
            retval = 1

        self.logger.info('Checking runtime configuration.')
        http_proxy = files[DEFAULTS_CONF_FILE].get('http_proxy')
        https_proxy = files[DEFAULTS_CONF_FILE].get('https_proxy')
        # Either both are given or both are not given
        if (not http_proxy or not https_proxy) and not (http_proxy == https_proxy):
            self.logger.warning('Incomplete configuration: Both http and https proxies must be set.')
            retval = 1

        self.logger.info('Checking pipeline configuration.')
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # pipeline keys
            for field in ['description', 'group', 'module', 'name']:
                if field not in bot_config:
                    self.logger.warning('Bot %r has no %r.', bot_id, field)
                    retval = 1
            if bot_id not in files[PIPELINE_CONF_FILE]:
                self.logger.error('Misconfiguration: No pipeline configuration found for %r.', bot_id)
                retval = 1
            else:
                if ('group' in bot_config and
                        bot_config['group'] in ['Collector', 'Parser', 'Expert'] and
                        ('destination-queues' not in files[PIPELINE_CONF_FILE][bot_id] or
                         (not isinstance(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'], list) or
                          len(files[PIPELINE_CONF_FILE][bot_id]['destination-queues']) < 1))):
                    self.logger.error('Misconfiguration: No destination queues for %r.', bot_id)
                    retval = 1
                if ('group' in bot_config and
                        bot_config['group'] in ['Parser', 'Expert', 'Output'] and
                        ('source-queue' not in files[PIPELINE_CONF_FILE][bot_id] or
                         not isinstance(files[PIPELINE_CONF_FILE][bot_id]['source-queue'], str))):
                    self.logger.error('Misconfiguration: No source queue for %r.', bot_id)
                    retval = 1

        self.logger.info('Checking for bots.')
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # importable module
            try:
                importlib.import_module(bot_config['module'])
            except ImportError:
                self.logger.error('Incomplete installation: Module %r not importable.', bot_id)
                retval = 1
        for group in files[BOTS_FILE].values():
            for bot_id, bot in group.items():
                if subprocess.call(['which', bot['module']], stdout=subprocess.DEVNULL):
                    self.logger.error('Incomplete installation: Executable %r for %r not found.',
                                      bot['module'], bot_id)
                    retval = 1

        if retval:
            self.logger.error('Some issues have been found, please check the above output.')
        else:
            self.logger.info('No issues found.')

        return retval


def main():  # pragma: no cover
    x = IntelMQController(interactive=True)
    return x.run()


if __name__ == "__main__":  # pragma: no cover
    exit(main())
