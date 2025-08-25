# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology, Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from ipaddress import ip_network
from random import choice
from json import load as json_load

from intelmq.lib.bot import ExpertBot
from intelmq import VAR_STATE_PATH
from intelmq.lib.message import Event


class FakeExpertBot(ExpertBot):
    """Add fake data"""

    overwrite: bool = False
    database: str = f'{VAR_STATE_PATH}fake/data.json'  # TODO: should be pathlib.Path

    def init(self):
        with open(self.database) as database:
            database = json_load(database)
        self.ip_networks = database.get('ip_network', [])
        self.event_fields = database.get('event_fields', {})

    def process(self):
        event = self.receive_message()
        if self.ip_networks:
            network = choice(self.ip_networks)

            updated = False
            try:
                updated = event.add('source.ip', ip_network(network)[1], overwrite=self.overwrite)
            except IndexError:
                updated = event.add('source.ip', ip_network(network)[0], overwrite=self.overwrite)
            # For consistency, only set the network if the source.ip was set or overwritten, but then always overwrite it
            if updated:
                event.add('source.network', network, overwrite=True)

        for fieldname, field in self.event_fields.items():
            if field['mode'] == 'random_single_value':
                event.add(fieldname, choice(field['values']), overwrite=self.overwrite)
            else:
                raise ValueError(f"Mode {field['mode']} not supported in field {fieldname}.")

        self.send_message(event)
        self.acknowledge_message()

    def check(parameters: dict):
        try:
            with open(parameters['database']) as database:
                database = json_load(database)
        except Exception as exc:
            return [['error', f"Could not load database: {exc}"]]
        errors = []
        if not isinstance(database.get('ip_network', []), list):
            errors.append(['error', 'ip_network is not of type list'])
        if not isinstance(database.get('event_fields', {}), dict):
            errors.append(['error', 'event_fields is not of type dict'])
        else:
            test_event = Event()
            for fieldname, field in database.get('event_fields', {}).items():
                fieldname_check = test_event._Message__is_valid_key(fieldname)
                if not fieldname_check[0]:
                    errors.append(['error', f"Field name {fieldname} is not valid: {fieldname_check[1]}."])
                mode = field.get('mode')
                if mode not in ('random_single_value', ):
                    errors.append(['error', f"Mode {mode} not supported in field {fieldname}."])
                if 'values' not in field:
                    errors.append(['error', f"No values defined in field {fieldname}."])
                elif not isinstance(field['values'], list):
                    errors.append(['error', f"Values is not a list in field {fieldname}."])
        return errors if errors else None


BOT = FakeExpertBot
