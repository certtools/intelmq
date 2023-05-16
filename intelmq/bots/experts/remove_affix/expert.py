"""
Remove Affix

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from intelmq.lib.bot import ExpertBot


class RemoveAffixExpertBot(ExpertBot):
    remove_prefix: bool = True  # True - from start, False - from end
    affix: str = 'www.'
    field: str = 'source.fqdn'

    def process(self):
        event = self.receive_message()

        if self.field in event:
            if self.remove_prefix:
                event.change(self.field, self.removeprefix(event[self.field], self.affix))
            else:
                event.change(self.field, self.removesuffix(event[self.field], self.affix))

        self.send_message(event)
        self.acknowledge_message()

    def removeprefix(self, field: str, prefix: str) -> str:
        if field.startswith(prefix):
            return field[len(prefix):]
        else:
            return field[:]

    def removesuffix(self, field: str, suffix: str) -> str:
        if suffix and field.endswith(suffix):
            return field[:-len(suffix)]
        else:
            return field[:]


BOT = RemoveAffixExpertBot
