"""
HTTP Content Expert Bot

SPDX-FileCopyrightText: 2021 Birger Schacht <schacht@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from typing import List

from intelmq.lib.bot import Bot
from intelmq.lib.utils import create_request_session


class HttpContentExpertBot(Bot):
    """
    Test if a given string is part of the content for a given URL

    Parameters
    ----------
    field: str
        The name of the field containing the URL to be checked (defaults to 'source.url').
    needle: str
        The string that the content available on URL is checked for.
    overwrite:
        Specifies if an existing 'status' value should be overwritten.
    """
    field: str = "source.url"  # The field containing the URL
    needle: str = None
    overwrite: bool = True
    __session = None

    def init(self):
        self.set_request_parameters()
        self.__session = create_request_session(self)

    def process(self):
        event = self.receive_message()

        if self.field in event and self.needle is not None:
            try:
                response = self.__session.get(event[self.field])
                if response:
                    if self.needle in response.text:
                        event.add('status', 'online', overwrite=self.overwrite)
                    else:
                        event.add('status', 'offline', overwrite=self.overwrite)
                        event.add('extra.reason', f'Text {self.needle} not found in response from {event[self.field]}')
                else:
                    event.add('status', 'offline', overwrite=self.overwrite)
                    event.add('extra.reason', response.reason)
            except Exception as exc:
                event.add('status', 'offline', overwrite=self.overwrite)
                event.add('extra.reason', str(exc))
        else:
            self.logger.debug('Field %s was not part of the message or search string is not set.', self.field)

        self.send_message(event)
        self.acknowledge_message()


BOT = HttpContentExpertBot
