# SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
GITHUB API Collector bot
"""
import base64
from requests import exceptions

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin

static_params = {
    'headers': {
        'Accept': 'application/vnd.github.v3.text-match+json'
    }
}


class GithubAPICollectorBot(CollectorBot, HttpMixin):
    basic_auth_username = None
    basic_auth_password = None

    def init(self):
        self.__user_headers = static_params['headers']
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            self.__user_headers.update(self.__produce_auth_header(self.basic_auth_username, self.basic_auth_password))
        else:
            self.logger.warning('Using unauthenticated API access, means the request limit is at 60 per hour.')

    def process(self):
        self.process_request()

    def process_request(self):
        """
        Requests github API with specific path and functionality
        """
        raise NotImplementedError

    def github_api(self, api_path: str, **kwargs) -> dict:
        try:
            response = self.http_get(api_path, headers=self.__user_headers, params=kwargs)
            if response.status_code == 401:
                # bad credentials
                raise ValueError(response.json()['message'])
            else:
                return response.json()
        except exceptions.RequestException:
            raise ValueError(f"Unknown repository {api_path!r}.")

    @staticmethod
    def __produce_auth_header(username: str, password: str) -> dict:
        encoded_auth_bytes = base64.b64encode(bytes(f'{username}:{password}', encoding='utf-8'))
        return {
            'Authorization': 'Basic {}'.format(encoded_auth_bytes.decode('utf-8'))
        }
