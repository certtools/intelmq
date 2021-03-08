"""
HTTP Status Expert Bot

SPDX-FileCopyrightText: 2021 Birger Schacht <schacht@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from typing import List

from intelmq.lib.bot import Bot
from intelmq.lib.utils import create_request_session


class HttpStatusExpertBot(Bot):
    """
    Fetch the HTTP Status for a given URL

    Parameters
    ----------
    field: str
        The name of the field containing the URL to be checked (defaults to 'source.url').
    success_status_codes: List
        A list of success status codes. If this parameter is omitted or the list is empty,
        successful status codes are the ones between 200 and 400.
    overwrite:
        Specifies if an existing 'status' value should be overwritten.
    """
    field: str = "source.url"  # The field containing the URL
    success_status_codes: List[int] = []  # A list of status codes for success
    overwrite: bool = True

    def process(self):
        event = self.receive_message()

        if self.field in event:
            self.set_request_parameters()
            session = create_request_session(self)

            try:
                response = session.get(event[self.field])
                # If success_status_codes are configured, we use those
                # to check the success of the request, otherwise we
                # rely on the boolean value of the response
                if (self.success_status_codes and response.status_code in self.success_status_codes) or (response):
                    event.add('status', "online", overwrite=self.overwrite)
                else:
                    event.add('status', 'offline', overwrite=self.overwrite)
                    event.add('extra.reason', response.reason)
            except Exception as exc:
                event.add('status', 'offline', overwrite=self.overwrite)
                event.add('extra.reason', str(exc))
        else:
            self.logger.debug('Field %s was not part of the message.', self.field)

        self.send_message(event)
        self.acknowledge_message()


BOT = HttpStatusExpertBot
