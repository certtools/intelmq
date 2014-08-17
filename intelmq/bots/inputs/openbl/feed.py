from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class OpenBLFeedBot(Bot):

    def process(self):
        url = "http://www.openbl.org/lists/date_all.txt"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = OpenBLFeedBot(sys.argv[1])
    bot.start()

