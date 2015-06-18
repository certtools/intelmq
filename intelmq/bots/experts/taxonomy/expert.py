from intelmq.lib.bot import Bot, sys

# FIXME: this dict should be on a sparated file

TAXONOMY = {
            "phishing"                  : "Fraud",
            "ddos"                      : "Availability",
            "spam"                      : "Abusive Content",
            "scanner"                   : "Information Gathering",
            "dropzone"                  : "Information Content Security",
            "malware"                   : "Malicious Code",
            "botnet drone"              : "Malicious Code",
            "ransomware"                : "Malicious Code",
            "malware configuration"     : "Malicious Code",
            "c&c"                       : "Malicious Code",
            "exploit"                   : "Intrusion Attempts",
            "brute-force"               : "Intrusion Attempts",
            "ids alert"                 : "Intrusion Attempts",
            "defacement"                : "Intrusions",
            "compromised"               : "Intrusions",
            "backdoor"                  : "Intrusions",
            "vulnerable service"        : "Vulnerable",
            "blacklist"                 : "Other",
            "unknown"                   : "Other",
            "test"                      : "Test",
           }
           

class TaxonomyExpertBot(Bot):
    
    def process(self):
        event = self.receive_message()

        if not event.contains("classification.taxonomy") and event.contains("classification.type"):
            type = event.value("classification.type")
            taxonomy = TAXONOMY[type]
            event.add("classification.taxonomy", taxonomy, sanitize=True)
        
        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = TaxonomyExpertBot(sys.argv[1])
    bot.start()
