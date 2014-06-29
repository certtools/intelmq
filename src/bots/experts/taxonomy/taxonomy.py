import sys
from lib.bot import *
from lib.utils import *
from lib.event import *

TAXONOMY = {
            "spam"                      : "Abusive Content",
            "malware"                   : "Malicious Code",
            "botnet drone"              : "Malicious Code",
            "ransomware"                : "Malicious Code",
            "malware configuration"     : "Malicious Code",
            "c&c"                       : "Malicious Code",
            "scanner"                   : "Information Gathering",
            "exploit"                   : "Intrusion Attempts",
            "brute-force"               : "Intrusion Attempts",
            "ids alert"                 : "Intrusion Attempts",
            "defacement"                : "Intrusions",
            "backdoor"                  : "Intrusions",
            "ddos"                      : "Availability",
            "dropzone"                  : "Information Content Security",
            "phishing"                  : "Fraud",
            "vulnerable service"        : "Vulnerable",
            "blacklist"                 : "Other",
            "test"                      : "Test"
           }


class TaxonomyExpertBot(Bot):
    
    def process(self):
        event = self.receive_message()
        if event:
            
            type = event.value("type")
            taxonomy = TAXONOMY[type]
            event.add("taxonomy",taxonomy)
            
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = TaxonomyExpertBot(sys.argv[1])
    bot.start()
