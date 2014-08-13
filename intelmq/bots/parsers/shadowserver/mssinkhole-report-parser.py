"""
Shadowserver MS Sinkhole report parser

Based on drone-report-parser.py, adapted by Kris Boulez (CERT.be) <kris.boulez@cert.be>

"""


from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
import StringIO, csv
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class ShadowServerMSSinkholeReportParserBot(Bot):

    def process(self):
        report = self.receive_message()
        report = report.strip()

        if report:

            # "timestamp","ip","asn","geo","url","type","http_agent","tor","src_port","p0f_genre","p0f_detail","hostname","dst_port","http_host","http_referer","http_referer_asn","http_referer_geo","dst_ip","dst_asn","dst_geo"
            
            columns = {
                "timestamp": "source_time",
                "ip": "reported_ip",
                "asn": "reported_asn",
                "geo": "reported_cc",
		"url": "__TDB__",
                "type": "__IGNORE__",
		"http_agent": "__TDB__",
		"tor": "__TDB__",
                "src_port": "source_port",
		"p0f_genre": "__TDB__",
		"p0f_detail": "__TDB__",
                "hostname": "source_reverse_dns",
                "dst_port": "destination_port",
		"http_host": "__TDB__",
		"http_referer": "__TDB__",
		"http_referer_asn": "__TDB__",
		"http_referer_ip": "__TDB__",
		"http_referer_geo": "__TDB__",
                "dst_ip": "destination_ip",
                "dst_asn": "destination_asn",
                "dst_geo": "destination_cc",
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
                event.add('feed code', 'SHMSSINKB')
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
    bot = ShadowServerMSSinkholeReportParserBot(sys.argv[1])
    bot.start()
