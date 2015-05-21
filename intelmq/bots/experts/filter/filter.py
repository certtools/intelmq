from glob import glob
from intelmq.lib.bot import Bot
from intelmq.lib.bot import sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event
import json
import logging


class BotDev:
    """ Development object. """
    def __init__(self):
        self.logger = logging.getLogger("filter-test")
        self.parameters = lambda: None
        self.parameters.rules_dir = "/mnt/intelmq-beta" + "/opt/intelmq/etc/filters/" #ma byt nastaveno v BOTS

        self.init()
        pass

    def acknowledge_message(self):
        pass
    def send_message(self, message):
        print("SENT")
        pass

    def receive_message(self):
        # XXX tato funkce musi dedit od Bot
        return {"feed": "arbor",
            "source_cymru_cc": "CO",
            "reported_source_ip": "190.255.48.99",
            "feed_url": "http://atlas-public.ec2.arbor.net/public/ssh_attackers",
            "source_time": "2015-04-07T00:00:00+00:00",
            "taxonomy": "Intrusion Attempts",
            "observation_time": "2015-04-07T12:15:39",
            "source_ip": "190.255.48.99",
            "source_registry": "lacnic",
            "source_allocated": "2008-04-22",
            "source_bgp_prefix": "190.255.48.0/20",
            "type": "brute-force",
            "source_as_name": "COLOMBIA TELECOMUNICACIONES S.A. ESP,CO",
            "source_asn": "3816"
            }
        return {"filter": {
        "Taxonomy": [
            "Malicious Code",
            "Intrusion Attempts"
        ],
        "Type": [
            "botnet drone",
            "c&c"
        ],
        "ASN": [
            "25761",
            "54600"
        ],
        "CIDR": [
            "192.168.100.0/24",
            "10.10.25.38/32"
        ],
        "Recipient": [
            "karel@seznam.cz",
        ],
        "CC": [
            "DE"
        ]
    }}

class CustomFilterBot(Bot):
    """ Filter bot has filters. Filters have conditions. """

    filters = {}

    def meet_condition(self, message):
        for filterI in CustomFilterBot.filters:
            filter = CustomFilterBot.filters[filterI]
            logging.debug("Rule: {}".format(filter))
            including = True if filter["type"] == "include" else False # typ filtru
            conforming = True # message odpovida vsem podminkam filteru

            for condition in filter["conditions"]:                                
                # aby filter odpovidal, musi odpovidat vsechny pravidla filtru
                #logging.debug("Filter: {} {}".format(filter["conditions"][condition], "n/a" if condition not in message else message[condition]))

                if not message.value(condition):
                    if including: # podminka v message neexistuje, ale mela by
                        self.logger.warning("[{}] Condition does not exist: condition {}, value {} ".format(filter["name"],condition, message.value(condition)))
                        return False
                    self.logger.warning("[{}] Okay, condition does not exist: condition {}, value {} ".format(filter["name"],condition, message.value(condition)))
                    conforming = False
                    break
                else: # podminka existuje
                    # aby podminka odpovidala, aspon jedna jeji hodnota musi odpovidat
                    passed = False
                    for value in filter["conditions"][condition]: # XX nefunguje wildcard *@isp.cz
                        if value == message.value(condition):
                            passed = True
                            self.logger.warning("[{}] Okay, value met: condition {}, value {} ".format(filter["name"],condition, message.value(condition)))
                            break
                    #logging.debug("F-conf: {}".format(passed))
                    if passed == False:
                        if including: # podminka neodpovida, ale mela by
                            self.logger.warning("[{}] No value met: condition {}, value {} ".format(filter["name"],condition, message.value(condition)))
                            return False
                        self.logger.warning("[{}] Okay, no value met: condition {}, value {} ".format(filter["name"],condition, message.value(condition)))
                        conforming = False
                        break

                #else: # subpravidlo existuje

            #logging.debug("Conf:{}".format(conforming))

            if conforming and including == False:
                #self.logger.warning("EXCLUDED\n\n") #logging.debug("EXCLUDED")
                return False # pravidlo celistve odpovida, ale nesmi


        #raise ValueError("Unknown filter type %s." % CustomFilterBot.filters.type)
        #return True # message odpovida vsem podminkam filteru tohoto rule
        #return False # message neodpovida zadnemu rule
        #logging.debug("PASSED")
        return True # zadny filter zpravu nevyloucil

    #def __init__(self, bot_id):
    #    self.logger.warning(" JINUDY ")
    #    super(D, self).__init__(bot_id)
    #    CustomFilterBot.filters = {}

    def init(self):
        """ Loads rules from .json """
        #self.logger.warning("BOT INIT")
        # load filter rules from json
        ruleI = 0
        for rule_file in glob(self.parameters.rules_dir + "*.json"):
            with open(rule_file, 'r') as f:                
                rule = json.load(f)                
                CustomFilterBot.filters[ruleI] = rule                
            ruleI += 1
            self.logger.warning(rule_file)

        #with open('rules.json') as data_file:
        #    CustomFilterBot.filters = json.load(data_file)
        self.logger.warning("Bot init succesful.")

    def process(self):
        self.logger.warning("Processing..")
        message = self.receive_message()

        #logging.warning("toto je zprava, co chceme videt:")
        #logging.warning(message)
        #print message
        #self.send_message(message)
        #quit()
        #print unicode(message["filter"]["CC"][0])
        #quit()


        if self.meet_condition(message):
            # propustit radek
            self.logger.warning("PASSED\n")
            self.send_message(message)
        else:
            # zahodit radek
            self.logger.warning("TRASHED\n")


        self.acknowledge_message() # dokoncil jsem praci (asi)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    #logging.debug("starts...")
    #b = CustomFilterBot()
    #b.process()
    #quit()
    #
    bot = CustomFilterBot(sys.argv[1])
    bot.start()
