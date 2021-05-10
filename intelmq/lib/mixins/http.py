""" HttpMixin for IntelMQ

SPDX-FileCopyrightText: 2021 Birger Schacht
SPDX-License-Identifier: AGPL-3.0-or-later

Based on `create_request_session` in intelmq.lib.utils and
`set_request_parameters` in intelmq.lib.bot.Bot
"""

from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None


class TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    """
    A requests-HTTP Adapter which can set the timeout generally.
    """

    def __init__(self, *args, timeout=None, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super().send(*args, **kwargs)


class HttpMixin:
    """
    Setup a request session
    """
    __session: requests.Session = None
    __auth = None
    __proxy = {}

    ssl_client_cert = None  # TODO: path?
    http_header: dict = {}
    http_user_agent: str = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    http_verify_cert: bool = True
    http_proxy = None
    https_proxy = None
    http_timeout_max_tries: int = 3
    http_timeout_sec: int = 30
    http_username = None
    http_password = None

    def __init__(self, **kwargs):
        self.logger.debug("Running HTTP Mixin initialization.")
        self.http_header = {}
        super().__init__()

    def setup(self):
        self.logger.debug("Setting up HTTP Mixin.")
        if requests is None:
            raise MissingDependencyError("requests")

        self.__session = requests.Session()

        # tls settings
        self.__session.verify = self.http_verify_cert
        # tls certificate settings
        if self.ssl_client_cert is not None:
            self.__session.cert = self.ssl_client_cert
        # auth settings
        if self.http_username is not None:
            self.__auth = (self.http_username, self.http_password)
        self.__session.auth = self.__auth
        # headers settings
        if self.http_header is not None:
            self.__session.headers.update(self.http_header)
        elif self.http_user_agent is not None:
            self.__session.headers.update({"User-Agent": self.http_user_agent})

        # proxy settings
        if self.http_proxy is not None and self.https_proxy is not None:
            self.__proxy = {
                'http': self.http_proxy,
                'https': self.https_proxy
            }
        elif self.http_proxy or self.https_proxy:
            self.logger.warning('Only %s_proxy seems to be set.'
                                'Both http and https proxies must be set.',
                                'http' if self.http_proxy else 'https')
        self.__session.proxies = self.__proxy

        # timeout settings
        if self.http_timeout_max_tries is not None:
            max_retries = self.http_timeout_max_tries - 1

        if self.http_timeout_sec is not None:
            timeout = self.http_timeout_sec

        adapter = TimeoutHTTPAdapter(max_retries=max_retries, timeout=timeout)
        self.__session.mount('http://', adapter)
        self.__session.mount('https://', adapter)

    def http_get(self, url: str, **kwargs) -> requests.Response:
        self.setup()
        return self.__session.get(url, **kwargs)

    def http_session(self) -> requests.Session:
        self.setup()
        return self.__session
