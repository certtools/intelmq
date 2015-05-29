from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

import csv
import StringIO
from intelmq.bots.parsers.dcu.lib import *


class DCUParserBot(Bot):
    # This bot parses the data which was produced by the
    # dcu collector. It is for the Microsoft digital crime unit feed

    HEADERS = ["SourcedFrom", "FileTimeUtc",
               "Botnet", "SourceIp", 
               "SourcePort", "SourceIpAsnNr", 
               "TargetIp", "TargetPort", 
               "Payload", "SourceIpCountryCode", 
               "SourceIpRegion", "SourceIpCity", 
               "SourceIpPostalCode", "SourceIpLatitude", 
               "SourceIpLongitude", "SourceIpMetroCode", 
               "SourceIpAreaCode", "HttpRequest", 
               "HttpReferrer", "HttpUserAgent", 
               "HttpMethod", "HttpVersion", 
               "HttpHost", "Custom Field 1", 
               "Custom Field 2", "Custom Field 3", 
               "Custom Field 4", "Custom Field 5"]


    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()
            buffered = StringIO.StringIO(report)
            rows = csv.DictReader(buffered, delimiter="\t", fieldnames=self.HEADERS)

            for row in rows:
                event = Event()
                event.add("feed", "microsoft_dcu")
                for key, value in row.items():
                    parts = convert_dcu_field(key, value)
                    if parts:
                        event.add(parts[0], parts[1])
                    
                self.send_message(event)
        self.acknowledge_message()
        

if __name__ == "__main__":
    bot = DCUParserBot(sys.argv[1])
    bot.start()
