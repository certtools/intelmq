# -*- coding: utf-8 -*-
import html

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import ClassificationType

TAXONOMY = {
    "brute force": "brute-force",
    "bruteforce": "brute-force",
    "scan": "scanner",
    "cve": "exploit",
    "sql inject": "exploit",
}


class AutoshunParserBot(ParserBot):

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        split = raw_report.split("</tr>")
        self.tempdata = ['</tr>'.join(split[:2])]
        # TODO: save ending line
        for line in split[2:]:
            yield line.strip()

    def parse_line(self, line, report):
        event = self.new_event(report)

        info = line.split("<td>")
        if len(line) <= 0 or len(info) < 3:
            return

        ip = info[1].split('</td>')[0].strip()
        last_seen = info[2].split('</td>')[0].strip() + '-05:00'
        description = html.unescape(info[3].split('</td>')[0].strip())

        for key in ClassificationType.allowed_values:
            if description.lower().find(key.lower()) > -1:
                event.add("classification.type", key)
                break
        else:
            for key, value in TAXONOMY.items():
                if description.lower().find(key.lower()) > -1:
                    event.add("classification.type", value)
                    break

        if "classification.type" not in event:
            event.add("classification.type", 'unknown')

        event.add("time.source", last_seen)
        event.add("source.ip", ip)
        event.add("event_description.text", description)
        event.add("raw", line + "</tr>")
        yield event


BOT = AutoshunParserBot
