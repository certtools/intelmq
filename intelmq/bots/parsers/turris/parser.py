import unicodecsv
from cStringIO import StringIO
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime

class TurrisGreylistParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))

        columns = [
                   "source.ip",
                   "__IGNORE__",
                   "description.text",
                   "__IGNORE__"
                  ]
        
        for row in unicodecsv.reader(StringIO(raw_report), encoding='utf-8'):

            # ignore headers
            if "Address,Country,Tags,ASN" in row:
                continue
            
            event = Event()
            
            for key, value in zip(columns, row):
                if key == "__IGNORE__":
                    continue
                
                event.add(key, value, sanitize=True)
                            
            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'scanner')
            event.add("raw", ",".join(row), sanitize=True)
            
            self.send_message(event)            
        self.acknowledge_message()


if __name__ == "__main__":
    bot = TurrisGreylistParserBot(sys.argv[1])
    bot.start()
