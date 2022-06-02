# SPDX-FileCopyrightText: 2022 gutsohnCERT
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from rfc3986 import uri_reference, validators
from intelmq.lib.bot import ExpertBot


class URIExpertBot(ExpertBot):
    """Parse the URI"""
    overwrite = False

    def process(self):
        event = self.receive_message()
        uri_validator = validators.Validator().require_presence_of('scheme', 'path')

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

            uri_validator.validate(uri_reference(event.get(key_url)))
            scheme = uri_reference(event.get(key_url)).scheme
            path = uri_reference(event.get(key_url)).path
            userinfo = uri_reference(event.get(key_url)).userinfo
            host = uri_reference(event.get(key_url)).host
            port = uri_reference(event.get(key_url)).port
            query = uri_reference(event.get(key_url)).query

            if not event.add(key_fqdn, host, overwrite=self.overwrite,
                             raise_failure=False):
                event.add(key_ip, host, overwrite=self.overwrite,
                          raise_failure=False)

            event.add(key_scheme, scheme, overwrite=self.overwrite, raise_failure=False)
            event.add(key_path, path, overwrite=self.overwrite, raise_failure=False)
            event.add(key_userinfo, userinfo, overwrite=self.overwrite, raise_failure=False)
            event.add(key_port, port, overwrite=self.overwrite, raise_failure=False)
            event.add(key_query, query, overwrite=self.overwrite, raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = URIExpertBot
