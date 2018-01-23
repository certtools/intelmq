from intelmq.lib.bot import ParserBot
from intelmq.lib import utils
import re

class SucuriParserBot(ParserBot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"]) # decoding
        raw_report = re.sub(r"<!--(.|\s|\n)*?-->", "", raw_report) # removing comments
        report_list = [row.strip() for row in raw_report.splitlines()]
        index = 0
        actual_line = report_list[index]
        while actual_line != "<h4>Hidden iframes</h4>": # displacement to target table
            index += 1
            actual_line = report_list[index]
        while actual_line[:8] != "</tbody>": # scrabing table data
            index += 1
            actual_line = report_list[index]
            if actual_line[:2] == "<t":
                event = self.new_event(report)
                event.add("source.url", actual_line.split("\"")[actual_line.count("\"")][1:].split("</a>")[0]) # taking pure data from html line
                self.send_message(event)
        self.acknowledge_message()


BOT = SucuriParserBot


