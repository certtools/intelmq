import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class ArborParserBot(Bot):

    def process(self):
        report = self.pipeline.receive()

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

                self.pipeline.send(event)

        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = ArborParserBot(sys.argv[1])
    bot.start()
