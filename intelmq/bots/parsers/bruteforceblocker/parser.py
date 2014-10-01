from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re

class BruteForceBlockerParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            regex_ip = "^[^ \t]+"
            regex_timestamp = "# ([^ \t]+ [^ \t]+)"
            
            for row in report.split('\n'):

                if row.startswith('#'):
                    continue

                event = Event()

                match = re.search(regex_ip, row)
                if match:
                    ip = match.group()
                    
                match = re.search(regex_timestamp, row)
                if match:
                    timestamp = match.group(1) + " UTC"
                
                event.add("source_ip", ip)
                event.add("source_time", timestamp)
                event.add('feed', 'bruteforceblocker')
                event.add('feed_url', 'http://danger.rulez.sk/projects/bruteforceblocker/blist.php')
                event.add('type', 'brute-force')

                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = BruteForceBlockerParserBot(sys.argv[1])
    bot.start()
