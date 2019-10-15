# -*- coding: utf-8 -*-
from intelmq.lib import utils
from intelmq.lib.bot import Bot


class SurblParserBot(Bot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report["raw"])  # decoding
        lines = [line for line in raw_report.splitlines()][9:-2]
        for line in lines:
            if line[0] == ":":
                attributes = line.split()[-3][1:-2].split("][")
                if "mw" in attributes:
                    attribute = "malware"
                elif "ph" in attributes:
                    attribute = "phishing"
                else:
                    attribute = "blacklist"
            elif line[0] == ".":
                event = self.new_event(report)
                event.add("source.fqdn", line[1:])
                event.add("classification.type", attribute)
                event.add("raw", line)
                self.send_message(event)
        self.acknowledge_message()


BOT = SurblParserBot
