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
            
            # "timestamp", "ip", "port", "asn", "geo", "region", "city", "hostname", "type", "infection", "url", "agent", "cc", "cc_port", "cc_asn", "cc_geo", "cc_dns", "count", "proxy", "application", "p0f_genre", "p0f_detail", "machine_name", "id"
            
            columns = ["source_time", "reported_ip", "source_port", "reported_asn", "reported_cc", "region", "city", "source_reverse_dns", "__IGNORE__", "malware", "__TDB__", "__TDB__", "destination_ip", "destination_port", "destination_asn", "destination_cc", "destination_reverse_dns", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__"]
            
            print "1"
            rows = csv.DictReader(StringIO.StringIO(report), fieldnames = columns)
            print "2"
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    print value
                    
                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue
                    
                    if key is "malware":
                        value = value.strip().lower()                    
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver')
                #event.add('feed_url', 'TBD')
                event.add('type', 'bot')
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
