from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class DragonResearchGroupVNCParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()              

                if len(row) == 0 or row.startswith('#'): # ignore all lines starting with comment mark
                    continue
                
                row = row.split('|')
                event = Event()

                columns = ["reported_asn", "reported_as_name", "reported_ip", "source_time"]
                for key, value in zip(columns, row):
                    event.add(key, value.strip())
                    
                event.add('feed', 'dragonresearchgroup')
                event.add('feed_url', 'http://dragonresearchgroup.org/insight/vncprobe.txt')
                event.add('type', 'brute-force')
                event.add('protocol', 'vnc')

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
    bot = DragonResearchGroupVNCParserBot(sys.argv[1])
    bot.start()
