import urlparse
from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

class VXVaultParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
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
                event.add("source_url", url)
                event.add("source_domain_name", hostname)
                if port:
                    event.add("source_port", str(port))

                event.add('feed', 'vxvault')
                event.add('feed_url', 'http://vxvault.siri-urz.net/URL_List.php')
                event.add('type', 'malware')
                
                event = utils.generate_source_time(event, "source_time")
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultParserBot(sys.argv[1])
    bot.start()
