from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class DragonResearchGroupSSHParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()              

                if len(row) == 0 or row.startswith('#'): # ignore all lines starting with comment mark
                    continue
                
                row = row.split('|')
                event = Event()

                # malware = LOWER CASE
                        # "timestamp", "ip", "port", "asn", "geo", "region", "city", "hostname", "type", "infection", "url", "agent", "cc", "cc_port", "cc_asn", "cc_geo", "cc_dns", "count", "proxy", "application", "p0f_genre", "p0f_detail", "machine_name", "id"
                columns = ["source_time", "reported_ip", "source_port", "reported_asn", "reported_cc", "region", "city", "source_reverse_dns", "__IGNORE__", "malware", "__TDB__", "__TDB__", "destination_ip", "destination_port", "destination_asn", "destination_cc", "destination_reverse_dns", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__", "__TDB__"]
                
                for key, value in zip(columns, row):
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue
                    
                    if key is "malware":
                        event.add(key, value.strip().lower())
                        continue
                    
                    event.add(key, value.strip())
                    
                    
                event.add('feed', 'shadowserver')
                event.add('feed_url', 'http://dragonresearchgroup.org/insight/sshpwauth.txt')
                event.add('type', 'brute-force')
                event.add('protocol', 'ssh')

                ip_value = event.value('reported_ip')
                event.add('source_ip', ip_value)
                event.add('ip', ip_value)
                
                asn_value = event.value('reported_asn')
                event.add('asn', asn_value)
                
                as_name_value = event.value('reported_as_name')
                event.add('as_name', as_name_value)
                
                event = sanitize.source_time(event, "source_time")  
                event = sanitize.generate_observation_time(event, "observation_time")
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = DragonResearchGroupSSHParserBot(sys.argv[1])
    bot.start()
