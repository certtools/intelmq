import re
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


REGEX_IP = "^(\d+\.\d+\.\d+\.\d+)"      # bug: this ignores IPv6 right now
REGEX_TIMESTAMP = "(\d+\-\d+\-\d+\s\d+\:\d+\:\d+)"


class DshieldParserBot(Bot):


    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            if row.startswith('#'):
                continue

            octets = list()
            match = re.search(REGEX_IP, row)
            if match:
                for octet in match.group().split('.'):
                    result = octet.lstrip('0')
                    if result == "":
                        result = "0"
                    octets.append(result)
                ip = ".".join(octets)
            else:
                continue
    
            match = re.search(REGEX_TIMESTAMP, row)
            if match:
                timestamp = match.group(1) + " UTC"
            else:
                continue
            
            event = Event()
            
            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add("time.source", timestamp, sanitize=True)
            event.add('feed.name', u'dshield')
            event.add('feed.url', u'http://dshield.org/asdetailsascii.html')
            event.add('classification.type', u'brute-force')
            event.add("source.ip", ip, sanitize=True)
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = DshieldParserBot(sys.argv[1])
    bot.start()
