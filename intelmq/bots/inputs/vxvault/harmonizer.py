from intelmq.lib.bot import Bot, sys

class VXVaultHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()
        
        if event:
            event.add('feed', 'vxvault')
            event.add('feed_url', 'http://vxvault.siri-urz.net/URL_List.php')
            ip_value = event.value('ip')
            event.add('source_ip', ip_value)
            event.add('reported_ip', ip_value)
            event.add('type', 'malware')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultHarmonizerBot(sys.argv[1])
    bot.start()
