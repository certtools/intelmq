import sys
from intelmq.lib.bot import Bot
from intelmq.lib.utils import force_decode
from intelmq.lib.event import Event
#from intelmq.lib.cache import *

class ArborParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            for row in report.split('\n'):
                row = row.strip()

                if len(row) == 0 or row.startswith('other'):
                    continue

                row = force_decode(row).split()
                event = Event()

                columns = ["ip"]
                for key, value in zip(columns, row):
                    event.add(key, value)

                self.send_message(event)

        self.acknowledge_message()


if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
