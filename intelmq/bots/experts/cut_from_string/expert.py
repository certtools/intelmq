# -*- coding: utf-8 -*-
"""
Cut from string
"""
from intelmq.lib.bot import Bot


class CutFromStringExpertBot(Bot):
    string_from_start: bool = True  # True - from start, False - from end
    string_for_cut: str = 'www.'
    field: str = 'source.fqdn'

    def process(self):
        event = self.receive_message()

        if self.field in event:
            field_string = event[self.field]
            if self.string_from_start and field_string.startswith(self.string_for_cut):
                field_string = field_string[len(self.string_for_cut):]
                event.change(self.field, field_string)

            if not self.string_from_start and field_string.endswith(self.string_for_cut):
                field_string = field_string[:-len(self.string_for_cut)]
                event.change(self.field, field_string)

        self.send_message(event)
        self.acknowledge_message()


BOT = CutFromStringExpertBot
