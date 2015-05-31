import datetime
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


class OpenBLParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):
                
            row = row.strip()              

            if len(row) == 0 or row.startswith('#'):
                continue
            
            splitted_row = row.split()
            event = Event()

            columns = ["source.ip", "time.source"]
            
            for key, value in zip(columns, splitted_row):    
                if key == "time.source":
                    value = datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S') + " UTC"
                
                event.add(key, value.strip(), sanitize=True)

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', u'openbl')
            event.add('feed.url', u'http://www.openbl.org/lists/date_all.txt')
            event.add('classification.type', u'blacklist')
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = OpenBLParserBot(sys.argv[1])
    bot.start()

