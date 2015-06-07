from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


class CERTEUMaliciousURLsParserBot(Bot):

    
    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):
                
            row = row.strip()
            
            if len(row) == 0:
                continue

            splitted_row = row.split('|')
            event = Event()

            columns = ["source.url", "source.asn", "source.ip", "time.source", "source.reverse_domain_name", "source.geolocation.cc", "__IGNORE__", "description"]
            
            for key, value in zip(columns, splitted_row):
                
                if key == "time.source":
                    value += " UTC"
                
                if value != "N/A" and key != "__IGNORE__":
                    event.add(key, value, sanitize=True)

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', u'cert-eu')
            event.add('classification.type', u'malware')
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = CERTEUMaliciousURLsParserBot(sys.argv[1])
    bot.start()
