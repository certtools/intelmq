# -*- coding: utf-8 -*-
from html.parser import HTMLParser

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MyHTMLParser(HTMLParser):

    lsData = ""

    def handle_data(self, data):
        self.lsData = data

    def handle_starttag(self, tag, attrs):
        self.lsCSP = False  # boolean if attrs item is ('class', 'susp-row')
        if attrs == [('class', 'susp-row')]:
            self.lsCSP = True


parser = MyHTMLParser()


class WebinspektorParserBot(Bot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        report_list = [row.strip() for row in raw_report.splitlines()]
        index = 0
        while parser.lsData != "Details":
            index += 1
            parser.feed(report_list[index])
        while report_list[index] != "</table>":
            index += 1
            parser.feed(report_list[index])
            if parser.lsCSP:
                index += 1
                parser.feed(report_list[index])
                event = self.new_event(report)
                raw_url_line = report_list[index]
                event.add("source.url", parser.lsData)
                event.add("classification.type", "blacklist")
                index += 1
                parser.feed(report_list[index])
                event.add("classification.identifier", parser.lsData)
                event.add("classification.taxonomy", "other")
                index += 1
                parser.feed(report_list[index])
                event.add("time.source", parser.lsData)
                event.add("raw", raw_url_line + report_list[index])
                self.send_message(event)
        self.acknowledge_message()


BOT = WebinspektorParserBot
