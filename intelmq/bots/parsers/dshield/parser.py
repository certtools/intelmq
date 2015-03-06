from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re

class DshieldParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            regex_ip = "^(\d+\.\d+\.\d+\.\d+)"      # bug: this ignores IPv6 right now
            regex_timestamp = "(\d+\-\d+\-\d+\s\d+\:\d+\:\d+)"
            
            for row in report.split('\n'):

                if row.startswith('#'):
                    continue

                event = Event()

                match = re.search(regex_ip, row)
                if match:
                    ip = ".".join([octet.lstrip('0') for octet in match.group().split('.')])
                else:
                    continue    # skip lines without IP address
		
                match = re.search(regex_timestamp, row)
                if match:
                    timestamp = match.group(1) + " UTC"
                else:
                    continue    # no timestamp -> no event, skip this line
                
                event.add("source_ip", ip)
                event.add("source_time", timestamp)
                event.add('feed', 'dshield')
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
