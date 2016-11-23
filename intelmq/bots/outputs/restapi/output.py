# -*- coding: utf-8 -*-

import requests

from intelmq.lib.bot import Bot


class RestAPIOutputBot(Bot):

    def init(self):
        self.session = requests.Session()
        if self.parameters.auth_token_name and self.parameters.auth_token:
            self.session.headers.update(
                {self.parameters.auth_token_name: self.parameters.auth_token})
        self.session.headers.update({"content-type":
                                     "application/json; charset=utf-8"})
        self.session.keep_alive = False

    def process(self):
        event = self.receive_message()
        if self.parameters.use_json:
            kwargs = {'json': event.to_dict(hierarchical=self.parameters.hierarchical_output)}
        else:
            kwargs = {'data': event.to_dict(hierarchical=self.parameters.hierarchical_output)}

        try:
            r = self.session.post(self.parameters.host, **kwargs)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            if r:
                self.logger.error('Response code: {1}\nHeaders: '
                                  '{2}\nResponse body: {3}'
                                  ''.format(r, r.headers,
                                            r.text))
            else:
                self.logger.error(repr(e))
        self.acknowledge_message()


BOT = RestAPIOutputBot
