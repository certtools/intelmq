
### NOTE: this json is a sample of the main file with all bots and correspondent options. Use it to build this script

INFO = '''
{
    "Input Bots": {
        "ArborFeed": {
            "module": "intelmq.bots.inputs.arbor.feed",
            "description": "Arbor Feed is the bot responsible to get the report from source of information.",
            "parameters": {
                "processing_interval": "3600"
            }
        },
        "ArborParser": {
            "module": "intelmq.bots.inputs.arbor.parser",
            "description": "Arbor Parser is the bot responsible to parse the report.",
            "parameters": { }
        },
        "ArborHarmonizer": {
            "module": "intelmq.bots.inputs.arbor.harmonizer",
            "description": "Arbor Harmonizer is the bot responsible to add additional information to the events.",
            "parameters": { }
        },
        "VXVaultFeed": {
            "module": "intelmq.bots.inputs.vxvault.feed",
            "description": "VXVault Feed is the bot responsible to get the report from source of information.",
            "parameters": {
                "processing_interval": "3600"
            }
        },
        "VXVaultParser": {
            "module": "intelmq.bots.inputs.vxvault.parser",
            "description": "VXVault Parser is the bot responsible to parse the report.",
            "parameters": { }
        },
        "VXVaultHarmonizer": {
            "module": "intelmq.bots.inputs.vxvault.harmonizer",
            "description": "VXVault Harmonizer is the bot responsible to add additional information to the events.",
            "parameters": { }
        }
    },
    "Experts Bots": {

    },
    "Output Bots": {

    }
}
'''











import re
import os
import json
import shlex
import inspect
import psutil
import argparse



def generate_options_list(options, description_text, question_text):
    while True:
    
        counter = 1
        options_list = list()
        template = "  [%s] %s"
        
        print "\n\n%s" % description_text
        for option in options:
            option_text = template % (counter, option)
            options_list.append(option_text)
            print option_text
            counter += 1
        
        try:
            answer = int(raw_input("\n%s" % question_text))
            if answer <= len(options_list) and answer > 0:
                return answer-1
        
        except ValueError:
            pass
        
        print "\n" * 3
        print "\nERROR: Invalid option!"
        
            












class IntelMQContoller():
    
    def __init__(self):
        
        APPNAME = "intelmqctl"
        VERSION = "0.0.0"
        DESCRIPTION = "description: intelmqctl is the tool to control intelmq system"
        USAGE = '''
        intelmqctl --bot [start|stop|restart|reload] --id=cymru-expert
        intelmqctl --botnet [start|stop|restart|reload]
        intelmqctl --pipeline [list|edit]'''
        
        parser = argparse.ArgumentParser(
                                        prog=APPNAME,
                                        usage=USAGE,
                                        epilog=DESCRIPTION
                                        )

        group = parser.add_mutually_exclusive_group()
        group_list = group.add_mutually_exclusive_group()
        
        parser.add_argument('-v', '--version', action='version', version=VERSION)
        parser.add_argument("--id", dest='id', default=None, help='bot ID')
        
        group_list.add_argument('--bot',      choices=['start', 'stop', 'restart', 'reload', 'status'], metavar='[start|stop|restart|reload|status]', default=None)
        group_list.add_argument('--botnet',   choices=['start', 'stop', 'restart', 'reload', 'status'], metavar='[start|stop|restart|reload|status]', default=None)
        group_list.add_argument('--pipeline', choices=['list', 'edit'],                                 metavar='[list|edit]'                       , default=None)

        self.args = parser.parse_args()
        
        if self.args.id and not self.args.bot:
            print "usage: %s" % USAGE
            print "%s: error: argument --id: expected argument --bot [start|stop|restart|reload|status]" % APPNAME
            exit()








    def auto_method_call(self, method):
        inspect_members = inspect.getmembers(self)
        for name, func in inspect_members:
            if name.startswith(method):
                return func        

    
    def run(self):
        if self.args.bot:
            method_name = "bot_" + self.args.bot
            call_method = self.auto_method_call(method_name)
            call_method(self.args.id)
            
        elif self.args.botnet:
            method_name = "botnet_" + self.args.botnet
            call_method = self.auto_method_call(method_name)
            call_method()
            
        elif self.args.pipeline:
            method_name = "pipeline_" + self.args.pipeline
            call_method = self.auto_method_call(method_name)
            call_method()

    







    def bot_start(self, id):
        info = json.loads(INFO)
        
        # ALGORITH
        # ---------
        # if id already exists:
            # if wants to load:
                # load bot info 
            #else:
        # else:
        #   print list bots


        # Show bot categories (Inputs, Experts, Outputs)
        options = info.keys()
        description_text = "Bots Categories:"
        question_text = "Choose category: "
        answer = generate_options_list(options, description_text, question_text)
        category = options[answer]

        # Show bots correspondent to the category
        options = info[category].keys()
        #for key, values in info[category].iteritems():
        #    text = "%s - %s" % (key, info[category][key]['description'])
        #    options.append(text)
            
        description_text = "%s Bots:" % category
        question_text = "Choose bot: "
        answer = generate_options_list(options, description_text, question_text)
        bot = options[answer]

        module = info[category][bot]['module']
        
        # NOTE: need to be generic and probably needs the ENV VARIABLE. we need to filter part of filepath to be like bots.output.postgresql
        cmd = "python -m %s %s" % (module, id)
        args = shlex.split(cmd)
        p = psutil.Popen(args)
        # save PID in file
        
        
    def bot_stop(self):
        print "bot_stop"
        
        
    def bot_restart(self):
        print "bot_restart"
    
    
    def bot_reload(self):
        print "bot_reload"
    
    
    def bot_status(self):
        print "bot_status"

    
    def botnet_start(self):
        print "botnet_start"
    
    
    def botnet_stop(self):
        print "botnet_stop"
    
    
    def botnet_restart(self):
        print "botnet_restart"
    
    
    def botnet_reload(self):
        print "botnet_reload"
    
    
    def botnet_status(self):
        print "botnet_status"
    
    
    def pipeline_list(self):
        print "pipeline_list"
    
    
    def pipeline_edit(self):
        print "pipeline_edit"
    
    
    
x = IntelMQContoller()
x.run()
