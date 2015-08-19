import urlparse
from intelmq.lib import utils
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.lib.harmonization import DateTime, IPAddress


class VXVaultParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if not report:
            self.acknowledge_message()
            return
        if not report.contains("raw"):
            self.acknowledge_message()

        raw_report = utils.base64_decode(report.value("raw"))
        for row in raw_report.split('\n'):

            row = row.strip()

            if len(row) == 0 or not row.startswith('http'):
                continue

            url_object = urlparse.urlparse(row)

            if not url_object:
                continue

            url      = url_object.geturl()
            hostname = url_object.hostname
            port     = url_object.port

            event = Event()

            if IPAddress.is_valid(hostname, sanitize=True):
                event.add("source.ip", hostname, sanitize=True)
            else:
                event.add("source.fqdn", hostname, sanitize=True)

            time_observation = DateTime().generate_datetime_now()
            event.add('time.observation', time_observation, sanitize=True)
            event.add('feed.name', report.value("feed.name"))
            event.add('feed.url', report.value("feed.url"))
            event.add('classification.type', u'malware')
            event.add("source.url", url, sanitize=True)
            event.add("source.port", str(port), sanitize=True)
            event.add("raw", row, sanitize=True)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultParserBot(sys.argv[1])
    bot.start()
