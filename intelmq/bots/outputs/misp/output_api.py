"""Connect to a MISP instance and add event as MISPObject if not there already.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Reiter <bernhard@intevation.de>

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - misp_tag_for_bot: str used to mark MISP events
  - significant_fields: list of intelmq field names

The significant field values will be searched for in MISP attribute values
and if all found in the same MISP event, no new one will be created.
If a new one will be created those will be the attributes where
correlation is enabled.
Example::

    "significant_fields": ["source.fqdn", "source.reverse_dns"]


Tested with pymisp v2.4.120 (which needs python v>=3.6).
"""
from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pymisp
except ImportError:
    pymisp = None


class MISPAPIOutputBot(OutputBot):
    is_multithreadable = False

    def init(self):
        if pymisp is None:
            raise MissingDependencyError('pymisp', version='>=2.4.120')

        self.logger.info('Significant fields are {}.'.format(
            self.parameters.significant_fields))

        self.logger.info('Connecting to MISP instance at {}.'.format(
            self.parameters.misp_url))
        self.misp = pymisp.api.PyMISP(self.parameters.misp_url,
                                      self.parameters.misp_key,
                                      self.parameters.http_verify_cert)

        self.misp.toggle_global_pythonify()

    def process(self):
        intelmq_event = self.receive_message().to_dict(jsondict_as_string=True)

        # search for existing events that have all values that are significant
        values_to_search_for = []
        for sig_field in self.parameters.significant_fields:
            if sig_field in intelmq_event:
                values_to_search_for.append(intelmq_event[sig_field])

        vquery = self.misp.build_complex_query(
            and_parameters=values_to_search_for
        )
        r = self.misp.search(tags=self.parameters.misp_tag_for_bot,
                             value=vquery)

        if len(r) > 0:
            msg = 'Found MISP events matching {}: {} not inserting.'
            self.logger.info(msg.format(vquery, [event.id for event in r]))
        else:
            # insert a new one
            new_misp_event = pymisp.MISPEvent()

            new_misp_event.info = 'Created by IntelMQ MISP API Output Bot.'
            new_misp_event.add_tag(self.parameters.misp_tag_for_bot)

            obj = new_misp_event.add_object(name='intelmq_event')
            for object_relation, value in intelmq_event.items():
                disable_correlation = True

                if object_relation in self.parameters.significant_fields:
                    disable_correlation = False
                try:
                    obj.add_attribute(object_relation,
                                      value=value,
                                      disable_correlation=disable_correlation)
                except pymisp.NewAttributeError:
                    msg = 'Ignoring "{}":"{}" as not in object template.'
                    self.logger.debug(msg.format(object_relation, value))

            misp_event = self.misp.add_event(new_misp_event)
            self.logger.info(
                'Inserted new MISP event with id: {}'.format(misp_event.id))

        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        required_parameters = ['misp_url', 'misp_key',
                               'misp_tag_for_bot', 'significant_fields']
        missing_parameters = []
        for para in required_parameters:
            if para not in parameters:
                missing_parameters.append(para)

        if len(missing_parameters) > 0:
            return [["error",
                     "Parameters missing: " + str(missing_parameters)]]


BOT = MISPAPIOutputBot
