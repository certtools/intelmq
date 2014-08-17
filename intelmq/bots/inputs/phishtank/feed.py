from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class PhishTankFeedBot(Bot):

    def process(self):
    	key = "b8dcd71742be6361cd83db13cd93153784c1aaa6b0f5d080d6de483239f4bd40" # replace by config field...
        url = "http://data.phishtank.com/data/%s/online-valid.csv" % (key)
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = PhishTankFeedBot(sys.argv[1])
    bot.start()
