from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class DragonResearchGroupVNCFeedBot(Bot):

    def process(self):
        url = "https://dragonresearchgroup.org/insight/vncprobe.txt"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = DragonResearchGroupVNCFeedBot(sys.argv[1])
    bot.start()
