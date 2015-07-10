from intelmq.lib.bot import Bot, sys
from intelmq.bots.collectors.http.lib import fetch_url
from intelmq.lib.message import Report

class URLCollectorBot(Bot):

    def process(self):
        self.logger.info("Downloading report from %s" % self.parameters.url)
        raw_report = fetch_url(
                                self.parameters.url,
                                timeout = 60.0,
                                chunk_size = 16384,
                                http_proxy=self.parameters.http_proxy,
                                https_proxy=self.parameters.https_proxy,
                                user_agent = self.parameters.user_agent if hasattr(self.parameters, 'user_agent') else None
                            )
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", raw_report, sanitize=True)
        report.add("feed.name", self.parameters.feed, sanitize=True)
        report.add("feed.url", self.parameters.url, sanitize=True)
        self.send_message(report)


if __name__ == "__main__":
    bot = URLCollectorBot(sys.argv[1])
    bot.start()
