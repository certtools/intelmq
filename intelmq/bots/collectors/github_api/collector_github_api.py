# -*- coding: utf-8 -*-
"""
GITHUB API Collector bot
"""
import base64

from intelmq.lib.bot import CollectorBot

try:
    import requests
except ImportError:
    requests = None

static_params = {
    'headers': {
        'Accept': 'application/vnd.github.v3.text-match+json'
    }
}


class GithubAPICollectorBot(CollectorBot):

    def init(self):
        if requests is None:
            raise ValueError('Could not import requests. Please install it.')

        self.__user_headers = static_params['headers']
        if hasattr(self.parameters, 'basic_auth_username') and hasattr(self.parameters, 'basic_auth_password'):
            self.__user_headers.update(self.__produce_auth_header(getattr(self.parameters, 'basic_auth_username'),
                                                                  getattr(self.parameters, 'basic_auth_password')))
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
            response = requests.get("{}".format(api_path), params=kwargs, headers=self.__user_headers)
            if response.status_code == 401:
                # bad credentials
                raise ValueError(response.json()['message'])
            else:
                return response.json()
        except requests.RequestException:
            raise ValueError("Unknown repository {!r}.".format(api_path))

    @staticmethod
    def __produce_auth_header(username: str, password: str) -> dict:
        encoded_auth_bytes = base64.b64encode(bytes('{}:{}'.format(username, password), encoding='utf-8'))
        return {
            'Authorization': 'Basic {}'.format(encoded_auth_bytes.decode('utf-8'))
        }
