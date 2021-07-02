"""
© 2021 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0-or-later

https://gitlab.com/intevation/tuency/tuency/-/blob/master/backend/docs/IntelMQ-API.md

Example query:
> curl -s -H "Authorization: Bearer XXX"\
    'https://tuency-demo1.example.com/intelmq/lookup?classification_taxonomy=availability&classification_type=backdoor\
     &feed_provider=Team+Cymru&feed_name=FTP&feed_status=production&ip=123.123.123.23'
     same for domain=
     a query can contain both ip address and domain

Example response:
{"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@example.com"}]}]},"suppress":true,"interval":{"unit":"days","length":1}}
{"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@example.vom"}]}]},"domain":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"abuse@example.at"}]}]},"suppress":true,"interval":{"unit":"immediate","length":1}}
"""

from intelmq.lib.bot import Bot
from intelmq.lib.utils import create_request_session, parse_relative


class TuencyExpertBot(Bot):
    url: str  # Path to the tuency instance
    authentication_token: str
    overwrite: bool = True

    def init(self):
        self.set_request_parameters()
        self.session = create_request_session(self)
        self.session.headers["Authorization"] = f"Bearer {self.authentication_token}"
        self.url = f"{self.url}intelmq/lookup"

    def process(self):
        event = self.receive_message()
        if not ("source.ip" in event or "source.fqdn" in event):
            self.send_message(event)
            self.acknowledge_message()
            return

        try:
            params = {
                "classification_taxonomy": event["classification.taxonomy"],
                "classification_type": event["classification.type"],
                "feed_provider": event["feed.provider"],
                "feed_name": event["feed.name"],
                "feed_status": "production",
            }
        except KeyError as exc:
            self.logger.debug('Skipping event because of missing field: %s.', exc)
            self.send_message(event)
            self.acknowledge_message()
            return
        try:
            params["ip"] = event["source.ip"]
        except KeyError:
            pass
        try:
            params["domain"] = event["source.fqdn"]
        except KeyError:
            pass

        response = self.session.get(self.url, params=params).json()
        self.logger.debug('Received response %r.', response)

        if response.get("suppress", False):
            event["extra.notify"] = False
        else:
            if 'interval' not in response:
                # empty response
                self.send_message(event)
                self.acknowledge_message()
                return
            elif response['interval']['unit'] == 'immediate':
                event["extra.ttl"] = 0
            else:
                event["extra.ttl"] = parse_relative(f"{response['interval']['length']} {response['interval']['unit']}") * 60
        contacts = []
        for destination in response.get('ip', {'destinations': []})['destinations'] + response.get('domain', {'destinations': []})['destinations']:
            contacts.extend(contact['email'] for contact in destination["contacts"])
        event.add('source.abuse_contact', ','.join(contacts), overwrite=self.overwrite)

        self.send_message(event)
        self.acknowledge_message()


BOT = TuencyExpertBot
