# SPDX-FileCopyrightText: 2015 robcza
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import warnings

from urllib.parse import urlparse
from typing import Optional, List

from intelmq.lib.bot import ExpertBot

DEPRECATION_WARNING = "This bot is deprecated and will be removed in version 4.0. Use 'URL Expert' bot instead."


class Url2fqdnExpertBot(ExpertBot):
    """Parse the FQDN from the URL"""
    overwrite = False

    def init(self):
        warnings.warn(DEPRECATION_WARNING, DeprecationWarning)

    @staticmethod
    def check(parameters: dict) -> Optional[List[List[str]]]:
        return [["warning", DEPRECATION_WARNING]]

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            key_url = key + "url"
            key_fqdn = key + "fqdn"
            key_ip = key + "ip"
            if key_url not in event:
                continue
            if key_fqdn in event and not self.overwrite:
                continue

            hostname = urlparse(event.get(key_url)).hostname
            if not event.add(key_fqdn, hostname, overwrite=self.overwrite,
                             raise_failure=False):
                event.add(key_ip, hostname, overwrite=self.overwrite,
                          raise_failure=False)

        self.send_message(event)
        self.acknowledge_message()


BOT = Url2fqdnExpertBot
