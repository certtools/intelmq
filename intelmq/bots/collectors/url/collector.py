from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.url.lib import fetch_url

class URLCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report from %s" % self.parameters.url)
        report = fetch_url(self.parameters.url, timeout = 60.0, chunk_size = 16384, http_proxy=self.parameters.http_proxy, https_proxy=self.parameters.https_proxy)
        self.logger.info("Report downloaded.")
        self.send_message(report)


if __name__ == "__main__":
    bot = URLCollectorBot(sys.argv[1])
    bot.start()
