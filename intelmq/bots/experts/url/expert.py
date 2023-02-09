# SPDX-FileCopyrightText: 2023 Filip Pokorný
#
# SPDX-License-Identifier: AGPL-3.0-or-later
from typing import Optional, List
from urllib.parse import urlparse

from intelmq.lib.bot import ExpertBot
from intelmq.lib.harmonization import IPAddress, FQDN

URLSCHEMES = {
    "ftp": {
        "default_port": 21,
        "transport_protocol": "tcp"
    },
    "http": {
        "default_port": 80,
        "transport_protocol": "tcp"
    },
    "https": {
        "default_port": 443,
        "application_protocol": "http"
    },
    "sftp": {
        "default_port": 22,
        "transport_protocol": "tcp"
    },
    "ssh": {
        "default_port": 22,
        "transport_protocol": "tcp"
    },
    "tftp": {
        "default_port": 69,
        "transport_protocol": "udp"
    },
    "ws": {
        "default_port": 80,
        "transport_protocol": "tcp"
    },
    "wss": {
        "default_port": 443,
        "transport_protocol": "tcp"
    },
}


class URLExpertBot(ExpertBot):
    """
    Extract additional information for the URL.

    Possibly fills the following fields:
    "source.fqdn",
    "source.ip",
    "source.port",
    "source.urlpath",
    "source.account",
    "destination.fqdn",
    "destination.ip",
    "destination.port",
    "destination.urlpath",
    "destination.account",
    "protocol.application",
    "protocol.transport"

    Fields "protocol.application" and "protocol.transport" are preferred from source.url.

    """

    overwrite: bool = False
    skip_fields: Optional[List[str]] = None

    def init(self):
        if self.skip_fields is None:
            self.skip_fields = []

    def process(self):
        event = self.receive_message()
        protocols_added: int = 0

        for base in "source", "destination":

            url_key: str = f"{base}.url"

            if not event.get(url_key):
                continue

            fqdn_key: str = f"{base}.fqdn"
            ip_key: str = f"{base}.ip"
            port_key: str = f"{base}.port"
            urlpath_key: str = f"{base}.urlpath"
            account_key: str = f"{base}.account"

            url = urlparse(event.get(url_key))
            overwrite_protocols: bool = not bool(protocols_added)

            # IP
            if url.hostname and ip_key not in self.skip_fields and IPAddress.is_valid(url.hostname, sanitize=True):
                event.add(key=ip_key, value=url.hostname, overwrite=self.overwrite)

            # FQDN
            elif url.hostname and fqdn_key not in self.skip_fields and FQDN.is_valid(url.hostname, sanitize=True):
                event.add(key=fqdn_key, value=url.hostname, overwrite=self.overwrite)

            # PORT
            if url.port and port_key not in self.skip_fields:
                event.add(key=port_key, value=str(url.port), overwrite=self.overwrite)

            # PORT
            elif port_key not in self.skip_fields and url.scheme in URLSCHEMES:
                event.add(key=port_key, value=str(URLSCHEMES[url.scheme]["default_port"]), overwrite=self.overwrite)

            # URLPATH
            if url.path and urlpath_key not in self.skip_fields:
                event.add(key=urlpath_key, value=url.path, overwrite=self.overwrite)

            # ACCOUNT
            if url.username and account_key not in self.skip_fields:
                event.add(key=account_key, value=url.username, overwrite=self.overwrite, raise_failure=False)

            # PROTOCOL.APPLICATION
            if overwrite_protocols and url.scheme and "protocol.application" not in self.skip_fields:
                value = URLSCHEMES[url.scheme].get("application_protocol", url.scheme) if URLSCHEMES.get(url.scheme) else url.scheme
                event.add(key="protocol.application", value=value, overwrite=self.overwrite)
                protocols_added += 1

            # PROTOCOL.TRANSPORT
            if overwrite_protocols and url.scheme and "protocol.transport" not in self.skip_fields and url.scheme in URLSCHEMES and URLSCHEMES[url.scheme].get("transport_protocol"):
                event.add(key="protocol.transport", value=URLSCHEMES[url.scheme]["transport_protocol"], overwrite=self.overwrite)
                protocols_added += 1

        self.send_message(event)
        self.acknowledge_message()


BOT = URLExpertBot
