import unicodecsv
from io import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.utils import encode
from intelmq.bots import utils

class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()
        
        if report:
            event = Event()
            report = encode(report)

            # colums according to https://www.phishtank.com/developer_info.php as of 2015/04/30:
            #   phish_id,url,phish_detail_url,submission_time,verified,verification_time,online,target
            # example:
            # 123456,http://www.example.com/,http://www.phishtank.com/phish_detail.php?phish_id=123456,2009-06-19T15:15:47+00:00,yes,2009-06-19T15:37:31+00:00,yes,1st National Example Bank
            columns = ["__IGNORE__", "source_url", "description_url", "source_time", "__IGNORE__", "__IGNORE__", "__IGNORE__", "target"]
            
            for row in unicodecsv.reader(StringIO(report), encoding='utf-8'):

                if "phish_id" in row:
                    continue		# skip header
                
                for key, value in zip(columns, row):

                    if key == "__IGNORE__":
                        continue
                    
                    event.add(key, value.strip())
                
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
