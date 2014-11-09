from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event
from intelmq.bots import utils
import re

class DshieldParserBot(Bot):

    def process(self):
        report = self.receive_message()

// Function to clean leading 0's maybe we need to add it to the sanitizer
    def cleanip(ip):
        ip = ".".join([octet.lstrip('0') for octet in ip.split('.')])
        return ip

        if report:
            regex_ip = "^(\d+\.\d+\.\d+\.\d+)"
            regex_timestamp = "(\d+\-\d+\-\d+\s\d+\:\d+\:\d+)"
            
            for row in report.split('\n'):

                if row.startswith('#'):
                    continue

                event = Event()

                match = re.search(regex_ip, row)
                if match:
                    ip = cleanip(match.group())
		
    
                match = re.search(regex_timestamp, row)
                if match:
                    timestamp = match.group(1) + " UTC"
                
                event.add("source_ip", ip)
                event.add("source_time", timestamp)
                event.add('feed', 'Dshield')
                event.add('feed_url', 'http://dshield.org/asdetailsascii.html')
                event.add('type', 'brute-force')

                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = DshieldParserBot(sys.argv[1])
    bot.start()
