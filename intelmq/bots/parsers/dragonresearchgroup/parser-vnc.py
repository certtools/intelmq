from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class DragonResearchGroupVNCParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()              

                if len(row) == 0 or row.startswith('#'): # ignore all lines starting with comment mark
                    continue
                
                row = row.split('|')
                event = Event()

                columns = ["source_asn", "source_as_name", "source_ip", "source_time"]
                
                for key, value in zip(columns, row):
                    value = value.strip()
                    
                    if key == "source_time":
                        value += " UTC"
                    
                    event.add(key, value)
                    
                event.add('feed', 'dragonresearchgroup')
                event.add('feed_url', 'http://dragonresearchgroup.org/insight/vncprobe.txt')
                event.add('type', 'brute-force')
                event.add('application_protocol', 'vnc')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
    

if __name__ == "__main__":
    bot = DragonResearchGroupVNCParserBot(sys.argv[1])
    bot.start()
