from intelmq.lib.bot import Bot, sys
from intelmq.lib import sanitize

class VXVaultHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()
        
        if event:
            event.add('feed', 'vxvault')
            event.add('feed_url', 'http://vxvault.siri-urz.net/URL_List.php')
            event.add('type', 'malware')
            event = sanitize.generate_source_time(event, "source_time")
            event = sanitize.generate_observation_time(event, "observation_time")

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultHarmonizerBot(sys.argv[1])
    bot.start()
