# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Reducer bot
"""

from intelmq.lib.bot import Bot
from intelmq.lib.message import Event


class FieldReducerExpertBot(Bot):
    """Remove fields from events"""
    type = None
    keys = None

    def init(self):
        if self.type not in ['whitelist', 'blacklist']:
            raise ValueError("Invalid configuration: value of 'type' not allowed.")
        if isinstance(self.keys, str):
            self.keys = [key.strip() for key in self.keys.split(',')]

    def process(self):
        event = self.receive_message()

        if self.type == 'whitelist':
            new_event = Event()
            for key in self.keys:
                if key in event:
                    new_event.add(key, event[key], sanitize=False)
            event = new_event
        else:
            for key in self.keys:
                if key in event:
                    del event[key]

        self.send_message(event)
        self.acknowledge_message()


BOT = FieldReducerExpertBot
