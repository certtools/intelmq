# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot


class BlackholeOutputBot(Bot):
    "Discard messages"

    def process(self):
        self.receive_message()
        self.acknowledge_message()


BOT = BlackholeOutputBot
