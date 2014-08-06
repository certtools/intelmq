from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
from intelmq.lib.event import Event
from intelmq.lib import sanitize

class ArborParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()

                if len(row) == 0 or row.startswith('other'):
                    continue

                row = row.split()
                event = Event()

                columns = ["reported_ip"]
                for key, value in zip(columns, row):
                    event.add(key, value)
                    
                event.add('feed', 'arbor')
                event.add('feed_url', 'http://atlas-public.ec2.arbor.net/public/ssh_attackers')
                event.add('type', 'brute-force')
                
                ip_value = event.value('reported_ip')
                event.add('source_ip', ip_value)
                event.add('ip', ip_value)
                
                event = sanitize.generate_source_time(event, "source_time")
                event = sanitize.generate_observation_time(event, "observation_time")
                
                self.send_message(event)

        self.acknowledge_message()

if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
