"""Connect to a MISP instance and add event as MISPObject if not there already.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Reiter <bernhard@intevation.de>

A shortened copy of this documentation is kept at `docs/user/bots.rst`, please
keep it current, when changing something.

Parameters:
  - add_feed_provider_as_tag: bool (use true when in doubt)
  - add_feed_name_as_as_tag: bool (use true when in doubt)
  - misp_additional_correlation_fields: list of fields for which
        the correlation flags will be enabled (in addition to those which are
        in significant_fields)
  - misp_additional_tags: list of tags to set not be searched for
        when looking for duplicates
  - misp_key: str, API key for accessing MISP
  - misp_publish: bool, if a new MISP event should be set to "publish".
        Expert setting as MISP may really make it "public"!
        (Use false when in doubt.)
  - misp_tag_for_bot: str, used to mark MISP events
  - misp_to_ids_fields: list of fields for which the to_ids flags will be set
  - misp_url: str, URL of the MISP server
  - significant_fields: list of intelmq field names

The `significant_fields` values
will be searched for in all MISP attribute values
and if all values are found in the one MISP event, no new MISP event
will be created.
(The reason that all values are matched without considering the
attribute type is a technical limitation of the
search functionality exposed by the MISP/pymisp 2.4.120 API.)
Instead if the existing MISP events have the same feed.provider
and match closely, their timestamp will be updated.

If a new MISP event is inserted the `significant_fields` and the
`misp_additional_correlation_fields` will be the attributes
where correlation is enabled.

Make sure to build the IntelMQ Botnet in a way the rate of incoming
events is what MISP can handle, as IntelMQ can process many more events faster
than MISP (which is by design as MISP is for manual handling).
Also remove the fields of the IntelMQ events with an expert bot
that you do not want to be inserted into MISP.

Example (of some parameters in JSON)::

    "add_feed_provider_as_tag": true,
    "add_feed_name_as_tag": true,
    "misp_additional_correlation_fields": ["source.asn"],
    "misp_additional_tags": ["OSINT", "osint:certainty==\"90\""],
    "misp_publish": false,
    "misp_to_ids_fields": ["source.fqdn", "source.reverse_dns"],
    "significant_fields": ["source.fqdn", "source.reverse_dns"],


Originally developed with pymisp v2.4.120 (which needs python v>=3.6).
"""
import datetime

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pymisp
except ImportError:
    pymisp = None
    import_fail_reason = 'import'
except SyntaxError:
    pymisp = None
    import_fail_reason = 'syntax'

MISPOBJECT_NAME = 'intelmq_event'


class MISPAPIOutputBot(OutputBot):
    is_multithreadable = False

    def init(self):
        if pymisp is None and import_fail_reason == 'syntax':
            raise MissingDependencyError(
                "pymisp",
                version='>=2.4.120',
                additional_text="Python versions >= 3.6 are "
                                "required for this 'pymisp' version."
            )
        elif pymisp is None:
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
            if sig_field in intelmq_event and intelmq_event[sig_field]:
                values_to_search_for.append(intelmq_event[sig_field])

        if values_to_search_for == []:
            msg = 'All significant_fields empty -> skipping event (raw={}).'
            self.logger.warning(msg.format(intelmq_event.get('raw')))
        else:
            vquery = self.misp.build_complex_query(
                and_parameters=values_to_search_for
            )
            # limit=20 is a safeguard against searches that'll find too much,
            # as the returning python objects can take up much time and memory
            # and because there should only be one matching MISPEvent
            r = self.misp.search(tags=self.parameters.misp_tag_for_bot,
                                 value=vquery, limit=20)
            if len(r) > 0:
                msg = 'Found MISP events matching {}: {} -> not inserting.'
                self.logger.info(msg.format(vquery, [event.id for event in r]))

                for misp_event in r:
                    self._update_misp_event(misp_event, intelmq_event)
            else:
                self._insert_misp_event(intelmq_event)

        self.acknowledge_message()

    def _update_misp_event(self, misp_event, intelmq_event):
        """Update timestamp on a found MISPEvent if it matches closely."""
        # As we insert only one MISPObject, we only examine the first one
        misp_o = misp_event.get_objects_by_name(MISPOBJECT_NAME)[0]

        all_found = True
        for field in ['feed.provider'] + self.parameters.significant_fields:
            attributes = misp_o.get_attributes_by_relation(field)
            value = attributes[0].value if len(attributes) > 0 else None
            if not (value == intelmq_event.get(field)):
                all_found = False
                break

        if all_found:
            misp_event.timestamp = datetime.datetime.now()
            self.misp.update_event(misp_event)
            msg = 'Updated timestamp of MISP event with id: {}'
            self.logger.info(msg.format(misp_event.id))

    def _insert_misp_event(self, intelmq_event):
        """Insert a new MISPEvent."""
        new_misp_event = pymisp.MISPEvent()

        if 'feed.provider' in intelmq_event:
            new_misp_event.info = 'from {} via IntelMQ'.format(
                intelmq_event['feed.provider'])
        else:
            new_misp_event.info = 'via IntelMQ'

        # set the tags
        new_misp_event.add_tag(self.parameters.misp_tag_for_bot)

        if (self.parameters.add_feed_provider_as_tag and
                'feed.provider' in intelmq_event):
            new_tag = 'IntelMQ:feed.provider="{}"'.format(
                intelmq_event['feed.provider'])
            new_misp_event.add_tag(new_tag)

        if (self.parameters.add_feed_name_as_tag and
                'feed.name' in intelmq_event):
            new_tag = 'IntelMQ:feed.name="{}"'.format(
                intelmq_event['feed.name'])
            new_misp_event.add_tag(new_tag)

        for new_tag in self.parameters.misp_additional_tags:
            new_misp_event.add_tag(new_tag)

        # build the MISPObject and its attributes
        obj = new_misp_event.add_object(name=MISPOBJECT_NAME)

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
        if self.parameters.misp_publish:
            self.misp.publish(misp_event)
        self.logger.info(
            'Inserted new MISP event with id: {}'.format(misp_event.id))

    @staticmethod
    def check(parameters):
        required_parameters = [
            'add_feed_provider_as_tag',
            'add_feed_name_as_tag',
            'misp_additional_correlation_fields',
            'misp_additional_tags',
            'misp_key',
            'misp_publish',
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
