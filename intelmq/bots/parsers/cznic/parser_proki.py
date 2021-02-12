# -*- coding: utf-8 -*-
import json

from intelmq.lib import utils
from intelmq.lib.bot import ParserBot


class CZNICProkiParserBot(ParserBot):

    recover_line = ParserBot.recover_line_json

    def parse(self, report):
        raw_report = utils.base64_decode(report.get("raw"))
        report = json.loads(raw_report)

        if isinstance(report, dict) and "data" in report:
            # extract event list from received JSON
            report = report.get("data")

        for line in report:
            yield line

    def parse_line(self, line, report):
        event = self.new_event(report)

        # json keys map 1:1 to harmonization fields
        for field in line:
            if field == "feed.name":
                event.add("extra.original_feed_name", line.get(field))
            elif field == "time.observation":
                event.add("extra.original_time_observation", line.get(field))
            else:
                event.add(field, line.get(field))
        event.add("raw", self.recover_line(line))

        yield event


BOT = CZNICProkiParserBot
