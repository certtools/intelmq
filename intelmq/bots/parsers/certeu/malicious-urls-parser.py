from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class CERTEUMaliciousURLsParserBot(Bot):
    
    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                
                row = row.strip()
                
                if len(row) == 0:
                    continue

                row = row.split('|')
                event = Event()

                columns = ["source_url", "source_asn", "source_ip", "source_time", "source_reverse_dns", "source_cc", "__IGNORE__", "additional_information"]
                
                for key, value in zip(columns, row):
                    value = value.strip()
                    
                    if key == "source_time":
                        value += " UTC"
                    
                    if value != "N/A" and key != "__IGNORE__":
                        event.add(key, value)
                        
                event.add('feed', 'cert-eu')
                event.add('type', 'malware')

                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)

                self.send_message(event)
            self.acknowledge_message()


if __name__ == "__main__":
    bot = CERTEUMaliciousURLsParserBot(sys.argv[1])
    bot.start()
