from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

import lib


class DCUParserBot(Bot):
    """ Parses DCU-Collector output. """

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()
            headers = lib.dcu_headers()    
       
            rows = report.split("\n")

            for row in rows:
                try: 
                    columns = row.strip().split("\t")
                    fields = dict(zip(headers, columns))

                    event = Event(lib.convert_dcu_fields(fields))
                    event.add("feed", "microsoft-dcu")

                    event = utils.generate_observation_time(event, "observation_time")
                    event = utils.generate_reported_fields(event)

                    self.send_message(event)
                except lib.ParsingError as exc:
                    msg = "Got a parsing problem: %s affected row '%s' IGNORING AND CONTINUING" % (exc.message, row.strip())
                    self.logger.warning(msg, exc_info=True)
                    continue
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DCUParserBot(sys.argv[1])
    bot.start()
