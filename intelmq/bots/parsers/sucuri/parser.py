from intelmq.lib.bot import ParserBot
from intelmq.lib import utils
import re
from html.parser import HTMLParser
import urllib.request as urllib2


class MyHTMLParser(HTMLParser):

    lsData = ""

    def handle_data(self,data):
        self.lsData = data


parser = MyHTMLParser()


class SucuriParserBot(ParserBot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"]) # decoding
        raw_report = re.sub(r"<!--(.|\s|\n)*?-->", "", raw_report) # removing comments
        report_list = [row.strip() for row in raw_report.splitlines()]
        index = 0
        actual_line = report_list[index]
        while parser.lsData != "Hidden iframes": # displacement to target table
            index += 1
            actual_line = report_list[index]
            parser.feed(actual_line)
        while actual_line[:8] != "</tbody>": # scrabing table data
            index += 1
            actual_line = report_list[index]
            if actual_line[:2] == "<t":
                event = self.new_event(report)
                parser.feed(report_list[index])
                event.add("source.url", parser.lsData)
                event.add("classification.type", "blacklist")
                event.add("classification.identifier", "hidden iframe")
                event.add("raw", actual_line)
                self.send_message(event)
        self.acknowledge_message()


BOT = SucuriParserBot


