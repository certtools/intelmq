# -*- coding: utf-8 -*-
import sys

import requests

from intelmq.lib.bot import Bot


class RestAPI(Bot):

    def init(self):
        self.session = requests.Session()
        if self.parameters.auth_token_name and self.parameters.auth_token:
            self.session.headers.update(
                {self.parameters.auth_token_name: self.parameters.auth_token})
        self.session.headers.update({"content-type":
                                     "application/json; charset=utf-8"})

    def process(self):
        event = self.receive_message()
        jevent = event.to_json(hierarchical=self.parameters.hierarchical_output)

        try:
            r = self.session.post(self.parameters.host,
                                  jevent)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            if r:
                self.logger.error('Event: {0}\nResponse code: {1}\nHeaders: '
                                  '{2}\nResponse body: {3}'
                                  ''.format(event.to_json(), r, r.headers,
                                            r.text))
            else:
                self.logger.error(repr(e))
        self.acknowledge_message()


if __name__ == "__main__":
    bot = RestAPI(sys.argv[1])
    bot.start()
