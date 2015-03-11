import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerSandboxUrlParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
                "asn": "source_asn",
		"geo": "source_cc",
		"md5hash": "artifact_hash",
		"url" : "reported_destination_url",
                "user_agent" : "user_agent",
                "host": "reported_destination_reverse_dns",
                "method": "comment"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue
                    
                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
		    if key== "comment":
			value ="HTTP Method ->"+value
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-Sandbox-Url')
                event.add('type', 'malware')
		event.add('artifact_hash_type','MD5')
                

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerSandboxUrlParserBot(sys.argv[1])
    bot.start()
