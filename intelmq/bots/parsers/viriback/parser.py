# -*- coding: utf-8 -*-
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class ViribackParserBot(ParserBot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])
        iocs = raw_report.splitlines()[78].strip()[8:-10].split("</td></tr><tr><td>")
        for ioc in iocs:
            malware_type, url, ip, date = ioc.split("</td><td>")
            event = self.new_event(report)
            event.add("source.url", "http://" + url)
            event.add("raw", ioc)
            event.add("source.ip", ip)
            event.add("classification.type", "malware")
            event.add("classification.taxonomy", "malicious code")
            event.add("classification.identifier", malware_type)
            self.send_message(event)
        self.acknowledge_message()


BOT = ViribackParserBot
