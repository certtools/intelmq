import argparse
import psutil
import inspect

APPNAME = "intelmqctl"
VERSION = "0.0.0"
DESCRIPTION = "description: intelmqctl is the tool to control intelmq system"
USAGE = '''
  intelmqctl --bot [start|stop|restart|reload] --id=cymru-expert
  intelmqctl --botnet [start|stop|restart|reload]
  intelmqctl --pipeline [list|edit]'''


class IntelMQContoller():
    
    def __init__(self):
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
        print "bot_start"
        
    def bot_stop(self):
        print "bot_start"
        
    def bot_restart(self):
        print "bot_start"
    def bot_reload(self):
        print "bot_start"
    def bot_status(self):
        print "bot_start"

    def botnet_start(self):
        print "bot_start"
    def botnet_stop(self):
        print "bot_start"
    def botnet_restart(self):
        print "bot_start"
    def botnet_reload(self):
        print "bot_start"
    def botnet_status(self):
        print "bot_start"
    
    def pipeline_list(self):
        print "bot_start"
    def pipeline_edit(self):
        print "bot_start"
    
    
    
x = IntelMQContoller()
x.run()
