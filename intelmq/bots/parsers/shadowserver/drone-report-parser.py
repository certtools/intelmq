from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
import StringIO, csv
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class ShadowServerDroneReportParserBot(Bot):

    def process(self):
        report = self.receive_message()
        report = report.strip()

        if report:
            
            columns = {
                "timestamp": "source_time",
                "ip": "reported_ip",
                "port": "source_port",
                "asn": "reported_asn",
                "geo": "reported_cc",
                "region": "region",
                "city": "city",
                "hostname": "source_reverse_dns",
                "type": "__IGNORE__",
                "infection": "malware",
                "url": "__TDB__",
                "agent": "__TDB__",
                "cc": "destination_ip",
                "cc_port": "destination_port",
                "cc_asn": "destination_asn",
                "cc_geo": "destination_cc",
                "cc_dns": "destination_reverse_dns",
                "count": "__TDB__",
                "proxy": "__TDB__",
                "application": "__TDB__",
                "p0f_genre": "__TDB__",
                "p0f_detail": "__TDB__",
                "machine_name": "__TDB__",
                "id": "__TDB__"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue
                    
                    if key is "malware":
                        value = value.strip().lower()                    
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver')
                #event.add('feed_url', 'TBD')
                event.add('type', 'botnet drone')
                #event.add('protocol', 'TBD')

                ip_value = event.value('reported_ip')
                event.add('source_ip', ip_value)
                event.add('ip', ip_value)
                
                asn_value = event.value('reported_asn')
                event.add('asn', asn_value)
                
                event = sanitize.source_time(event, "source_time")  
                event = sanitize.generate_observation_time(event, "observation_time")
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerDroneReportParserBot(sys.argv[1])
    bot.start()
