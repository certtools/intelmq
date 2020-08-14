# -*- coding: utf-8 -*-
import csv
import dateutil.parser

from intelmq.lib.bot import ParserBot


class CertBundAvalancheParserBot(ParserBot):

    parse = ParserBot.parse_csv_dict
    recover_line = ParserBot.recover_line_csv_dict

    csv_params = {"quoting": csv.QUOTE_ALL}

    def parse_line(self, line, report):
        event = self.new_event(report)

        event.add("source.asn", line["asn"])
        event.add("source.ip", line["ip"])
        event.add("time.source", str(dateutil.parser.parse(line["timestamp"] + " UTC")))
        event.add("classification.type", "malware")
        event.add("malware.name", line["malware"])

        if len(line["src_port"]):
            event.add("source.port", line["src_port"])
        if len(line["dst_ip"]):
            event.add("destination.ip", line["dst_ip"])
        if len(line["dst_port"]):
            event.add("destination.port", line["dst_port"])
        if len(line["dst_host"]):
            event.add("destination.fqdn", line["dst_host"])

        event.add("protocol.transport", line["proto"])
        event.add("raw", self.recover_line(line, strip=False))

        yield event


BOT = CertBundAvalancheParserBot
