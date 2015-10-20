from __future__ import unicode_literals
import sys
from glob import glob
from intelmq.lib.bot import Bot
import json

class CustomFilterExpertBot(Bot):
    """ Filter bot has filters. Filters have conditions. """

    filters = {}

    def meet_condition(self, message):
        for filterI in CustomFilterExpertBot.filters:
            filter = CustomFilterExpertBot.filters[filterI]
            including = True if filter["type"] == "include" else False # typ filtru
            conforming = True # message odpovida vsem podminkam filteru            
            for condition in filter["conditions"]:
                if condition not in message:
                    if including:
                        return False
                    conforming = False
                    break
                else:
                    passed = False
                    for value in filter["conditions"][condition]: # XX nefunguje wildcard *@isp.cz
                        if value == message[condition]:
                            passed = True
                            break
                    if passed == False:
                        if including:
                            return False
                        conforming = False
                        break
            if conforming and including == False:
                return False
        return True


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
        self.acknowledge_message()

if __name__ == "__main__":
    bot = CustomFilterExpertBot(sys.argv[1])
    bot.start()
