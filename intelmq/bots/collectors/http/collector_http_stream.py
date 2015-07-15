import pycurl
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Report

class HTTPStreamCollectorBot(Bot):

    def init(self):
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.URL, str(self.parameters.url))
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)

    def process(self):
        self.conn.perform()

    def on_receive(self, data):
        for line in data.split('\n'):

            line = line.strip()
            if line == "":
                continue

            report = Report()
            report.add("raw", str(line), sanitize=True)
            report.add("feed.name", self.parameters.feed, sanitize=True)
            self.send_message(report)


if __name__ == "__main__":
    bot = HTTPStreamCollectorBot(sys.argv[1])
    bot.start()
