import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class ShadowServerMicrosoftSinkholeParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()
            
            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
                "asn": "source_asn",
                "geo": "source_cc",
                "url": "__TBD__",
                "type": "__IGNORE__",
                "http_agent": "__TBD__",
                "tor": "__TBD__",
                "src_port": "source_port",
                "p0f_genre": "__TBD__",
                "p0f_detail": "__TBD__",
                "hostname": "source_reverse_dns",
                "dst_port": "destination_port",
                "http_host": "__TBD__",
                "http_referer": "__TBD__",
                "http_referer_asn": "__TBD__",
                "http_referer_ip": "__TBD__",
                "http_referer_geo": "__TBD__",
                "dst_ip": "destination_ip",
                "dst_asn": "destination_asn",
                "dst_geo": "destination_cc"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TBD__":
                        continue
                    
                    # set timezone explicitly to UTC as it is absent in the input
                    if key == "source_time":
                        value += " UTC"
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-microsoft-sinkhole')
                event.add('type', 'botnet drone')
                event.add('application_protocol', 'http')
                
                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerMicrosoftSinkholeParserBot(sys.argv[1])
    bot.start()
