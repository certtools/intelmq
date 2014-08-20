"""
Shadowserver QOTD report parser

Based on drone-report-parser.py, adapted by Kris Boulez (CERT.be) <kris.boulez@cert.be>

"""

from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
import StringIO, csv
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class ShadowServerQotdReportParserBot(Bot):

    def process(self):
        report = self.receive_message()
        report = report.strip()

        if report:

            # "timestamp","ip","protocol","port","hostname","tag","quote","asn","geo","region","city"
            columns = {
                "timestamp": "source_time",
                "ip": "reported_ip",
                "protocol" : "__IGNORE__",
                "port" : "destination_port",
                "hostname": "destination_reverse_dns",
                "tag" : "__TDB__",
                "quote" : "__IGNORE__",
                "asn": "reported_asn",
                "geo": "reported_cc",
                "region" : "__TDB__",
                "city" : "__TDB__",
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
                event.add('feed code', 'SHQOTDB')
                #event.add('feed_url', 'TBD')
                event.add('type', 'vulnerable service')
                event.add('protocol', 'QOTD')

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
    bot = ShadowServerQotdReportParserBot(sys.argv[1])
    bot.start()
