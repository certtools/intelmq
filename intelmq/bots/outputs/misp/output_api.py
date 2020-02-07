"""Connect to a MISP instance and add event as MISPObject if not there already.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Reiter <bernhard@intevation.de>

Parameters:
  - add_feed_provider_as_tag: bool (use true when in doubt)
  - misp_additional_correlation_fields: list of fields for which
        the correlation flags will be enabled (in addition to those which are
        in significant_fields)
  - misp_additional_tags: list of tags to set not be searched for
        when looking for duplicates
  - misp_key: API key for accessing MISP
  - misp_tag_for_bot: str used to mark MISP events
  - misp_to_ids_fields: list of fields for which the to_ids flags will be set
  - misp_url: URL of the MISP server
  - significant_fields: list of intelmq field names

The significant field values will be searched for in all MISP attribute values
and if all values are found in the same MISP event, no new MISP event
will be created.

If a new MISP event is inserted the significant_fields will be the attributes
where correlation is enabled. (The reason is a technical limitation of the
search functionality exposed by the MISP/pymisp 2.4.120 API.)

Example (of some parameters in JSON)::

    "add_feed_provider_as_tag": true,
    "misp_additional_correlation_fields": ["source.asn"],
    "misp_additional_tags": ["OSINT", "osint:certainty==\"90\""],
    "misp_to_ids_fields": ["source.fqdn", "source.reverse_dns"],
    "significant_fields": ["source.fqdn", "source.reverse_dns"],


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
            self._insert_misp_event(intelmq_event)

        self.acknowledge_message()

    def _insert_misp_event(self, intelmq_event):
        """Insert a new MISPEvent."""
        new_misp_event = pymisp.MISPEvent()

        new_misp_event.info = 'Created by IntelMQ MISP API Output Bot.'

        # set the tags
        new_misp_event.add_tag(self.parameters.misp_tag_for_bot)

        if (self.parameters.add_feed_provider_as_tag and
                'feed.provider' in intelmq_event):
            new_tag = 'IntelMQ:feed.provider="{}"'.format(
                intelmq_event['feed.provider'])
            new_misp_event.add_tag(new_tag)

        for new_tag in self.parameters.misp_additional_tags:
            new_misp_event.add_tag(new_tag)

        # build the MISPObject and its attributes
        obj = new_misp_event.add_object(name='intelmq_event')

        fields_to_correlate = (
            self.parameters.significant_fields +
            self.parameters.misp_additional_correlation_fields
        )

        for object_relation, value in intelmq_event.items():
            try:
                obj.add_attribute(
                    object_relation,
                    value=value,
                    disable_correlation=(
                        object_relation not in fields_to_correlate),
                    to_ids=(
                        object_relation in self.parameters.misp_to_ids_fields)
                )
            except pymisp.NewAttributeError:
                msg = 'Ignoring "{}":"{}" as not in object template.'
                self.logger.debug(msg.format(object_relation, value))

        misp_event = self.misp.add_event(new_misp_event)
        self.logger.info(
            'Inserted new MISP event with id: {}'.format(misp_event.id))

    @staticmethod
    def check(parameters):
        required_parameters = [
            'add_feed_provider_as_tag',
            'misp_additional_correlation_fields',
            'misp_additional_tags',
            'misp_key',
            'misp_tag_for_bot',
            'misp_to_ids_fields',
            'misp_url',
            'significant_fields'
            ]
        missing_parameters = []
        for para in required_parameters:
            if para not in parameters:
                missing_parameters.append(para)

        if len(missing_parameters) > 0:
            return [["error",
                     "Parameters missing: " + str(missing_parameters)]]


BOT = MISPAPIOutputBot
