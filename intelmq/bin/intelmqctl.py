#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import importlib
import json
import os
import signal
import time
import traceback

import pkg_resources
import psutil

from intelmq import (DEFAULTS_CONF_FILE, PIPELINE_CONF_FILE, RUNTIME_CONF_FILE,
                     STARTUP_CONF_FILE, SYSTEM_CONF_FILE, VAR_RUN_PATH)
from intelmq.lib import utils
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
    'starting': 'Starting {}...',
    'running': '{} is running.',
    'stopped': '{} is stopped.',
    'stopping': 'Stopping {}...',
    'reloading': 'Reloading {} ...',
    'reloaded': '{} is reloaded.',
}

ERROR_MESSAGES = {
    'starting': '{} failed to START.',
    'running': '{} is still running.',
    'stopped': '{} was NOT RUNNING.',
    'stopping': '{} failed to STOP.',
    'noid': 'No or unconfigured ID was given, use --id',
    'notfound': '{} not found.'
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
            logger.info("{} - {}".format(queue, counter))


def log_bot_error(status, *args):
    if RETURN_TYPE == 'text':
        logger.error(ERROR_MESSAGES[status].format(*args))


def log_bot_message(status, *args):
    if QUIET:
        return
    if RETURN_TYPE == 'text':
        logger.info(MESSAGES[status].format(*args))


def log_botnet_error(status):
    if RETURN_TYPE == 'text':
        logger.error(ERROR_MESSAGES[status].format('Botnet'))


def log_botnet_message(status):
    if QUIET:
        return
    if RETURN_TYPE == 'text':
        logger.info(MESSAGES[status].format('Botnet'))


def log_log_messages(messages):
    if RETURN_TYPE == 'text':
        for message in messages:
            print(' - '.join([message['date'], message['bot_id'],
                              message['log_level'], message['message']]))
            try:
                print(message['extended_message'])
            except KeyError:
                pass


class IntelMQContoller():

    def __init__(self, interactive=False, return_type="python", quiet=False):
        """
        Initializes intelmqctl.

        Parameters
        ==========
        interactive : boolean
            for cli-interface true, functions can exits, parameters are used
        return_type : string
            'python': no special treatment, can be used for use by other
                python code
            'text': user-friendly output for cli, default for interactive use
            'json': machine-readable output for managers
        quiet : boolean
            False by default, can be activated for cronjobs etc.
        """
        global RETURN_TYPE
        RETURN_TYPE = return_type
        global logger
        global QUIET
        QUIET = quiet
        logger = utils.log('intelmqctl', log_level='DEBUG')
        self.logger = logger
        self.interactive = interactive
        self.args = None
        if os.geteuid() == 0:
            logger.warning('Running intelmq as root is highly discouraged!')

        APPNAME = "intelmqctl"
        VERSION = pkg_resources.get_distribution("intelmq").version
        DESCRIPTION = """
        description: intelmqctl is the tool to control intelmq system.

        Outputs are logged to /opt/intelmq/var/log/intelmqctl"""
        USAGE = '''
        intelmqctl [start|stop|restart|status|reload|run] bot-id
        intelmqctl [start|stop|restart|status|reload]
        intelmqctl list [bots|queues]
        intelmqctl log bot-id [number-of-lines [log-level]]
        intelmqctl clear queue-id

Starting a bot:
    intelmqctl start bot-id
Stopping a bot:
    intelmqctl stop bot-id
Restarting a bot:
    intelmqctl restart bot-id
Get status of a bot:
    intelmqctl status bot-id

Run a bot directly (blocking) for debugging purpose:
    intelmqctl run bot-id

Starting the botnet (all bots):
    intelmqctl start
    etc.

Get a list of all configured bots:
    intelmqctl list bots

Get a list of all queues:
    intelmqctl list queues

Clear a queue:
    intelmqctl clear queue-id

Get logs of a bot:
    intelmqctl log bot-id [number-of-lines [log-level]]
    Reads the last lines from bot log, or from system log if no bot ID was
    given. Log level should be one of DEBUG, INFO, ERROR or CRITICAL.
    Default is INFO. Number of lines defaults to 10, -1 gives all. Result
    can be longer due to our logging format!'''

        # stolen functions from the bot file
        # this will not work with various instances of REDIS
        self.parameters = Parameters()
        self.load_defaults_configuration()
        self.load_system_configuration()
        self.pipepline_configuration = utils.load_configuration(
            PIPELINE_CONF_FILE)
        self.runtime_configuration = utils.load_configuration(
            RUNTIME_CONF_FILE)

        if os.path.exists(STARTUP_CONF_FILE):
            self.logger.warning('Deprecated startup.conf file found, please migrate to runtime.conf soon.')
            with open(STARTUP_CONF_FILE, 'r') as fp:
                startup = json.load(fp)
                for bot_id, bot_values in startup.items():
                    if 'parameters' in self.runtime_configuration[bot_id]:
                        self.logger.error('Mixed setup of new runtime.conf and old startup.conf'
                                          ' found. Ignoring startup.conf, please fix this!')
                        exit(1)
                    params = self.runtime_configuration[bot_id].copy()
                    self.runtime_configuration[bot_id].clear()
                    self.runtime_configuration[bot_id]['parameters'] = params
                    self.runtime_configuration[bot_id].update(bot_values)
            try:
                with open(RUNTIME_CONF_FILE + '.new', 'w') as fp:
                    json.dump(self.runtime_configuration, fp, indent=4, sort_keys=True,
                              separators=(',', ': '))
            except PermissionError:
                self.logger.info('Failed to write new configuration format to %r.'
                                 '' % (RUNTIME_CONF_FILE + '.new'))
            else:
                self.logger.info('%r with new format written.' % (RUNTIME_CONF_FILE + '.new'))

        if not os.path.exists(VAR_RUN_PATH):
            os.makedirs(VAR_RUN_PATH)

        if self.interactive:
            parser = argparse.ArgumentParser(
                prog=APPNAME,
                usage=USAGE,
                epilog=DESCRIPTION
            )

            parser.add_argument('-v', '--version',
                                action='version', version=VERSION)
            parser.add_argument('--type', '-t', choices=RETURN_TYPES,
                                default=RETURN_TYPES[0],
                                help='choose if it should return regular text '
                                     'or other machine-readable')

            parser.add_argument('action',
                                choices=['start', 'stop', 'restart', 'status',
                                         'reload', 'run', 'list', 'clear',
                                         'help', 'log'],
                                metavar='[start|stop|restart|status|reload|run'
                                        '|list|clear|log]')
            parser.add_argument('parameter', nargs='*')
            parser.add_argument('--quiet', '-q', action='store_const',
                                help='Quiet mode, useful for reloads initiated'
                                     'scripts like logrotate',
                                const=True)
            self.parser = parser
            self.args = parser.parse_args()
            if self.args.action == 'help':
                parser.print_help()
                exit(0)

            RETURN_TYPE = self.args.type
            QUIET = self.args.quiet

    def load_system_configuration(self):
        if os.path.exists(SYSTEM_CONF_FILE):
            config = utils.load_configuration(SYSTEM_CONF_FILE)
            for option, value in config.items():
                setattr(self.parameters, option, value)

    def load_defaults_configuration(self):
        # Load defaults configuration section
        config = utils.load_configuration(DEFAULTS_CONF_FILE)
        for option, value in config.items():
            setattr(self.parameters, option, value)

    def run(self):
        results = None
        if self.args.action in ['start', 'restart', 'stop', 'status',
                                'reload']:
            if self.args.parameter:
                call_method = getattr(self, "bot_" + self.args.action)
                results = call_method(self.args.parameter[0])
            else:
                call_method = getattr(self, "botnet_" + self.args.action)
                results = call_method()
        elif self.args.action == 'run':
            if self.args.parameter and len(self.args.parameter) == 1:
                self.bot_run(self.args.parameter[0])
            else:
                print("Exactly one bot-id must be given for run.")
                self.parser.print_help()
                exit(2)
        elif self.args.action == 'list':
            if not self.args.parameter or self.args.parameter[0] not in ['bots', 'queues']:
                print("Second argument for list must be 'bots' or 'queues'.")
                self.parser.print_help()
                exit(2)
            method_name = "list_" + self.args.parameter[0]
            call_method = getattr(self, method_name)
            results = call_method()
        elif self.args.action == 'log':
            if not self.args.parameter:
                print("You must give parameters for 'log'.")
                self.parser.print_help()
                exit(2)
            results = self.read_log(*self.args.parameter)
        elif self.args.action == 'clear':
            if not self.args.parameter:
                print("Queue name not given.")
                self.parser.print_help()
                exit(2)
            results = self.clear_queue(self.args.parameter[0])

        if self.args.type == 'json':
            print(json.dumps(results))

    def bot_run(self, bot_id):
        try:
            bot_module = self.runtime_configuration[bot_id]['module']
        except KeyError:
            log_bot_error('notfound', bot_id)
            return 'error'
        else:
            module = importlib.import_module(bot_module)
            # TODO: Search for bot class is dirty (but works)
            botname = [name for name in dir(module)
                       if hasattr(getattr(module, name), 'process') and
                       name.endswith('Bot') and
                       name not in ['CollectorBot', 'ParserBot']][0]
            bot = getattr(module, botname)
            instance = bot(bot_id)
            instance.start()

    def status_process(self, pid):
        try:
            return psutil.Process(int(pid.strip()))
        except psutil.NoSuchProcess:
            return False

    def bot_start(self, bot_id):
        if bot_id is None:
            log_bot_error('noid')
            return 'error'
        pid = utils.read_pidfile(bot_id)
        if pid:
            if self.bot_status(bot_id) == 'running':
                return 'running'
            else:
                utils.remove_pidfile(bot_id)
        log_bot_message('starting', bot_id)
        try:
            module = self.runtime_configuration[bot_id]['module']
        except KeyError:
            log_bot_error('notfound', bot_id)
            return 'error'
        else:
            cmdargs = ["python3", "-m", module, bot_id]
            with open('/dev/null', 'w') as devnull:
                psutil.Popen(cmdargs, stdout=devnull, stderr=devnull)

        time.sleep(0.25)
        return self.bot_status(bot_id)

    def bot_stop(self, bot_id):
        pid = utils.read_pidfile(bot_id)
        if not pid:
            log_bot_error('stopped', bot_id)
            return 'stopped'
        log_bot_message('stopping', bot_id)
        proc = self.status_process(pid)
        if proc:
            proc.send_signal(signal.SIGINT)
            time.sleep(0.25)
            if self.status_process(pid):
                log_bot_error('running', bot_id)
                return 'running'
        else:
            utils.remove_pidfile(bot_id, force=True)
            log_bot_message('stopped', bot_id)
            return 'stopped'

    def bot_reload(self, bot_id):
        pid = utils.read_pidfile(bot_id)
        if not pid:
            log_bot_error('stopped', bot_id)
            return 'stopped'
        log_bot_message('reloading', bot_id)
        proc = psutil.Process(int(pid.strip()))
        proc.send_signal(signal.SIGHUP)
        if self.status_process(pid):
            log_bot_message('running', bot_id)
            return 'running'
        log_bot_error('stopped', bot_id)
        return 'stopped'

    def bot_restart(self, bot_id):
        status_stop = self.bot_stop(bot_id)
        status_start = self.bot_start(bot_id)
        return (status_stop, status_start)

    def bot_status(self, bot_id):
        pid = utils.read_pidfile(bot_id)
        if pid and self.status_process(pid):
            log_bot_message('running', bot_id)
            return 'running'
        elif pid and not self.status_process(pid):
            utils.remove_pidfile(bot_id, force=True)

        if bot_id not in self.runtime_configuration:
            log_bot_error('notfound', bot_id)
            return 'error'

        log_bot_message('stopped', bot_id)
        return 'stopped'

    def botnet_start(self):
        botnet_status = {}
        log_botnet_message('starting')
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = self.bot_start(bot_id)
        log_botnet_message('running')
        return botnet_status

    def botnet_stop(self):
        botnet_status = {}
        log_botnet_message('stopping')
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = self.bot_stop(bot_id)
        log_botnet_message('stopped')
        return botnet_status

    def botnet_reload(self):
        botnet_status = {}
        log_botnet_message('reloading')
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = self.bot_reload(bot_id)
        log_botnet_message('reloaded')
        return botnet_status

    def botnet_restart(self):
        botnet_status = {}
        log_botnet_message('stopping')
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = tuple(self.bot_stop(bot_id))
        time.sleep(3)
        log_botnet_message('stopped')
        log_botnet_message('starting')
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] += tuple(self.bot_start(bot_id))
        log_botnet_message('running')
        return botnet_status

    def botnet_status(self):
        botnet_status = {}
        for bot_id in sorted(self.runtime_configuration.keys()):
            botnet_status[bot_id] = self.bot_status(bot_id)
        return botnet_status

    def list_bots(self):
        """
        Lists all configured bots from startup.conf with bot id and
        description.

        If description is not set, None is used instead.
        """
        if self.args and self.args.type == 'text':
            for bot_id in sorted(self.runtime_configuration.keys()):
                print("Bot ID: {}\nDescription: {}"
                      "".format(bot_id, self.runtime_configuration[bot_id].get('description')))
        return [{'id': bot_id,
                 'description': self.runtime_configuration[bot_id].get('description')}
                for bot_id in sorted(self.runtime_configuration.keys())]

    def list_queues(self):
        source_queues = set()
        destination_queues = set()
        internal_queues = set()

        for botid, value in self.pipepline_configuration.items():
            if 'source-queue' in value:
                source_queues.add(value['source-queue'])
                internal_queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                destination_queues.update(value['destination-queues'])

        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(source_queues, "source")
        pipeline.connect()

        queues = source_queues.union(destination_queues).union(internal_queues)
        counters = pipeline.count_queued_messages(*queues)
        log_list_queues(counters)

        return_dict = dict()
        for bot_id, info in self.pipepline_configuration.items():
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
        logger.info("Clearing queue {}".format(queue))
        queues = set()
        for key, value in self.pipepline_configuration.items():
            if 'source-queue' in value:
                queues.add(value['source-queue'])
                queues.add(value['source-queue'] + '-internal')
            if 'destination-queues' in value:
                queues.update(value['destination-queues'])

        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(queues, "source")
        pipeline.connect()

        if queue not in queues:
            logger.error("Queue {} does not exist!".format(queue))
            return 'not-found'

        try:
            pipeline.clear_queue(queue)
            logger.info("Successfully cleared queue {}".format(queue))
            return 'success'
        except Exception:
            logger.error("Error while clearing queue {}:\n{}"
                         "".format(queue, traceback.format_exc()))
            return 'error'

    def read_log(self, bot_id, number_of_lines=10, log_level='INFO'):
        # TODO: Parse number of lines
        try:
            number_of_lines = int(number_of_lines)
        except ValueError:
            number_of_lines = 10
        if not log_level:
            log_level = LOG_LEVEL['INFO']
        else:
            try:
                log_level = LOG_LEVEL[log_level.upper()]
            except KeyError:
                logger.error("Invalid log_level. Must be one of {}"
                             "".format(', '.join(LOG_LEVEL.keys())))
                return[]

        return self.read_bot_log(bot_id, log_level, number_of_lines)

    def read_bot_log(self, bot_id, log_level, number_of_lines):
        bot_log_path = os.path.join(self.parameters.logging_path,
                                    bot_id + '.log')
        if not os.path.isfile(bot_log_path):
            logger.error("Log path not found: {}".format(bot_log_path))
            return []

        messages = list()

        message_overflow = ''
        message_count = 0

        for line in utils.reverse_readline(bot_log_path):
            log_message = utils.parse_logline(line)

            if type(log_message) is not dict:
                message_overflow = '\n'.join([line, message_overflow])
                continue
            if LOG_LEVEL[log_message['log_level']] < log_level:
                continue

            if message_overflow:
                log_message['extended_message'] = message_overflow
                message_overflow = ''

            message_count += 1
            messages.append(log_message)

            if message_count >= number_of_lines and number_of_lines != -1:
                break

        log_log_messages(messages[::-1])
        return messages[::-1]


def main():
    x = IntelMQContoller(interactive=True)
    x.run()

if __name__ == "__main__":
    main()
