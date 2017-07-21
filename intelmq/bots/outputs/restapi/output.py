# -*- coding: utf-8 -*-

import requests

from intelmq.lib.bot import Bot


class RestAPIOutputBot(Bot):

    def init(self):
        self.session = requests.Session()
        self.set_request_parameters()
        if self.parameters.auth_token_name and self.parameters.auth_token:
            if self.parameters.auth_type == 'http_header':
                self.session.headers.update(
                    {self.parameters.auth_token_name: self.parameters.auth_token})
            elif self.parameters.auth_type == 'http_basic_auth':
                self.session.auth = self.parameters.auth_token_name, self.parameters.auth_token
        self.session.headers.update({"content-type":
                                     "application/json; charset=utf-8"})
        self.session.keep_alive = False

    def process(self):
        event = self.receive_message()
        if self.parameters.use_json:
            kwargs = {'json': event.to_dict(hierarchical=self.parameters.hierarchical_output)}
        else:
            kwargs = {'data': event.to_dict(hierarchical=self.parameters.hierarchical_output)}

        r = self.session.post(self.parameters.host,
                              proxies=self.proxy,
                              headers=self.http_header,
                              verify=self.http_verify_cert,
                              cert=self.ssl_client_cert,
                              timeout=self.http_timeout_sec,
                              **kwargs)
        r.raise_for_status()
        self.logger.debug('Sent message.')
        self.acknowledge_message()


BOT = RestAPIOutputBot
