# -*- coding: utf-8 -*-

from dateutil.parser import parse

from intelmq.lib.bot import ParserBot
from intelmq.lib.harmonization import DateTime
from intelmq.lib.message import Message
from intelmq.lib.utils import base64_decode
from intelmq.lib.harmonization import DateTime


class JSONCustomParserBot(ParserBot):

    def init(self):
        self.time_format = getattr(self.parameters, "time_format", None)
        if self.time_format and self.time_format.split('|')[0] not in DateTime.TIME_CONVERSIONS.keys():
            raise InvalidArgument('time_format', got=self.time_format,
                                  expected=list(DateTime.TIME_CONVERSIONS.keys()),
                                  docs='https://intelmq.readthedocs.io/en/latest/user/Bots.html#json-custom-parser')

        self.json_data_format = getattr(self.parameters, 'json_data_format', False)
        self.json_data_key = getattr(self.parameters, 'json_data_key', '')
        self.multiple_msg_field = getattr(self.parameters, 'multiple_msg_field', None)
        self.translate_fields = getattr(self.parameters, 'translate_fields', {})
        self.split_lines = getattr(self.parameters, 'splitlines', False)
        self.default_url_protocol = getattr(self.parameters, 'default_url_protocol', 'http://')
        self.classification_type = getattr(self.parameters, 'type')

    def flatten_json(self, json_object):
        out = {}

        def flatten(x, name='', separator='.'):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + separator)
            else:
                out[name[:-1]] = x

        flatten(json_object)
        return out

    def process(self):

        report = self.receive_message()
        raw_report = base64_decode(report["raw"])

        if self.json_data_format:
            lines = Message.unserialize(raw_report)[self.json_data_key]
        elif self.split_lines:
            lines = raw_report.splitlines()
        else:
            lines = [raw_report]

        for line in lines:
            if not line:
                continue

            msg = Message.unserialize(line) if not self.json_data_format else line
            flatten_msg = self.flatten_json(msg)
            event_msg = {}

            for key in self.translate_fields:
                data = flatten_msg.get(self.translate_fields[key])

                if key in ["time.source", "time.destination"]:
                    try:
                        data = int(data)
                    except ValueError:
                        pass
                    data = DateTime.convert(data, format=self.time_format)

                elif key.endswith('.url'):
                    if not data:
                        continue
                    if '://' not in data:
                        data = self.default_url_protocol + data

                event_msg[key] = data

            multiple_msgs = []
            if self.multiple_msg_field in event_msg and type(event_msg[self.multiple_msg_field]) is list:
                for value in event_msg[self.multiple_msg_field]:
                    new_msg = event_msg.copy()
                    new_msg[self.multiple_msg_field] = value
                    multiple_msgs.append(new_msg)
            else:
                multiple_msgs = [event_msg]

            for event_msg in multiple_msgs:
                event = self.new_event(report)
                event.update(event_msg)

                if self.classification_type and "classification.type" not in event:
                    event.add('classification.type', self.classification_type)
                event['raw'] = Message.serialize(line) if self.json_data_format else line

                self.send_message(event)

        self.acknowledge_message()


BOT = JSONCustomParserBot
