import StringIO, csv, re
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event

class BruteForceBlockerParserBot(Bot):

    def process(self):
        report = self.receive_message()
        report = report.strip()

        if report:
	    columns = ["source_ip", "__IGNORE__", "source time", "__IGNORE__" , "count", "ID"]
            rows = csv.DictReader(StringIO.StringIO(content), fieldnames = columns, dialect="excel-tab", delimiter='\t')

            for row in rows:

                event = Event()
                for key, value in row.items():

                    if key is "__IGNORE__":
                        continue

		    if key is "source time":
			row['source time'].strip('#')
	
                    event.add(key, value)

                self.send_message(event)
                
        self.acknowledge_message()


if __name__ == "__main__":
    bot = BruteForceBlockerParserBot(sys.argv[1])
    bot.start()
