# SPDX-FileCopyrightText: 2022 gutsohnCERT
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import rfc3986.exceptions
from rfc3986 import uri_reference, validators
from intelmq.lib.bot import ExpertBot


class URIExpertBot(ExpertBot):
    """Parse the URI"""
    overwrite = False

    def process(self):
        event = self.receive_message()
        uri_validator = validators.Validator().require_presence_of('scheme')

        for key in ["source.", "destination."]:
            key_url = "{}{}".format(key, "url")
            key_ip = "{}{}".format(key, "ip")
            key_fqdn = "{}{}".format(key, "fqdn")
            key_scheme = "{}{}".format(key, "scheme")
            key_path = "{}{}".format(key, "path")
            key_userinfo = "{}{}".format(key, "userinfo")
            key_port = "{}{}".format(key, "port")
            key_query = "{}{}".format(key, "query")

            if key_url not in event:
                continue
            if key_fqdn in event and not self.overwrite:
                continue

            try:
                uri_validator.validate(uri_reference(event.get(key_url)))
            except rfc3986.exceptions.MissingComponentError:
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
