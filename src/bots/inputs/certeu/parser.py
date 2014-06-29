import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
import traceback


class CERTEUParserBot(Bot):
    
    def process(self):
        print 'Waiting for report'
        report = self.receive_message()
        print 'Got report: %r' % report

        if report:
            for row in report.split('\n'):
                row = row.strip()
                if len(row) == 0:
                    continue

                row = force_decode(row).split('|')
                event = Event()

                columns = ["asn", "ip", "time", "ptr", "cc", "type", "additional_information"]
                for key, value in zip(columns, row):
                    event.add(key, value)

                self.send_message(event)
            self.acknowledge_message()


if __name__ == "__main__":
    bot = CERTEUParserBot(sys.argv[1])
    bot.start()
