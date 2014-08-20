from intelmq.lib.bot import Bot, sys

class BruteForceBlockerHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            event.add('feed', 'bruteforceblocker')
            event.add('feed_url', 'http://danger.rulez.sk/projects/bruteforceblocker/blist.php')
            event.add('type', 'brute-force')
            self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = BruteForceBlockerHarmonizerBot(sys.argv[1])
    bot.start()
