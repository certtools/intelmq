"""
SPDX-FileCopyrightText: 2021 Sebastian Wagner <wagner@cert.at>
SPDX-FileCopyrightText: 2025 CERT.at GmbH <https://cert.at/>
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

import requests

from intelmq.lib.bot import ExpertBot
from intelmq.lib.utils import create_request_session, parse_relative


class TuencyExpertBot(ExpertBot):
    url: str  # Path to the tuency instance
    authentication_token: str
    overwrite: bool = True

    notify_field = "extra.notify"
    ttl_field = "extra.ttl"
    constituency_field = "extra.constituency"

    query_ip = True
    query_domain = True

    # Allows setting custom TTL for suspended sending
    ttl_on_suspended = None

    # Non-default values require Tuency v2.6+
    query_classification_identifier = False
    query_feed_code = False

    def init(self):
        self.set_request_parameters()
        self.session = create_request_session(self)
        self.session.headers["Authorization"] = f"Bearer {self.authentication_token}"
        self.url = f"{self.url}intelmq/lookup"

        if not self.query_ip and not self.query_domain:
            self.logger.warning(
                "Neither query_ip nor query_domain is set. "
                "Bot won't do anything, please ensure it's intended."
            )

    @staticmethod
    def check(parameters):
        results = []
        if not parameters.get("query_ip", True) and not parameters.get(
            "query_domain", True
        ):
            results.append(
                [
                    "warning",
                    "Neither query_ip nor query_domain is set. "
                    "Bot won't do anything, please ensure it's intended.",
                ]
            )

        return results or None

    def process(self):
        event = self.receive_message()

        try:
            params = {
                "classification_taxonomy": event["classification.taxonomy"],
                "classification_type": event["classification.type"],
                "feed_provider": event["feed.provider"],
                "feed_status": "production",
            }
            if self.query_feed_code:
                params["feed_code"] = event["feed.code"]
            else:
                params["feed_name"] = event["feed.name"]

            if self.query_classification_identifier:
                params["classification_identifier"] = event["classification.identifier"]
        except KeyError as exc:
            self.logger.debug("Skipping event because of missing field: %s.", exc)
            self.send_message(event)
            self.acknowledge_message()
            return

        if self.query_ip:
            try:
                params["ip"] = event["source.ip"]
            except KeyError:
                pass

        if self.query_domain:
            try:
                params["domain"] = event["source.fqdn"]
            except KeyError:
                pass

        if "ip" not in params and "domain" not in params:
            # Nothing to query - skip
            self.send_message(event)
            self.acknowledge_message()
            return

        response = self.session.get(self.url, params=params)
        self.logger.debug("Received response %r.", response.text)
        try:
            response = response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.error("Cannot proceed response: '%s'.", response.text)
            raise  # let IntelMQ handle issues

        destinations = (
            response.get("ip", {"destinations": []})["destinations"]
            + response.get("domain", {"destinations": []})["destinations"]
        )

        if response.get("suppress", False):
            event.add(self.notify_field, False, overwrite=self.overwrite)
            if self.ttl_on_suspended:
                event.add(
                    self.ttl_field,
                    self.ttl_on_suspended,
                    overwrite=self.overwrite,
                )
        else:
            if not destinations:
                # empty response
                self.send_message(event)
                self.acknowledge_message()
                return

            if "interval" in response:
                if response["interval"]["unit"] == "immediate":
                    event.add(self.ttl_field, 0, overwrite=self.overwrite)
                else:
                    event.add(
                        self.ttl_field,
                        (
                            parse_relative(
                                f"{response['interval']['length']} {response['interval']['unit']}"
                            )
                            * 60
                        ),
                        overwrite=self.overwrite,
                    )

        contacts = []
        for destination in destinations:
            contacts.extend(contact["email"] for contact in destination["contacts"])
        event.add("source.abuse_contact", ",".join(contacts), overwrite=self.overwrite)

        if self.constituency_field and (
            constituencies := response.get("constituencies", [])
        ):
            event.add(
                self.constituency_field,
                ",".join(constituencies),
                overwrite=self.overwrite,
            )

        self.send_message(event)
        self.acknowledge_message()


BOT = TuencyExpertBot
