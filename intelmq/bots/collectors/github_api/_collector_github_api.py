# SPDX-FileCopyrightText: 2022 Sebastian Waldbauer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
GITHUB API Collector bot
"""
from typing import Optional

import requests
from intelmq.lib.bot import CollectorBot

static_params = {
    'headers': {
        'Accept': 'application/vnd.github.v3.text-match+json'
    }
}


class GithubAPICollectorBot(CollectorBot):
    personal_access_token: Optional[str] = None

    def init(self):
        self.__user_headers = static_params['headers']
        if self.personal_access_token:
            self.__user_headers.update({'Authorization': self.personal_access_token})
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
            response = requests.get(f"{api_path}", params=kwargs, headers=self.__user_headers)
            if response.status_code == 401:
                # bad credentials
                raise ValueError(response.json()['message'])
            else:
                return response.json()
        except requests.RequestException:
            raise ValueError(f"Unknown repository {api_path!r}.")
