from intelmq.lib.bot import Bot, sys
from intelmq.lib import sanitize

class DragonResearchGroupSSHHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            event.add('feed', 'dragonresearchgroup')
            event.add('feed_url', 'http://dragonresearchgroup.org/insight/sshpwauth.txt')
            event.add('type', 'brute-force')

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
    bot = DragonResearchGroupSSHHarmonizerBot(sys.argv[1])
    bot.start()

