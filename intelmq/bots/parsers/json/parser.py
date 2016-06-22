"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.

Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH
"""
import json
import io
import sys

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class JSONParserBot(Bot):

    def process(self):
        report = self.receive_message()

        raw = report.get("raw")
        raw_decoded = utils.base64_decode(raw)
        raw_json = None


        self.logger.debug("Raw Report: " + raw)
        self.logger.debug("Raw Decoded: " + raw_decoded)
        try:
            raw_json = json.loads(raw_decoded)
            self.logger.debug("Raw Json: " + str(raw_json))
        except:
            self.logger.error("Could not convert report to json")
            raise

        event = Event(raw_json)

        #for key, value in raw_json:
        #    try:
        #        event.add(key, value)
        #    except:
        #        self.logger.error("Could not add %s : %s to event",
        #                          key,
        #                          value)
        #event.add("raw",raw)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = JSONParserBot(sys.argv[1])
    bot.start()
