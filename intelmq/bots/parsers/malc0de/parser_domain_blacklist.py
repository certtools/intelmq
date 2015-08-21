from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


class Malc0deDomainBlacklistParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report is None or not report.contains("raw"):
            self.acknowledge_message()
            return

        raw_report = utils.base64_decode(report.value("raw"))

        for row in raw_report.split('\n'):

            row = row.strip()
            if row == "" or row[:2] == "//":
                continue

            event = Event()

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('classification.type', u'malware')
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('source.fqdn', row.split(" ")[1], sanitize=True)
            event.add('raw', row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = Malc0deDomainBlacklistParserBot(sys.argv[1])
    bot.start()
