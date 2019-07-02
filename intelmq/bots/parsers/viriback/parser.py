# -*- coding: utf-8 -*-
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    iocs_data = []

    def handle_data(self, data):
        self.iocs_data.append(data)

class ViribackParserBot(ParserBot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        parser = MyHTMLParser()
        parser.feed(raw_report.splitlines()[78].strip())
        for malware_type, url, ip, date in [parser.iocs_data[i:i+4] for i in range(0, len(parser.iocs_data), 4)]:
            event = self.new_event(report)
            event.add("source.url", "http://" + url)
            event.add("raw", "</td><td>".join([malware_type, url, ip, date]))
            event.add("source.ip", ip)
            event.add("classification.type", "malware")
            event.add("classification.taxonomy", "malicious code")
            event.add("classification.identifier", malware_type)
            self.send_message(event)
        self.acknowledge_message()


BOT = ViribackParserBot
