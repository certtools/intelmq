from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

import csv
import StringIO
import lib


class DCUParserBot(Bot):
    """ Parses DCU-Collector output. """

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()
            buffered = StringIO.StringIO(report)
            rows = csv.DictReader(buffered,
                                  delimiter="\t",
                                  fieldnames=lib.dcu_headers())

            for row in rows:
                event = Event()
                event.add("feed", "microsoft-dcu")
                add_dcu_fields(event, row)

                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)

                self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DCUParserBot(sys.argv[1])
    bot.start()
