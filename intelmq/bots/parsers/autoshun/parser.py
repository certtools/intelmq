import HTMLParser
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime

TAXONOMY = {
    "brute force": "brute-force",
    "bruteforce": "brute-force",
    "scan": "scanner",
    "cve": "exploit",
    "sql inject": "exploit",
    "c&c": "c&c",
    "spam": "spam"
}


class AutoshunParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        raw_report_splitted = raw_report.split("</tr>")[2:]

        parser = HTMLParser.HTMLParser()

        for row in raw_report_splitted:
            event = Event()

            row = row.strip()

            if len(row) <= 0:
                continue

            info = row.split("<td>")
            if len(info) < 3:
                continue

            ip = info[1].split('</td>')[0].strip()
            last_seen = info[2].split('</td>')[0].strip()
            description = parser.unescape(info[3].split('</td>')[0].strip())

            for key in Parser.taxonomy.keys():
                if description.lower().find(key.lower()) > -1:
                    event.add("classification.type", TAXONOMY[key], sanitize=True)
                    break

            if not event.contains("classification.type"):
                event.add("classification.type", u'unknown')

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add("time.source", last_seen, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add("source.ip", ip, sanitize=True)
            event.add("description.text", description, sanitize=True)
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = AutoshunParserBot(sys.argv[1])
    bot.start()
