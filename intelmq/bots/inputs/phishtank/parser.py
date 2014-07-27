import StringIO, csv
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event

class PhishTankParserBot(Bot):

    def process(self):
        report = self.receive_message()
        report = report.strip()

        if report:
            columns = ["__IGNORE__", "url", "description_url", "source_time", "__IGNORE__", "__IGNORE__", "__IGNORE__", "target"] # ignore (__IGNORE__) fields specific to the source and other irrelevant fields
            rows = csv.DictReader(StringIO.StringIO(report), fieldnames = columns)

            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    if key is "__IGNORE__":
                        continue

                    event.add(key, value)
                self.send_message(event)
                
        self.acknowledge_message()


if __name__ == "__main__":
    bot = PhishTankParserBot(sys.argv[1])
    bot.start()
