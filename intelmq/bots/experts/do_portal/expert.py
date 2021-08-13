# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
As the frontend reverse-proxies the (backend) API
a "502 Bad Gateway" status code is treated the same as a timeout,
i.e. will be retried instead of a fail.
"""
try:
    import requests
except ImportError:
    requests = None

import intelmq.lib.utils as utils
from intelmq.lib.bot import Bot


class DoPortalExpertBot(Bot):
    """Retrieve abuse contact information for the source IP address from a do-portal instance"""
    mode: str = "append"
    portal_api_key: str = None
    portal_url: str = None

    def init(self):
        if requests is None:
            raise ValueError("Library 'requests' could not be loaded. Please install it.")

        self.set_request_parameters()

        self.url = self.portal_url + '/api/1.0/ripe/contact?cidr=%s'
        self.http_header.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "API-Authorization": self.portal_api_key
        })

        self.session = utils.create_request_session(self)
        retries = requests.urllib3.Retry.from_int(self.http_timeout_max_tries)
        retries.status_forcelist = [502]
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def process(self):
        event = self.receive_message()
        if "source.ip" not in event:
            self.send_message(event)
            self.acknowledge_message()
            return

        req = self.session.get(self.url % event['source.ip'])

        if req.status_code == 404 and req.json()['message'].startswith("('no such cidr'"):
            result = []
        else:
            req.raise_for_status()
            result = req.json()['abusecs']

        if self.mode == 'append':
            existing = event.get("source.abuse_contact", '').split(',')
            combined = ','.join(existing + result).strip(',')
            event.add("source.abuse_contact", combined, overwrite=True)
        else:
            event.add("source.abuse_contact", ','.join(result), overwrite=True)

        self.send_message(event)
        self.acknowledge_message()


BOT = DoPortalExpertBot
