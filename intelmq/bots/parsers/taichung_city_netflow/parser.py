import re
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


CLASSIFICATION = {
        "brute-force": [u"brute-force", u"brute force", u"mysql"],
        "c&c": [u"c&c server"],
        "botnet drone": [u"irc-botnet"],
        "malware": [u"malware provider", u"malware website", u'\u60e1\u610f', u"worm"],
        "scanner": [u"scan"],
        "exploit": [u"bash", u"php-cgi", u"phpmyadmin"],
    }


class TaichungCityNetflowParserBot(Bot):
    
    
    def get_type(self, value):
        value = value.lower()
        for event_type, keywords in CLASSIFICATION.iteritems():
            for keyword in keywords:
                if keyword in value:
                    return event_type
        return "unknown"
    

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('<tr>'):

            # Get IP and Type
            info1 = re.search(">[\ ]*(\d+\.\d+\.\d+\.\d+)[\ ]*<.*</td><td>([^<]+)</td>", row)
            
            if not info1:
                continue

            # Get Timestamp
            info2 = re.search("<td>[\ ]*(\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}:\d{2})[\ ]*</td>", row)

            event = Event()

            description = info1.group(2)
            description = utils.decode(description)
            event_type = self.get_type(description)
            time_observation = DateTime().generate_datetime_now()
            time_source = info2.group(1) + " UTC-8"

            event.add("time.source", time_source, sanitize=True)
            event.add('time.observation', time_observation, sanitize=True)
            event.add("source.ip", info1.group(1), sanitize=True)
            event.add('classification.type', event_type, sanitize=True)
            event.add('description.text', description, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("raw", row, sanitize=True)
        
            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = TaichungCityNetflowParserBot(sys.argv[1])
    bot.start()
