from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import fetch_url

class VXVaultFeedBot(Bot):

    def process(self):
        url = "http://vxvault.siri-urz.net/URL_List.php"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = VXVaultFeedBot(sys.argv[1])
    bot.start()
