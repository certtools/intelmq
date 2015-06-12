from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime


class ArborParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):
            row = row.strip()

            if len(row) == 0 or row.startswith('other'):
                continue

            event = Event()
                
            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'brute-force')
            event.add("raw", row, sanitize=True)

            columns = ["source.ip"]
            row = row.split()

            for key, value in zip(columns, row):
                event.add(key, value, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
