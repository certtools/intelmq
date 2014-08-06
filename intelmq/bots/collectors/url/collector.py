from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class URLCollectorBot(Bot):

    def process(self):
        report = fetch_url(self.parameters.url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = URLCollectorBot(sys.argv[1])
    bot.start()
