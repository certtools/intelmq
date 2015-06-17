import unicodecsv
from cStringIO import StringIO
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime

class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        columns = ["__IGNORE__", "source.url", "description", "time.source", "__IGNORE__", "__IGNORE__", "__IGNORE__", "target"]
        
        raw_report = utils.base64_decode(report.value("raw"))
        for row in unicodecsv.reader(StringIO(raw_report), encoding='utf-8', errors='ignore'):

            self.logger.error("raw: %s - %s" % (type(row), row))

            # ignore headers
            if "phish_id" in row:
                continue
            
            event = Event()
            
            for key, value in zip(columns, row):
                if key == "__IGNORE__":
                    continue
                
                event.add(key, value, sanitize=True)
                            
            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', u'phishtank')
            event.add('feed.url', u'http://data.phishtank.com/data/< API KEY >/online-valid.csv')
            event.add('classification.type', u'phishing')
            res = ",".join(row)
            self.logger.error("res: %r - %r" % (type(res), res))
            event.add("raw", res, sanitize=True)            
            #event.add("raw", ",".join(row), sanitize=True)            

            self.send_message(event)            
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
