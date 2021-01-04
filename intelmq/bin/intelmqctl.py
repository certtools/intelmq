# -*- coding: utf-8 -*-
import argparse
import datetime
import distutils.version
import getpass
import http.client
import importlib
import json
import logging
import os
import re
import signal
import socket
import subprocess
import sys
import textwrap
import traceback
import time
import xmlrpc.client
from collections import OrderedDict

import pkg_resources
from termstyle import green

from intelmq import (BOTS_FILE, DEFAULT_LOGGING_LEVEL, DEFAULTS_CONF_FILE,  # noqa: F401
                     HARMONIZATION_CONF_FILE, PIPELINE_CONF_FILE,
                     RUNTIME_CONF_FILE, VAR_RUN_PATH, STATE_FILE_PATH,
                     DEFAULT_LOGGING_PATH, __version_info__,
                     CONFIG_DIR, ROOT_DIR)
from intelmq.lib import utils
from intelmq.lib.bot_debugger import BotDebugger
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.pipeline import PipelineFactory
import intelmq.lib.upgrades as upgrades
from typing import Union, Iterable

try:
    import psutil
except ImportError:
    psutil = None


class Parameters(object):
    pass


STATUSES = {
    'starting': 0,
    'running': 1,
    'stopping': 2,
    'stopped': 3,
}

MESSAGES = {
    'enabled': 'Bot %s is enabled.',
    'disabled': 'Bot %s is disabled.',
    'starting': 'Starting %s...',
    'running': green('Bot %s is running.'),
    'stopped': 'Bot %s is stopped.',
    'stopping': 'Stopping bot %s...',
    'reloading': 'Reloading bot %s ...',
    'enabling': 'Enabling %s.',
    'disabling': 'Disabling %s.',
    'reloaded': 'Bot %s is reloaded.',
    'restarting': 'Restarting %s...',
}

ERROR_MESSAGES = {
    'starting': 'Bot %s failed to START.',
    'running': 'Bot %s is still running.',
    'stopped': 'Bot %s was NOT RUNNING.',
    'stopping': 'Bot %s failed to STOP.',
    'not found': ('Bot %s FAILED to start because the executable cannot be found. '
                  'Check your PATH variable and your the installation.'),
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

        if psutil is None:
            raise MissingDependencyError('psutil')

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
            self.logger.info("Main instance of the bot is running in the background and will be stopped; "
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

        output = ""
        try:
            bd = BotDebugger(self.__runtime_configuration[bot_id], bot_id, run_subcommand,
                             console_type, message_action_kind, dryrun, msg, show_sent,
                             loglevel=loglevel)
            output = bd.run()
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

        return retval, output

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
                # Wait for up to 2 seconds until the bot stops, #1434
                starttime = time.time()
                remaining = 2
                status = self.__status_process(pid, module, bot_id)
                while status is True and remaining > 0:
                    status = self.__status_process(pid, module, bot_id)
                    time.sleep(0.1)
                    remaining = 2 - (time.time() - starttime)

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

    @staticmethod
    def _interpret_commandline(pid: int, cmdline: Iterable[str],
                               module: str, bot_id: str) -> Union[bool, str]:
        """
        Separate function to allow easy testing

        Parameters
        ----------
        pid : int
            Process ID, used for return values (error messages) only.
        cmdline : Iterable[str]
            The command line of the process.
        module : str
            The module of the bot.
        bot_id : str
            The ID of the bot.

        Returns
        -------
        Union[bool, str]
            DESCRIPTION.
        """
        if len(cmdline) > 2 and cmdline[1].endswith('/%s' % module):
            if cmdline[2] == bot_id:
                return True
            else:
                return False
        elif (len(cmdline) > 3 and cmdline[1].endswith('/intelmqctl') and
              cmdline[2] == 'run'):
            if cmdline[3] == bot_id:
                return True
            else:
                return False
        elif len(cmdline) > 1:
            return 'Commandline of the process %d with commandline %r could not be interpreted.' % (pid, cmdline)
        else:
            return 'Unhandled error checking the process %d with commandline %r.' % (pid, cmdline)

    def __status_process(self, pid, module, bot_id):
        try:
            proc = psutil.Process(int(pid))
            cmdline = proc.cmdline()
            return IntelMQProcessManager._interpret_commandline(pid, cmdline, module, bot_id)
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied:
            return 'Could not get status of process: Access denied.'
        # let every other exception pass


class SupervisorProcessManager:
    class RpcFaults:
        UNKNOWN_METHOD = 1
        INCORRECT_PARAMETERS = 2
        BAD_ARGUMENTS = 3
        SIGNATURE_UNSUPPORTED = 4
        SHUTDOWN_STATE = 6
        BAD_NAME = 10
        BAD_SIGNAL = 11
        NO_FILE = 20
        NOT_EXECUTABLE = 21
        FAILED = 30
        ABNORMAL_TERMINATION = 40
        SPAWN_ERROR = 50
        ALREADY_STARTED = 60
        NOT_RUNNING = 70
        SUCCESS = 80
        ALREADY_ADDED = 90
        STILL_RUNNING = 91
        CANT_REREAD = 92

    class ProcessState:
        STOPPED = 0
        STARTING = 10
        RUNNING = 20
        BACKOFF = 30
        STOPPING = 40
        EXITED = 100
        FATAL = 200
        UNKNOWN = 1000

        @staticmethod
        def is_running(state: int) -> bool:
            return state in (
                SupervisorProcessManager.ProcessState.STARTING,
                SupervisorProcessManager.ProcessState.RUNNING,
                SupervisorProcessManager.ProcessState.BACKOFF)

    DEFAULT_SOCKET_PATH = "/var/run/supervisor.sock"
    SUPERVISOR_GROUP = "intelmq"
    __supervisor_xmlrpc = None

    def __init__(self, runtime_configuration: dict, logger: logging.Logger, controller) -> None:
        self.__runtime_configuration = runtime_configuration
        self.__logger = logger
        self.__controller = controller

    def bot_run(self, bot_id, run_subcommand=None, console_type=None, message_action_kind=None, dryrun=None, msg=None,
                show_sent=None, loglevel=None):
        paused = False
        state = self._get_process_state(bot_id)
        if state in (self.ProcessState.STARTING, self.ProcessState.RUNNING, self.ProcessState.BACKOFF):
            self.__logger.warning("Main instance of the bot is running in the background and will be stopped; "
                                  "when finished, we try to relaunch it again. "
                                  "You may want to launch: 'intelmqctl stop {}' to prevent this message."
                                  .format(bot_id))
            paused = True
            self.bot_stop(bot_id)

        log_bot_message("starting", bot_id)

        output = ""
        try:
            bd = BotDebugger(self.__runtime_configuration[bot_id], bot_id, run_subcommand,
                             console_type, message_action_kind, dryrun, msg, show_sent,
                             loglevel=loglevel)
            output = bd.run()
            retval = 0
        except KeyboardInterrupt:
            print("Keyboard interrupt.")
            retval = 0
        except SystemExit as exc:
            print("Bot exited with code %s." % exc.code)
            retval = exc.code

        if paused:
            self.bot_start(bot_id)

        return retval, output

    def bot_start(self, bot_id: str, getstatus: bool = True):
        state = self._get_process_state(bot_id)
        if state is not None:
            if state == self.ProcessState.RUNNING:
                log_bot_message("running", bot_id)
                return "running"

            elif not self.ProcessState.is_running(state):
                self._remove_bot(bot_id)

        log_bot_message("starting", bot_id)
        self._create_and_start_bot(bot_id)

        if getstatus:
            return self.bot_status(bot_id)

    def bot_stop(self, bot_id: str, getstatus: bool = True):
        state = self._get_process_state(bot_id)
        if state is None:
            if not self.__controller._is_enabled(bot_id):
                log_bot_message("disabled", bot_id)
                return "disabled"
            else:
                log_bot_error("stopped", bot_id)
                return "stopped"

        if not self.ProcessState.is_running(state):
            self._remove_bot(bot_id)
            log_bot_error("stopped", bot_id)
            return "stopped"

        log_bot_message("stopping", bot_id)

        self._get_supervisor().supervisor.stopProcess(self._process_name(bot_id))
        self._remove_bot(bot_id)

        if getstatus:
            return self.bot_status(bot_id)

    def bot_reload(self, bot_id: str, getstatus: bool = True):
        state = self._get_process_state(bot_id)
        if state is None:
            if not self.__controller._is_enabled(bot_id):
                log_bot_message("disabled", bot_id)
                return "disabled"
            else:
                log_bot_error("stopped", bot_id)
                return "stopped"

        if not self.ProcessState.is_running(state):
            self._remove_bot(bot_id)
            log_bot_error("stopped", bot_id)
            return "stopped"

        log_bot_message("reloading", bot_id)

        try:
            self._get_supervisor().supervisor.signalProcess(self._process_name(bot_id), "HUP")
        except xmlrpc.client.Fault as e:
            if e.faultCode == self.RpcFaults.UNKNOWN_METHOD:
                self._abort("Supervisor does not support signalProcess method, that was added in supervisor 3.2.0. "
                            "Reloading bots will not work.")
            else:
                raise e

        if getstatus:
            return self.bot_status(bot_id)

    def bot_status(self, bot_id: str) -> str:
        state = self._get_process_state(bot_id)
        if state is None:
            if not self.__controller._is_enabled(bot_id):
                log_bot_message("disabled", bot_id)
                return "disabled"
            else:
                log_bot_message("stopped", bot_id)
                return "stopped"

        if state == self.ProcessState.STARTING:
            # If process is still starting, try check it later
            time.sleep(0.1)
            return self.bot_status(bot_id)

        elif state == self.ProcessState.RUNNING:
            log_bot_message("running", bot_id)
            return "running"

        elif state == self.ProcessState.STOPPING:
            log_bot_error("stopping", bot_id)
            return "stopping"

        else:
            log_bot_message("stopped", bot_id)
            return "stopped"

    def _create_and_start_bot(self, bot_id: str) -> None:
        module = self.__runtime_configuration[bot_id]["module"]
        cmdargs = (module, bot_id)

        self._get_supervisor().twiddler.addProgramToGroup(self.SUPERVISOR_GROUP, bot_id, {
            "command": " ".join(cmdargs),
            "stopsignal": "INT",
        })

    def _remove_bot(self, bot_id: str) -> None:
        self._get_supervisor().twiddler.removeProcessFromGroup(self.SUPERVISOR_GROUP, bot_id)

    def _get_process_state(self, bot_id: str):
        try:
            return self._get_supervisor().supervisor.getProcessInfo(self._process_name(bot_id))["state"]
        except xmlrpc.client.Fault as e:
            if e.faultCode == self.RpcFaults.BAD_NAME:  # Process does not exists
                return None
            raise

    def _get_supervisor(self) -> xmlrpc.client.ServerProxy:
        class UnixStreamHTTPConnection(http.client.HTTPConnection):
            def connect(self):
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(self.host)

        class UnixStreamTransport(xmlrpc.client.Transport, object):
            def __init__(self, socket_path):
                self.socket_path = socket_path
                super(UnixStreamTransport, self).__init__()

            def make_connection(self, host):
                return UnixStreamHTTPConnection(self.socket_path)

        if not self.__supervisor_xmlrpc:
            socket_path = os.environ.get("SUPERVISOR_SOCKET", self.DEFAULT_SOCKET_PATH)

            if not os.path.exists(socket_path):
                self._abort("Socket '{}' does not exists. Is supervisor running?".format(socket_path))

            if not os.access(socket_path, os.W_OK):
                current_user = getpass.getuser()
                self._abort("Socket '{}' is not writable. "
                            "Has user '{}' write permission?".format(socket_path, current_user))

            self.__supervisor_xmlrpc = xmlrpc.client.ServerProxy(
                "http://none",
                transport=UnixStreamTransport(socket_path)
            )

            supervisor_version = self.__supervisor_xmlrpc.supervisor.getSupervisorVersion()
            self.__logger.debug("Connected to supervisor {} named '{}' (API version {})".format(
                supervisor_version,
                self.__supervisor_xmlrpc.supervisor.getIdentification(),
                self.__supervisor_xmlrpc.supervisor.getAPIVersion()
            ))

            if distutils.version.StrictVersion(supervisor_version) < distutils.version.StrictVersion("3.2.0"):
                self.__logger.warning("Current supervisor version is supported, but reloading bots will not work. "
                                      "Please upgrade supervisor to version 3.2.0 or higher.")

            supervisor_state = self.__supervisor_xmlrpc.supervisor.getState()["statename"]
            if supervisor_state != "RUNNING":
                raise Exception("Unexpected supervisor state {}".format(supervisor_state))

            try:
                self.__supervisor_xmlrpc.twiddler.getAPIVersion()
            except xmlrpc.client.Fault as e:
                if e.faultCode == self.RpcFaults.UNKNOWN_METHOD:
                    self._abort("Twiddler is not supported. Is Twiddler for supervisor installed and enabled?")
                else:
                    raise e

            if self.SUPERVISOR_GROUP not in self.__supervisor_xmlrpc.twiddler.getGroupNames():
                self._abort("Supervisor`s process group '{}' is not defined. "
                            "It must be created manually in supervisor config.".format(self.SUPERVISOR_GROUP))

        return self.__supervisor_xmlrpc

    def _process_name(self, bot_id: str) -> str:
        return "{}:{}".format(self.SUPERVISOR_GROUP, bot_id)

    def _abort(self, message: str):
        self.__controller.abort(message)


PROCESS_MANAGER = {'intelmq': IntelMQProcessManager, 'supervisor': SupervisorProcessManager}


class IntelMQController():

    def __init__(self, interactive: bool = False, return_type: str = "python", quiet: bool = False,
                 no_file_logging: bool = False, drop_privileges: bool = True) -> None:
        """
        Initializes intelmqctl.

        Parameters:
            interactive: for cli-interface true, functions can exits, parameters are used
            return_type: 'python': no special treatment, can be used for use by other
                python code
                'text': user-friendly output for cli, default for interactive use
                'json': machine-readable output for managers
            quiet: False by default, can be activated for cron jobs etc.
            no_file_logging: do not log to the log file
            drop_privileges: Drop privileges and fail if it did not work.
        """
        self.logging_level = DEFAULT_LOGGING_LEVEL
        self.interactive = interactive
        global RETURN_TYPE
        RETURN_TYPE = return_type
        global logger
        global QUIET
        QUIET = quiet
        self.parameters = Parameters()

        # Try to get logging_level from defaults configuration, else use default (defined above)
        defaults_loading_exc = None
        try:
            self.load_defaults_configuration()
        except Exception as exc:
            defaults_loading_exc = exc
            logging_level_stream = 'DEBUG'
        else:
            self.logging_level = self.parameters.logging_level.upper()
        # make sure that logging_level_stream is always at least INFO or more verbose
        # otherwise the output on stdout/stderr is less than the user expects
        logging_level_stream = self.logging_level if self.logging_level == 'DEBUG' else 'INFO'

        try:
            if no_file_logging:
                raise FileNotFoundError
            logger = utils.log('intelmqctl', log_level=self.logging_level,
                               log_format_stream=utils.LOG_FORMAT_SIMPLE,
                               logging_level_stream=logging_level_stream,
                               log_max_size=getattr(self.parameters, "logging_max_size", 0),
                               log_max_copies=getattr(self.parameters, "logging_max_copies", None))
        except (FileNotFoundError, PermissionError) as exc:
            logger = utils.log('intelmqctl', log_level=self.logging_level, log_path=False,
                               log_format_stream=utils.LOG_FORMAT_SIMPLE,
                               logging_level_stream=logging_level_stream)
            logger.error('Not logging to file: %s', exc)
        self.logger = logger
        if defaults_loading_exc:
            self.logger.exception('Loading the defaults configuration failed!',
                                  exc_info=defaults_loading_exc)

        if drop_privileges and not utils.drop_privileges():
            self.abort('IntelMQ must not run as root. Dropping privileges did not work.')

        APPNAME = "intelmqctl"
        try:
            VERSION = pkg_resources.get_distribution("intelmq").version
        except pkg_resources.DistributionNotFound:  # pragma: no cover
            # can only happen in interactive mode
            self.logger.error('No valid IntelMQ installation found: DistributionNotFound')
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

        # stolen functions from the bot file
        # this will not work with various instances of REDIS
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

            parser.add_argument('--quiet', '-q', action='store_true',
                                help='Quiet mode, useful for reloads initiated '
                                     'scripts like logrotate')

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
            parser_list.set_defaults(func=self.list)

            parser_clear = subparsers.add_parser('clear', help='Clear a queue')
            parser_clear.add_argument('queue', help='queue name')
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

    def load_defaults_configuration(self, silent=False):
        # Load defaults configuration
        try:
            config = utils.load_configuration(DEFAULTS_CONF_FILE)
        except ValueError as exc:  # pragma: no cover
            if not silent:
                self.abort('Error loading %r: %s' % (DEFAULTS_CONF_FILE, exc))
        for option, value in config.items():
            setattr(self.parameters, option, value)

        # TODO: Rewrite variables with env. variables ( CURRENT IMPLEMENTATION NOT FINAL )
        # "destination_pipeline_host": "127.0.0.1",
        # "source_pipeline_host": "127.0.0.1",
        if os.getenv('INTELMQ_IS_DOCKER', None):
            pipeline_host = os.getenv('INTELMQ_PIPELINE_HOST')
            if pipeline_host:
                setattr(self.parameters, 'destination_pipeline_host', pipeline_host)
                setattr(self.parameters, 'source_pipeline_host', pipeline_host)

    def run(self):
        results = None
        args = self.parser.parse_args()
        if 'func' not in args:
            sys.exit(self.parser.print_help())
        args_dict = vars(args).copy()

        global RETURN_TYPE, QUIET
        RETURN_TYPE, QUIET = args.type, args.quiet
        del args_dict['type'], args_dict['quiet'], args_dict['func']
        self.logging_level = 'WARNING' if QUIET else 'INFO'
        self.logger.setLevel(self.logging_level)

        retval, results = args.func(**args_dict)

        if RETURN_TYPE == 'json':
            print(json.dumps(results))
        return retval

    def bot_run(self, **kwargs):
        # the bot_run method is special in that it mixes plain text
        # and json in its output, therefore it is printed here
        # and not in the calling `run` method.
        retval, results = self.bot_process_manager.bot_run(**kwargs)
        print(results)
        return retval, None

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
            if self.bot_process_manager.bot_status(bot_id) == 'disabled':
                return 0, 'disabled'
            status = self.bot_process_manager.bot_reload(bot_id, getstatus)
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
            status = self.bot_process_manager.bot_status(bot_id)
            if status in ['running', 'disabled']:
                return 0, status
            else:
                return 1, status

    def bot_enable(self, bot_id):
        if self._is_enabled(bot_id):
            log_bot_message('enabled', bot_id)
        else:
            log_bot_message('enabling', bot_id)
            self.runtime_configuration[bot_id]['enabled'] = True
            self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def bot_disable(self, bot_id):
        """
        If Bot is already disabled, the "Bot ... is disabled" message is
        printed by the wrapping function already.
        """
        if self._is_enabled(bot_id):
            log_bot_message('disabling', bot_id)
            self.runtime_configuration[bot_id]['enabled'] = False
            self.write_updated_runtime_config()
        return self.bot_status(bot_id)

    def _is_enabled(self, bot_id):
        return self.runtime_configuration[bot_id].get('enabled', True)

    def botnet_start(self, group=None):
        botnet_status = {}
        log_botnet_message('starting', group)

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
        log_botnet_message('restarting')
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

    def list(self, kind=None, non_zero=False, count=False):
        if kind == 'queues':
            return self.list_queues(non_zero=non_zero, count=count)
        elif kind == 'bots':
            return self.list_bots(non_zero=non_zero)
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
            utils.write_configuration(filename, self.runtime_configuration)
        except PermissionError:
            self.abort('Can\'t update runtime configuration: Permission denied.')
        return True

    def list_bots(self, non_zero=False):
        """
        Lists all configured bots from runtime.conf with bot id and
        description.

        If description is not set, None is used instead.
        """
        if RETURN_TYPE == 'text':
            for bot_id in sorted(self.runtime_configuration.keys(), key=str.lower):
                if non_zero and not self.runtime_configuration[bot_id].get('enabled'):
                    continue
                if QUIET:
                    print(bot_id)
                else:
                    print("Bot ID: {}\nDescription: {}"
                          "".format(bot_id, self.runtime_configuration[bot_id].get('description')))
        return 0, [{'id': bot_id,
                    'description': self.runtime_configuration[bot_id].get('description')}
                   for bot_id in sorted(self.runtime_configuration.keys())]

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

        for botid, value in self.pipeline_configuration.items():
            if 'source-queue' in value:
                source_queues.add(value['source-queue'])
                if with_internal_queues:
                    internal_queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                # flattens ["one", "two"] → {"one", "two"}, {"_default": "one", "other": ["two", "three"]} → {"one", "two", "three"}
                destination_queues.update(utils.flatten_queues(value['destination-queues']))

        all_queues = source_queues.union(destination_queues).union(internal_queues)

        return source_queues, destination_queues, internal_queues, all_queues

    def list_queues(self, non_zero=False, count=False):
        pipeline = PipelineFactory.create(self.parameters, logger=self.logger)
        pipeline.set_queues(None, "source")
        pipeline.connect()
        source_queues, destination_queues, internal_queues,\
            all_queues = self.get_queues(with_internal_queues=pipeline.has_internal_queues)

        counters = pipeline.count_queued_messages(*all_queues)
        pipeline.disconnect()
        if RETURN_TYPE == 'text':
            for queue, counter in sorted(counters.items(), key=lambda x: str.lower(x[0])):
                if (counter or not non_zero) and not count:
                    logger.info("%s - %s", queue, counter)
            if count:
                logger.info("%s", sum(counters.values()))

        return_dict = {}
        if count:
            return_dict = {'total-messages': sum(counters.values())}
        else:
            for bot_id, info in self.pipeline_configuration.items():
                return_dict[bot_id] = {}

                if 'source-queue' in info:
                    return_dict[bot_id]['source_queue'] = (
                        info['source-queue'], counters[info['source-queue']])
                    if pipeline.has_internal_queues:
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
        pipeline = PipelineFactory.create(self.parameters, logger=self.logger)
        pipeline.set_queues(None, "source")
        pipeline.connect()

        if RETURN_TYPE == 'text':
            logger.info("Clearing queue %s.", queue)
        queues = set()
        for key, value in self.pipeline_configuration.items():
            if 'source-queue' in value:
                queues.add(value['source-queue'])
                if pipeline.has_internal_queues:
                    queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                queues.update(value['destination-queues'])

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
            self.abort("Unknown logging handler %r" % self.parameters.logging_handler)

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
            check_logger, list_handler = utils.setup_list_logging(name='check',
                                                                  logging_level=self.logging_level)
        else:
            check_logger = self.logger

        # loading files and syntax check
        files = {DEFAULTS_CONF_FILE: None, PIPELINE_CONF_FILE: None,
                 RUNTIME_CONF_FILE: None, BOTS_FILE: None,
                 HARMONIZATION_CONF_FILE: None}
        check_logger.info('Reading configuration files.')
        for filename in files:
            try:
                with open(filename) as file_handle:
                    files[filename] = json.load(file_handle)
            except (IOError, ValueError) as exc:  # pragma: no cover
                check_logger.error('Could not load %r: %s.', filename, exc)
                retval = 1
        if retval:
            if RETURN_TYPE == 'json':
                return 1, {'status': 'error', 'lines': list_handler.buffer}
            else:
                self.logger.error('Fatal errors occurred.')
                return 1, retval

        check_logger.info('Checking defaults configuration.')
        try:
            with open(pkg_resources.resource_filename('intelmq', 'etc/defaults.conf')) as fh:
                defaults = json.load(fh)
        except FileNotFoundError:
            pass
        else:
            keys = set(defaults.keys()) - set(files[DEFAULTS_CONF_FILE].keys())
            if keys:
                check_logger.error("Keys missing in your 'defaults.conf' file: %r", keys)

        check_logger.info('Checking runtime configuration.')
        http_proxy = files[DEFAULTS_CONF_FILE].get('http_proxy')
        https_proxy = files[DEFAULTS_CONF_FILE].get('https_proxy')
        # Either both are given or both are not given
        if (not http_proxy or not https_proxy) and not (http_proxy == https_proxy):
            check_logger.warning('Incomplete configuration: Both http and https proxies must be set.')
            retval = 1

        check_logger.info('Checking runtime and pipeline configuration.')
        all_queues = set()
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # pipeline keys
            for field in ['description', 'group', 'module', 'name', 'enabled']:
                if field not in bot_config:
                    check_logger.warning('Bot %r has no %r.', bot_id, field)
                    retval = 1
            if 'run_mode' in bot_config and bot_config['run_mode'] not in ['continuous', 'scheduled']:
                message = "Bot %r has invalid `run_mode` %r. Must be 'continuous' or 'scheduled'."
                check_logger.warning(message, bot_id, bot_config['run_mode'])
                retval = 1
            if bot_id not in files[PIPELINE_CONF_FILE] and bot_config.get('enabled', True):
                check_logger.error('Misconfiguration: No pipeline configuration found for %r.', bot_id)
                retval = 1
            elif bot_id not in files[PIPELINE_CONF_FILE] and not bot_config.get('enabled', True):
                check_logger.warning('Misconfiguration: No pipeline configuration found for %r.', bot_id)
            elif bot_id in files[PIPELINE_CONF_FILE]:
                if ('group' in bot_config and
                        bot_config['group'] in ['Collector', 'Parser', 'Expert']):
                    if ('destination-queues' not in files[PIPELINE_CONF_FILE][bot_id] or
                            (isinstance(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'], list) and
                             len(files[PIPELINE_CONF_FILE][bot_id]['destination-queues']) < 1) or
                            (isinstance(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'], dict) and
                             '_default' not in files[PIPELINE_CONF_FILE][bot_id]['destination-queues'])):
                        check_logger.error('Misconfiguration: No (default) destination queue for %r.', bot_id)
                        retval = 1
                    else:
                        all_queues = all_queues.union(files[PIPELINE_CONF_FILE][bot_id]['destination-queues'])
                if ('group' in bot_config and
                        bot_config['group'] in ['Parser', 'Expert', 'Output']):
                    if ('source-queue' not in files[PIPELINE_CONF_FILE][bot_id] or
                            not isinstance(files[PIPELINE_CONF_FILE][bot_id]['source-queue'], str)):
                        check_logger.error('Misconfiguration: No source queue for %r.', bot_id)
                        retval = 1
                    else:
                        all_queues.add(files[PIPELINE_CONF_FILE][bot_id]['source-queue'])
                        all_queues.add(files[PIPELINE_CONF_FILE][bot_id]['source-queue'] + '-internal')
        # ignore allowed orphaned queues
        allowed_orphan_queues = set(getattr(self.parameters, 'intelmqctl_check_orphaned_queues_ignore', ()))
        if not no_connections:
            try:
                pipeline = PipelineFactory.create(self.parameters, logger=self.logger)
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
                                         "https://intelmq.readthedocs.io/en/latest/guides/intelmqctl.html"
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
        if upgrades.harmonization({}, {}, files[HARMONIZATION_CONF_FILE],
                                  dry_run=True)[0]:
            check_logger.warning("Harmonization needs an upgrade, call "
                                 "intelmqctl upgrade-config.")

        check_logger.info('Checking for bots.')
        for bot_id, bot_config in files[RUNTIME_CONF_FILE].items():
            # importable module
            try:
                bot_module = importlib.import_module(bot_config['module'])
            except ImportError as exc:
                check_logger.error('Incomplete installation: Bot %r not importable: %r.', bot_id, exc)
                retval = 1
                continue
            bot = getattr(bot_module, 'BOT')
            bot_parameters = files[DEFAULTS_CONF_FILE].copy()
            bot_parameters.update(bot_config.get('parameters', {}))  # the parameters field may not exist
            bot_check = bot.check(bot_parameters)
            if bot_check:
                for log_line in bot_check:
                    getattr(check_logger, log_line[0])("Bot %r: %s" % (bot_id, log_line[1]))
        for group in files[BOTS_FILE].values():
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

        if RETURN_TYPE == 'json':
            if retval:
                return 1, {'status': 'error', 'lines': list_handler.buffer}
            else:
                return 0, {'status': 'success', 'lines': list_handler.buffer}
        else:
            if retval:
                self.logger.error('Some issues have been found, please check the above output.')
                return retval, 'error'
            else:
                self.logger.info('No issues found.')
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

        state file:

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
                self.logger.error("State file %r is not writable.", state_file)
                return 1, "State file %r is not writable." % state_file
            state = utils.load_configuration(state_file)
        else:
            """
            We create the state file directly before any upgrade function.
            Otherwise we might run into the situation, that we can't write the state but we already upgraded.
            """
            self.logger.info('Writing initial state file.')
            state = {"version_history": [],
                     "upgrades": {},
                     "results": []}
            if dry_run:
                self.logger.info('Would create state file now at %r.',
                                 state_file)
                return 0, 'success'
            try:
                utils.write_configuration(state_file, state, new=True)
            except Exception as exc:
                self.logger.error('Error writing state file %r: %s.', state_file, exc)
                return 1, 'Error writing state file %r: %s.' % (state_file, exc)
            self.logger.info('Successfully wrote initial state file.')

        defaults = utils.load_configuration(DEFAULTS_CONF_FILE)
        runtime = utils.load_configuration(RUNTIME_CONF_FILE)
        harmonization = utils.load_configuration(HARMONIZATION_CONF_FILE)
        if dry_run:
            self.logger.info('Doing a dry run, not writing anything now.')

        if function:
            if not force and state['upgrades'].get(function, False):
                # already performed
                self.logger.info('This upgrade has been performed previously successfully already. Force with -f.')
                return 0, 'success'

            result = {"function": function,
                      "time": datetime.datetime.now().isoformat()
                      }
            if not hasattr(upgrades, function):
                self.logger.error('This function does not exist. '
                                  'Available functions are %s',
                                  ', '.join(upgrades.__all__))
                return 1, 'error'
            try:
                retval, defaults_new, runtime_new, harmonization_new = getattr(
                    upgrades, function)(defaults, runtime, harmonization, dry_run)
                # Handle changed configurations
                if retval is True and not dry_run:
                    utils.write_configuration(DEFAULTS_CONF_FILE, defaults_new,
                                              backup=not no_backup)
                    utils.write_configuration(RUNTIME_CONF_FILE, runtime_new,
                                              backup=not no_backup)
                    utils.write_configuration(HARMONIZATION_CONF_FILE, harmonization_new,
                                              backup=not no_backup)
            except Exception:
                self.logger.exception('Upgrade %r failed, please report this bug '
                                      'with the shown traceback.',
                                      function)
                result['traceback'] = traceback.format_exc()
                result['success'] = False
            else:
                if type(retval) is str:
                    self.logger.error('Upgrade %r failed: %s', function, retval)
                    result['message'] = retval
                    result['success'] = False
                elif retval is None:
                    self.logger.info('Upgrade %r successful: Nothing to do.',
                                     function)
                    result['success'] = True
                elif retval is True:
                    self.logger.info('Upgrade %r successful.', function)
                    result['success'] = True
                else:
                    self.logger.error('Unknown return value %r for %r. '
                                      'Please report this as bug.',
                                      retval, function)
                    result['success'] = False

                result['retval'] = retval

            state['results'].append(result)
            state['upgrades'][function] = result['success']
            if not dry_run:
                utils.write_configuration(state_file, state,
                                          backup=not no_backup)

            if result['success']:
                return 0, 'success'
            else:
                return 1, 'error'

        if previous:
            previous = tuple(utils.lazy_int(v) for v in previous.split('.'))
            self.logger.info("Using previous version %r from parameter.",
                             '.'.join(str(x) for x in previous))

        if __version_info__ in state["version_history"] and not force:
            return 0, "Nothing to do."
        else:
            if state["version_history"] and not previous and not force:
                previous = state["version_history"][-1]
                self.logger.info("Found previous version %s in state file.",
                                 '.'.join(str(x) for x in previous))
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
                                self.logger.info("Catch up function %s from version %s.",
                                                 fname, '.'.join(str(x) for x in version))
                                funcs.append(function)
                        if funcs:
                            todo.append((version, funcs, False))
            else:
                self.logger.info("Found no previous version or forced, doing all upgrades.")
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
                    self.logger.info('Upgrading to version %s.',
                                     '.'.join(map(str, version)))
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
                        retval, defaults, runtime, harmonization = function(defaults, runtime, harmonization, dry_run)
                    except Exception:
                        self.logger.exception('%s: Upgrade failed, please report this bug '
                                              'with the traceback.', docstring)
                        result['traceback'] = traceback.format_exc()
                        result['success'] = False
                    else:
                        if type(retval) is str:
                            self.logger.error('%s: Upgrade failed: %s', docstring, retval)
                            result['message'] = retval
                            result['success'] = False
                        elif retval is None:
                            self.logger.info('%s: Nothing to do.', docstring)
                            result['success'] = True
                        elif retval is True:
                            self.logger.info('%s: Upgrade successful.', docstring)
                            result['success'] = True
                        else:
                            self.logger.error('%s: Unknown return value %r. Please report this '
                                              'as bug.', docstring, retval)
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
                                              backup=not no_backup)
                self.logger.error('Some migration did not succeed or '
                                  'manual intervention is needed. Look at '
                                  'the output above. Afterwards, re-run '
                                  'this program.')

            try:
                if not dry_run:
                    utils.write_configuration(DEFAULTS_CONF_FILE, defaults,
                                              backup=not no_backup)
                    utils.write_configuration(RUNTIME_CONF_FILE, runtime,
                                              backup=not no_backup)
                    utils.write_configuration(HARMONIZATION_CONF_FILE, harmonization,
                                              backup=not no_backup)
            except Exception as exc:
                self.logger.error('Writing defaults or runtime configuration '
                                  'did not succeed: %s\nFix the problem and '
                                  'afterwards, re-run this program.',
                                  exc)
                return 1, 'error'

            if not error:
                if todo:
                    self.logger.info('Configuration upgrade successful!')
                else:
                    self.logger.info('Nothing to do!')

            if not dry_run:
                utils.write_configuration(state_file, state,
                                          backup=not no_backup)

        if error:
            return 1, 'error'
        else:
            return 0, 'success'

    def debug(self, sections=None):
        """
        Give debugging output
        get_paths:
            print path information
        """

        output = {}
        if sections is None or 'paths' in sections:
            output['paths'] = {}
            variables = globals()
            if RETURN_TYPE == 'text':
                print('Paths:')
            for path in ('BOTS_FILE', 'DEFAULTS_CONF_FILE',
                         'HARMONIZATION_CONF_FILE', 'PIPELINE_CONF_FILE',
                         'RUNTIME_CONF_FILE', 'VAR_RUN_PATH', 'STATE_FILE_PATH',
                         'DEFAULT_LOGGING_PATH', '__file__',
                         'CONFIG_DIR', 'ROOT_DIR'):
                output['paths'][path] = variables[path]
                if RETURN_TYPE == 'text':
                    print('%s: %r' % (path, variables[path]))
        if sections is None or 'environment_variables' in sections:
            output['environment_variables'] = {}
            if RETURN_TYPE == 'text':
                print('Environment variables:')
            for variable in ('INTELMQ_ROOT_DIR', 'INTELMQ_PATHS_NO_OPT',
                             'INTELMQ_PATHS_OPT', 'INTELMQ_MANAGER_CONTROLLER_CMD',
                             'PATH'):
                output['environment_variables'][variable] = os.getenv(variable)
                if RETURN_TYPE == 'text':
                    print('%s: %r' % (variable, os.getenv(variable)))
        return 0, output


def main():  # pragma: no cover
    x = IntelMQController(interactive=True)
    return x.run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
