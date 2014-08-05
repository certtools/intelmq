from intelmq.lib.bot import Bot, sys
from intelmq.lib import sanitize

class ArborHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
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
    bot = ArborHarmonizerBot(sys.argv[1])
    bot.start()

