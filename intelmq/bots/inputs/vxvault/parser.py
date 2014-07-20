import urlparse
from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
from intelmq.lib.event import Event

class VXVaultParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()
                row = decode(row)

                if len(row) == 0 or not row.startswith('http'):
                    continue
                
                url_object = urlparse.urlparse(row)

                if not url_object:
                    continue

                url      = url_object.geturl() 
                hostname = url_object.hostname
                port     = url_object.port

                event = Event()
                event.add("url", url)
                event.add("domain_name", hostname)
                if port:
                    event.add("port", str(port))

                self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultParserBot(sys.argv[1])
    bot.start()
