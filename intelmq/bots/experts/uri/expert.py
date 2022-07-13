# SPDX-FileCopyrightText: 2022 CERT.at GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from intelmq.lib.bot import ExpertBot
try:
    from rfc3986 import uri_reference, validators, exceptions
except ImportError:
    rfc3986 = None
from intelmq.lib.exceptions import MissingDependencyError


class URIExpertBot(ExpertBot):
    """Parse the URI"""
    overwrite = False
    _uri_validator = None

    def init(self):
        if rfc3986 is None:
            raise MissingDependencyError("rfc3986", version=">=1.5")
        self._uri_validator = validators.Validator().require_presence_of('scheme')

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:
            key_url = f"{key}url"
            key_ip = f"{key}ip"
            key_fqdn = f"{key}fqdn"
            key_scheme = f"{key}scheme"
            key_path = f"{key}path"
            key_userinfo = f"{key}userinfo"
            key_port = f"{key}port"
            key_query = f"{key}query"

            if key_url not in event:
                continue
            if key_fqdn in event and not self.overwrite:
                continue

            try:
                self._uri_validator.validate(uri_reference(event.get(key_url)))
            except exceptions.MissingComponentError:
                raise ValueError('Invalid URI: The format of the URI could not be determined.')

            uri = uri_reference(event.get(key_url))
            uri_information = {
                key_scheme: uri.scheme,
                key_path: uri.path,
                key_userinfo: uri.userinfo,
                key_port: uri.port,
                key_query: uri.query
            }

            if not event.add(key_fqdn, uri.host, overwrite=self.overwrite,
                             raise_failure=False):
                event.add(key_ip, uri.host, overwrite=self.overwrite, raise_failure=False)

            for uri_key, uri_value in uri_information.items():
                if uri_value is not None:
                    event.add(uri_key, uri_value, overwrite=self.overwrite, raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = URIExpertBot
