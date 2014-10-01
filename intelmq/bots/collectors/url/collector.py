from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Report
from intelmq.bots.collectors.url.lib import fetch_url

class URLCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report from %s" % self.parameters.url)
        report_text = fetch_url(self.parameters.url, timeout = 60.0, chunk_size = 16384)
        self.logger.info("Report downloaded.")
        
        report = Report()
        report.add('content', report_text)
        
        self.send_message(report)


if __name__ == "__main__":
    bot = URLCollectorBot(sys.argv[1])
    bot.start()
