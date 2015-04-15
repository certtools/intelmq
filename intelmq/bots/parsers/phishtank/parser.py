import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()
        
        if report:
            report = encode(report)
	    columns = {
		"phish_id": "__IGNORE__",   
		"url": "source_url",            
		"phish_detail_url": "description_url",
		"submission_time": "__IGNORE__",
		"verified": "__IGNORE__",
		"verification_time": "source_time",
		"online": "__IGNORE__",
		"target": "__IGNORE__"
            }
          
            
            for row in csv.DictReader(StringIO.StringIO(report)):
		event = Event()
                               
                for key, value in row.items():
		    
		    key = columns[key]
                    
		    if key == "__IGNORE__":
                        continue
                    
                    event.add(key, value.strip())
                
                event.add('feed', 'phishtank')
                event.add('type', 'phishing')

                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
		self.logger.info(event)
                    
                self.send_message(event)
             
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
