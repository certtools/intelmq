import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event
from intelmq.bots import utils

class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()
            
            columns = ["__IGNORE__", "source_url", "description_url", "source_time", "__IGNORE__", "__IGNORE__", "__IGNORE__", "target"]
            rows = csv.DictReader(StringIO.StringIO(report), fieldnames = columns)

            for row in rows:
                event = Event()
                
                for key, value in row.items():
                    if key is "__IGNORE__":
                        continue
                    
                    event.add(key, value)
                    
                event.add('feed', 'phishtank')
                event.add('type', 'phishing')
                
                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                    
                self.send_message(event)
                
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
