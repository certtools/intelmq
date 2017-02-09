from __future__ import unicode_literals
import sys
from glob import glob
from intelmq.lib.bot import Bot
import json

class CustomFilterExpertBot(Bot):
    """ Filter bot has filters. Filters have conditions. 
    If the value conforms with any part of the condition, it is passed.    
    """

    filters = {}

    def meet_condition(self, message):        
        if not self.filters:
            return True
        
        includable = False
        for filterO in self.filters.values():                        
            conforming = False
            for key, value in filterO["conditions"].items():                
                try:                    
                    if (isinstance(value, list) and message[key] in value) or value == message[key]: # filter passed                        
                        conforming = True                        
                except KeyError:                    
                    conforming = False
                    break
            if conforming:
                if filterO["type"] == "include":                    
                    includable = True
                elif filterO["type"] == "exclude":                    
                    return False
        return includable    

    def init(self):
        """ Loads rules from .json """
        ruleI = 0
        for rule_file in glob(self.parameters.rules_dir + "*.json"):
            with open(rule_file, 'r') as f:                
                rule = json.load(f)                
                CustomFilterExpertBot.filters[ruleI] = rule
            ruleI += 1        

    def process(self):
        message = self.receive_message()        
        if message and self.meet_condition(message):
            self.send_message(message)
            self.logger.error("PASSING message: " + repr(message) + ".") # .debug not displayed until an .error is called
        else:
            self.logger.error("Dropping message: " + repr(message) + ".")
        self.acknowledge_message()
     

BOT = CustomFilterExpertBot