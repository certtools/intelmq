# -*- coding: utf-8 -*-

try:
    import requests
except ImportError:
    requests = None

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError


class RestAPIOutputBot(Bot):

    def init(self):
        if requests is None:
            raise MissingDependencyError("requests")

        self.set_request_parameters()

        if self.parameters.auth_token_name and self.parameters.auth_token:
            if self.parameters.auth_type == 'http_header':
                self.http_header.update(
                    {self.parameters.auth_token_name: self.parameters.auth_token})
            elif self.parameters.auth_type == 'http_basic_auth':
                self.auth = self.parameters.auth_token_name, self.parameters.auth_token
        self.http_header.update({"Content-Type":
                                 "application/json; charset=utf-8"})

        self.session = utils.create_request_session(self)
        self.session.keep_alive = False

    def process(self):
        event = self.receive_message()
        if self.parameters.use_json:
            kwargs = {'json': event.to_dict(hierarchical=self.parameters.hierarchical_output)}
        else:
            kwargs = {'data': event.to_dict(hierarchical=self.parameters.hierarchical_output)}

        timeoutretries = 0
        req = None
        while timeoutretries < self.http_timeout_max_tries and req is None:
            try:
                req = self.session.post(self.parameters.host,
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
