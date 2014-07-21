from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import decode
from intelmq.lib.event import Event

class DragonResearchGroupParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()              

                if len(row) == 0 or row.startswith('#'): # ignore all lines starting with comment mark
                    continue
                
                row = decode(row).split('|')
                event = Event()

                columns = ["reported_asn", "reported_as_name", "reported_ip", "source_time"]
                for key, value in zip(columns, row):
                    event.add(key, value.strip())

                self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = DragonResearchGroupParserBot(sys.argv[1])
    bot.start()
