#!/usr/bin/env python

# FIXME: stolen functions from the bot file
# FIXME: this will not work with various instances of REDIS

import re
import os
import sys
import json
import time
import shlex
import inspect
import signal
import argparse

'''
import psutil
from intelmq.lib.pipeline import PipelineFactory
from intelmq.lib.pipeline import Redis

from intelmq.lib import utils

from intelmq import DEFAULTS_CONF_FILE
from intelmq import STARTUP_CONF_FILE
from intelmq import PIPELINE_CONF_FILE
from intelmq import SYSTEM_CONF_FILE
from intelmq import RUNTIME_CONF_FILE
'''

class Parameters(object):
    pass


OUTPUT_FORMAT = None



PIDDIR = "/opt/intelmq/var/run/"
PIDFILE = "/opt/intelmq/var/run/%s.pid"

STATUSES = {
    'starting': 0,
    'running': 1,
    'stopping': 2,
    'stopped': 3
}

MESSAGES = {
    'starting': 'Starting %s...',
    'running': '%s is already running.',
    'stopped': '%s is stopped.',
    'stopping': 'Stopping %s...'
}

ERROR_MESSAGES = {
    'starting': '%s failed to START.',
    'running': '%s is still running.',
    'stopped': '%s was NOT RUNNING.',
    'stopping': '%s failed to STOP.'
}

LOG_LEVEL = {
    'default': -1,
    'DEBUG': 0,
    'INFO': 1,
    'ERROR': 2,
    'CRITICAL': 3
}



def log_list_queus(queues):
    if OUTPUT_FORMAT == 'text':
        for queue, counter in sorted(queues.iteritems()):
            print "%s - %s" % (queue,  counter)

def log_bot_error(bot_id, status):
    if OUTPUT_FORMAT == 'text':
        print ERROR_MESSAGES[status] % bot_id
    
def log_bot_message(bot_id, status):
    if OUTPUT_FORMAT == 'text':
        print MESSAGES[status] % bot_id

def log_botnet_error(status):
    if OUTPUT_FORMAT == 'text':
        print ERROR_MESSAGES[status] % 'Botnet'
    
def log_botnet_message(status):
    if OUTPUT_FORMAT == 'text':
        print MESSAGES[status] % 'Botnet'
       
def write_pidfile(bot_id, pid):
    filename = PIDFILE % bot_id
    with open(filename, 'w') as fp:
        fp.write(str(pid))

def remove_pidfile(bot_id):
    filename = PIDFILE % bot_id
    os.remove(filename)

def read_pidfile(bot_id):
    filename = PIDFILE % bot_id
    if check_pidfile(bot_id):
        with open(filename, 'r') as fp:
            pid = fp.read()
        return pid.strip()
    return None

def check_pidfile(bot_id):
    filename = PIDFILE % bot_id
    if os.path.isfile(filename):
        try:
            with open(filename, 'r') as fp:
                pid = fp.read()
            return int(pid.strip())
        except ValueError:
            return None
    return None
        
def start_process(bot_id, cmd):
    devnull = open('/dev/null', 'w')
    args = shlex.split(cmd)
    p = psutil.Popen(args, stdout=devnull, stderr=devnull)
    return p.pid

def stop_process(pid):
    p = psutil.Process(int(pid))
    p.send_signal(signal.SIGINT)
    
def status_process(pid):
    try:
        psutil.Process(int(pid))
        return True
    except psutil.NoSuchProcess:
        return False
    
    



def load_configuration_to_dict(configuration_file):
    with open(configuration_file) as fp:
        return json.load(fp)

def load_configuration_to_parameters(configuration_file):
    parameters = Parameters()
    config = utils.load_configuration(configuration_file) 
    for option, value in config.iteritems():
        setattr(parameters, option, value)
    return parameters

def get_method_instance(method_name):
    inspect_members = inspect.getmembers(IntelMQContoller())
    for name, method_instance in inspect_members:
        if name.startswith(method_name):
            return method_instance


class IntelMQContoller():

    def __init__(self):


        ''' Load configurations '''
        '''
        self.startup = load_configuration_to_dict(STARTUP_CONF_FILE)
        self.system = load_configuration_to_dict(SYSTEM_CONF_FILE)
    
        system_params = load_configuration_to_parameters(SYSTEM_CONF_FILE)
        defaults_params = load_configuration_to_parameters(DEFAULTS_CONF_FILE)

        self.parameters = Parameters()
        self.parameters.update(system_params)
        self.parameters.update(defaults_params)
        '''

        ''' Supported output formats '''

        self.output_formats = ['text', 'json']    



        ''' Command-line Interface '''
           
        APPNAME = "intelmqctl"
        VERSION = "0.0.0"
        DESCRIPTION = "description: intelmqctl is the tool to control IntelMQ system"
        USAGE = '''
        intelmqctl --bot [start|stop|restart|status] --id=cymru-expert
        intelmqctl --botnet [start|stop|restart|status]
        intelmqctl --list [bots|queues]
        intelmqctl --log <log-level>:<number-of-lines>'''
        
        parser = argparse.ArgumentParser(
                                          prog = APPNAME,
                                          usage = USAGE,
                                          epilog = DESCRIPTION
                                        )
        
        group = parser.add_mutually_exclusive_group()
        group_list = group.add_mutually_exclusive_group()
        
        parser.add_argument('-v', '--version', action='version', version=VERSION)
        parser.add_argument("--id", dest='bot_id', default=None, help='bot ID')
        parser.add_argument('--type', choices = self.output_formats, default = self.output_formats[0], help='choose if it should return regular text or other forms of output')
        
        group_list.add_argument('--log',                                                      metavar='<log-level>:<number-of-lines>', default=None)
        group_list.add_argument('--bot',      choices=['start', 'stop', 'restart', 'status'], metavar='[start|stop|restart|status]', default=None)
        group_list.add_argument('--botnet',   choices=['start', 'stop', 'restart', 'status'], metavar='[start|stop|restart|status]', default=None)
        group_list.add_argument('--list',     choices=['bots','queues'],                      metavar='[bots|queues]'              , default=None)
        
        self.args = parser.parse_args()
        
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(-1)



        ''' Output Format Defined '''

        global OUTPUT_FORMAT
        OUTPUT_FORMAT = self.args.type



        ''' PID Directory '''
        '''               
        if not os.path.exists(PIDDIR):
            os.makedirs(PIDDIR)
        '''




    

    
    def run(self):   

        if self.args.bot:
            method_name = "bot_" + self.args.bot

        elif self.args.botnet:
            method_name = "botnet_" + self.args.botnet
            
        elif self.args.list:
            method_name = "list_" + self.args.list
            
        elif self.args.log:
            method_name = "log_read"

        results = None
        method_instance = get_method_instance(method_name)
        results = method_instance()

        if self.args.type == 'json':
            print json.dumps(results)
        else:
            print results


    def bot_start(self):
        bot_id = self.args.bot_id

        pid = read_pidfile(bot_id)
        if pid:
            if status_process(pid):
                log_bot_message(bot_id, 'running')
                return 'running'
            else:
                remove_pidfile(bot_id)
        log_bot_message(bot_id, 'starting')
        self.__bot_start(bot_id, self.startup[bot_id]['module'])
        time.sleep(0.25)
        return self.bot_status(bot_id)
        
    def __bot_start(self, bot_id, module):
        cmd = "python -m %s %s" % (module, bot_id)
        pid = start_process(bot_id, cmd)
        write_pidfile(bot_id, pid)
        
        
    def bot_stop(self):
        bot_id = self.args.bot_id

        pid = read_pidfile(bot_id)
        if not pid:
            log_bot_error(bot_id, 'stopped')
            return 'stopped'
        if not status_process(pid):
            remove_pidfile(bot_id)
            log_bot_error(bot_id, 'stopped')
            return 'stopped'
        log_bot_message(bot_id, 'stopping')
        res = self.__bot_stop(bot_id, pid)
        time.sleep(0.25)
        if status_process(pid):
            log_bot_error(bot_id, 'running')
            return 'running'
        return 'stopped'
        
        
    def __bot_stop(self, bot_id, pid):
        stop_process(pid)
        remove_pidfile(bot_id)    


    def bot_restart(self):
        bot_id = self.args.bot_id

        status_stop = self.bot_stop(bot_id)
        status_start = self.bot_start(bot_id)
        return (status_stop, status_start)
    
    
    def bot_status(self):
        bot_id = self.args.bot_id

        pid = read_pidfile(bot_id)
        if pid and status_process(pid):
            log_bot_message(bot_id, 'running')
            return 'running'
        log_bot_message(bot_id, 'stopped')
        return 'stopped'

    
    def botnet_start(self):
        botnet_status = {}
        log_botnet_message('starting')
        for bot_id in sorted(self.startup.keys()):
            botnet_status[bot_id] = self.bot_start(bot_id)
        log_botnet_message('running')
        return botnet_status
    
    
    def botnet_stop(self):
        botnet_status = {}
        log_botnet_message('stopping')
        for bot_id in sorted(self.startup.keys()):
            botnet_status[bot_id] = self.bot_stop(bot_id)
        log_botnet_message('stopped')
        return botnet_status
    
    
    def botnet_restart(self):
        botnet_status = {}
        log_botnet_message('stopping')
        for bot_id in sorted(self.startup.keys()):
            botnet_status[bot_id] = tuple(self.bot_stop(bot_id))
        time.sleep(3)
        log_botnet_message('stopped')
        log_botnet_message('starting')
        for bot_id in sorted(self.startup.keys()):
            botnet_status[bot_id] += tuple(self.bot_start(bot_id))
        log_botnet_message('started')
        return botnet_status
    
    
    def botnet_status(self):
        botnet_status = {}
        for bot_id in sorted(self.startup.keys()):
            botnet_status[bot_id] = self.bot_status(bot_id)
        return botnet_status

    
    def list_bots(self):
        title = "\n\nList of Bots:\n"
        title += "-" * (len(title)-1)
        title += "\n"
        print title
        for bot_id in sorted(self.startup.keys()):
            print "Bot ID: %s\nDescription: %s\n" % (bot_id, self.startup[bot_id]['description'])

            
    def list_queues(self):
        fp = open(DEFAULTS_CONF_FILE, 'r')
        conf = json.load(fp)
        #pipeline_host = conf[""]
        #pipeline_port = 
        #pipeline_db = 
        fp.close()

        fp = open(PIPELINE_CONF_FILE, 'r')
        conf = json.load(fp)
        fp.close()

        source_queues = set()
        destination_queues = set()

        for key, value in conf.iteritems():
            if 'source-queue' in value:
                source_queues.add(value['source-queue'])
            if 'destination-queues' in value:
                destination_queues.update(value['destination-queues'])                

        pipeline = PipelineFactory.create(self.parameters)
        pipeline.set_queues(source_queues, "source")
        pipeline.connect()

        queues = source_queues.union(destination_queues)
        counters = pipeline.count_queued_messages(queues)
        log_list_queus(counters)
        
        return_dict = dict()
        for bot_id, info in conf.iteritems():
            return_dict[bot_id] = dict()
            
            if 'source-queue' in info:
                return_dict[bot_id]['source_queue'] = (info['source-queue'], counters[info['source-queue']])
                
            if 'destination-queues' in info:
                return_dict[bot_id]['destination_queues'] = list()
                for dest_queue in info['destination-queues']:
                    return_dict[bot_id]['destination_queues'].append((dest_queue, counters[dest_queue]))
        
        return return_dict
        
        
    def log_read(self, log_level, bot_id):

        self.args.log, self.args.bot_id

        # TODO: Parse number of lines
        split_log_level = self.args.log.split(':')
        
        if len(split_log_level) != 2:
            return
        
        number_of_lines = int(split_log_level[1])
        log_level = LOG_LEVEL[split_log_level[0]]

        if self.args.bot_id:
            return self.read_bot_log(self.args.bot_id, log_level, number_of_lines)
        else:
            return self.read_system_log(log_level, number_of_lines)


    # FIXME: rewrite        
    #
    def read_system_log(self, log_level, number_of_lines):
        pass

        
    # FIXME: rewrite
    #
    def read_bot_log(self, bot_id, log_level, number_of_lines):
        basepath = self.system['logging_path']
        if not self.system['logging_path'].endswith('/'):
            basepath += '/'
            
        bot_log_path = basepath + bot_id + '.log'
        
        if os.path.isfile(bot_log_path):
            bot_log_file = open(bot_log_path, 'r')
        else:
            return []
        
        messages = list()

        extended_message = ''
        last_message = {}
        added_messages = 0
        line_number = 0
        
        for line in bot_log_file:
            line_number += 1
            splitted_line = line.split(' - ')
            
            if len(splitted_line) >= 4:
                if splitted_line[1] == bot_id:
                    log_message = {
                        'line_number': line_number,
                        'date': splitted_line[0],
                        'bot_id': splitted_line[1],
                        'log_level': splitted_line[2],
                        'message': ' - '.join(splitted_line[3:])
                    }
                    
                    if extended_message != '':
                        last_message['extended_message'] = extended_message
                        extended_message = ''
                        
                    last_message = log_message
                    
                    if (log_message['log_level'] not in LOG_LEVEL) or (LOG_LEVEL[log_message['log_level']] >= log_level):
                        added_messages += 1
                        messages.append(log_message)
                        
                        if added_messages > number_of_lines:
                            del messages[0]
                else:
                    extended_message += line
            else:
                extended_message += line
                    
        return messages

            
    
if __name__ == "__main__":
    intelmqctl = IntelMQContoller()
    intelmqctl.run()
