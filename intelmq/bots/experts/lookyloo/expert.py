# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pylookyloo
except ImportError:
    pylookyloo = None


class LookyLooExpertBot(Bot):
    """ LookyLoo expert bot for automated website screenshots """
    instance_url: str = "http://localhost:5100/"

    __instance: None

    def init(self):
        if pylookyloo is None:
            raise MissingDependencyError("pylookyloo", version=">=0.6")

        self.__instance = pylookyloo.Lookyloo(self.instance_url)

    def process(self):
        event = self.receive_message()
        if 'source.url' in event:
            url = self.__instance.enqueue(url=event.get('source.url'), user_agent=self.http_user_agent)
            event.add('screenshot_url', url)
        self.send_message(event)
        self.acknowledge_message()


BOT = LookyLooExpertBot
