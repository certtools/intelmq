# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from ipaddress import ip_network
from random import choice
from json import load as json_load

from intelmq.lib.bot import ExpertBot


class FakeExpertBot(ExpertBot):
    """Add fake data"""

    overwrite: bool = False
    database: str = None  # TODO: should be pathlib.Path

    def init(self):
        with open(self.database) as database:
            self.networks = json_load(database)['ip_network']

    def process(self):
        event = self.receive_message()
        network = choice(self.networks)

        updated = False
        try:
            updated = event.add('source.ip', ip_network(network)[1], overwrite=self.overwrite)
        except IndexError:
            updated = event.add('source.ip', ip_network(network)[0], overwrite=self.overwrite)
        # For consistency, only set the network if the source.ip was set or overwritten, but then always overwrite it
        if updated:
            event.add('source.network', network, overwrite=True)

        self.send_message(event)
        self.acknowledge_message()

    def check(parameters: dict):
        try:
            with open(parameters['database']) as database:
                json_load(database)['ip_network']
        except Exception as exc:
            return [['error', exc]]


BOT = FakeExpertBot
