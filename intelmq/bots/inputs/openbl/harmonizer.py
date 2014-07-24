from intelmq.lib.bot import Bot, sys

class OpenBLHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            event.add('feed', 'openbl')
            event.add('feed_url', 'http://www.openbl.org/lists/date_all.txt')
            ip_value = event.value('reported_ip')
            event.add('source_ip', ip_value)
            event.add('ip', ip_value)
            event.add('type', 'brute-force') # ???
            
            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = OpenBLHarmonizerBot(sys.argv[1])
    bot.start()
