# -*- coding: utf-8 -*-
from html.parser import HTMLParser

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MyHTMLParser(HTMLParser):
    @property
    def set_empty_data(self):
        self.lsData = []
        self.raw_lines = []

    def handle_data(self, data):
        self.lsData.append(data)

    @property
    def process_data(self):
        self.lsData = self.lsData[:-2]
        self.raw_lines = self.raw_lines[:-2]


parser = MyHTMLParser()


class ThreatminerParserBot(Bot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        report_list = [row.strip() for row in raw_report.splitlines()]
        index = 0
        actual_line = report_list[index]
        while actual_line != "Recent domains":
            index += 1
            actual_line = report_list[index]
        parser.set_empty_data
        while actual_line != "Recent hosts":
            index += 1
            actual_line = report_list[index]
            count1 = len(parser.lsData)
            parser.feed(actual_line)
            count2 = len(parser.lsData)
            if count1 != count2:
                parser.raw_lines.append(actual_line)
        parser.process_data
        for item in range(len(parser.lsData)):
            event = self.new_event(report)
            event.add("source.fqdn", parser.lsData[item])
            event.add("classification.type", "blacklist")
            event.add("raw", parser.raw_lines[item])
            self.send_message(event)
        self.acknowledge_message()


BOT = ThreatminerParserBot
