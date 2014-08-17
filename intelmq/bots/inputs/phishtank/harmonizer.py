from intelmq.lib.bot import Bot, sys

class PhishTankHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            event.add('feed', 'phishtank')
            event.add('feed_url', 'http://data.phishtank.com/data/online-valid.csv')
            event.add('type', 'phishing')
            self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankHarmonizerBot(sys.argv[1])
    bot.start()