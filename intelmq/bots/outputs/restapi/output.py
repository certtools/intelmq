# SPDX-FileCopyrightText: 2015 robcza
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
from typing import Iterable

try:
    import requests
except ImportError:
    requests = None

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError


class RestAPIOutputBot(Bot):
    """Send events to a REST API listener through HTTP POST"""
    auth_token_name: str = None
    auth_token: str = None
    auth_type = None
    hierarchical_output: bool = False
    host: str = None
    use_json: bool = True

    _auth: Iterable[str] = None

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()

        if self.auth_token_name and self.auth_token:
            if self.auth_type == 'http_header':
                self.http_header.update(
                    {self.auth_token_name: self.auth_token})
            elif self.auth_type == 'http_basic_auth':
                self.auth = self.auth_token_name, self.auth_token
        self.http_header.update({"Content-Type":
                                 "application/json; charset=utf-8"})

        self.session = utils.create_request_session(self)
        self.session.keep_alive = False

    def process(self):
        event = self.receive_message()
        if self.use_json:
            kwargs = {'json': event.to_dict(hierarchical=self.hierarchical_output)}
        else:
            kwargs = {'data': event.to_dict(hierarchical=self.hierarchical_output)}

        timeoutretries = 0
        req = None
        while timeoutretries < self.http_timeout_max_tries and req is None:
            try:
                req = self.session.post(self.host,
                                        timeout=self.http_timeout_sec,
                                        **kwargs)
            except requests.exceptions.Timeout:
                timeoutretries += 1

        if req is None and timeoutretries >= self.http_timeout_max_tries:
            raise ValueError("Request timed out %i times in a row."
                             "" % timeoutretries)

        if not req.ok:
            self.logger.debug("Error during message sending, response body: %r.",
                              req.text)
        req.raise_for_status()
        self.logger.debug('Sent message.')
        self.acknowledge_message()


BOT = RestAPIOutputBot
