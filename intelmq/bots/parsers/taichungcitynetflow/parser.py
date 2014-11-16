from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils
import re

KEYWORDS = {
        "brute-force": ["brute-force", "brute force", "mysql"],
        "c&c": ["c&c server"],
        "botnet drone": ["irc-botnet"],
        "malware": ["malware provider", "malware website", u'\u60e1\u610f', "worm"],
        "scanner": ["scan"],
        "exploit": ["bash", "php-cgi", "phpmyadmin"],
    }

class TaichungCityNetflowParserBot(Bot):
    
    def get_type(self, value):
        value = value.lower()
        for event_type, keywords in KEYWORDS.iteritems():
            for keyword in keywords:
                if unicode(keyword) in value:
                    return event_type
        return "unknown"

    def process(self):
        report = self.receive_message()

        for row in report.split('<tr>'):

            # Get IP and Type
            info1 = re.search(">[\ ]*(\d+\.\d+\.\d+\.\d+)[\ ]*<.*</td><td>([^<]+)</td>", row)
            
            # Get Timestamp
            info2 = re.search("<td>[\ ]*(\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})[\ ]*</td>", row)

            if info1:
                event = Event()

                event.add("source_ip", info1.group(1))
                description = info1.group(2)
                event_type = self.get_type(description)
                event.add('type', event_type)
                event.add('description', description)
                event.add("source_time", info2.group(1) + " UTC-8")
                event.add('feed', 'taichungcitynetflow')
                event.add('feed_url', 'https://tc.edu.tw/net/netflow/lkout/recent/30')

                event = utils.parse_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
            
                self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = TaichungCityNetflowParserBot(sys.argv[1])
    bot.start()