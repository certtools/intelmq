# -*- coding: utf-8 -*-
"""
Cut from string
"""
from intelmq.lib.bot import Bot


class CutFromStringExpertBot(Bot):
    string_from_start: bool = True  # True - from start, False - from end
    string_for_cut: str = 'www.'
    field_for_cut: str = 'source.fqdn'

    def init(self):
        pass

    def process(self):
        event = self.receive_message()

        if self.field_for_cut in event:
            field_string = event[self.field_for_cut]
            if self.string_from_start == 1 and field_string.startswith(self.string_for_cut):
                field_string = field_string[len(self.string_for_cut):]
                event.change(self.field_for_cut, field_string)

            if self.string_from_start == 0 and field_string.endswith(self.string_for_cut):
                field_string = field_string[:-len(self.string_for_cut)]
                event.change(self.field_for_cut, field_string)

        self.send_message(event)
        self.acknowledge_message()


BOT = CutFromStringExpertBot
