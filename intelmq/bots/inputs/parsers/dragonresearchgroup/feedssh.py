from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class DragonResearchGroupSSHFeedBot(Bot):

    def process(self):
        url = "http://dragonresearchgroup.org/insight/sshpwauth.txt"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = DragonResearchGroupSSHFeedBot(sys.argv[1])
    bot.start()
