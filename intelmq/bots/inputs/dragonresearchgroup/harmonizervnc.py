from intelmq.lib.bot import Bot, sys

class DragonResearchGroupVNCHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            event.add('feed', 'dragonresearchgroup')
            event.add('feed_url', 'http://dragonresearchgroup.org/insight/vncprobe.txt')
            ip_value = event.value('reported_ip')
            event.add('source_ip', ip_value)
            event.add('ip', ip_value)
            event.add('type', 'brute-force')
            
            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DragonResearchGroupVNCHarmonizerBot(sys.argv[1])
    bot.start()

