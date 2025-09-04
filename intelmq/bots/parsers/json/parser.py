# SPDX-FileCopyrightText: 2016 by Bundesamt für Sicherheit in der Informationstechnik, 2016-2021 nic.at GmbH, 2024 Tim de Boer, 2025 Institute for Common Good Technology
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
JSON Parser Bot
Retrieves a base64 encoded JSON-String from raw and converts it into an
event.
"""
from intelmq.lib.bot import ParserBot
from intelmq.lib.message import MessageFactory
from intelmq.lib.utils import base64_decode
from json import loads as json_loads, dumps as json_dumps


class JSONParserBot(ParserBot):
    """Parse IntelMQ-JSON data"""
    splitlines: bool = False
    multiple_events: bool = False

    def init(self):
        if self.multiple_events and self.splitlines:
            raise ValueError("Modes 'splitlines' and 'multiple_events' are not possible at the same time. Please use either one.")

    def process(self):
        report = self.receive_message()
        if self.multiple_events:
            lines = json_loads(base64_decode(report["raw"]))
        elif self.splitlines:
            lines = base64_decode(report["raw"]).splitlines()
        else:
            lines = [base64_decode(report["raw"])]

        for line in lines:
            event = self.new_event(report)
            if self.multiple_events:
                event.update(MessageFactory.from_dict(line,
                                                      harmonization=self.harmonization,
                                                      default_type="Event"))
                event["raw"] = json_dumps(line, sort_keys=True)
            else:
                event.update(MessageFactory.unserialize(line,
                                                        harmonization=self.harmonization,
                                                        default_type="Event"))
                event.add('raw', line, overwrite=False)
            event.add("classification.type", "undetermined", overwrite=False)  # set to undetermined if input has no classification
            self.send_message(event)
        self.acknowledge_message()


BOT = JSONParserBot
