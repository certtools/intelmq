"""Connect to MISP instance and add event as MISPObject if not reported already.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Reiter <bernhard@intevation.de>

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP

Tested with pymisp v2.4.120 (which needs python v>=3.6).

WARNING: TODO, WIP: currently inserts the event unconditionally!
"""
import json

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

        # Initialize MISP connection
        self.misp = pymisp.api.PyMISP(self.parameters.misp_url,
                                      self.parameters.misp_key,
                                      self.parameters.http_verify_cert)

        self.misp.toggle_global_pythonify()

    def process(self):
        intelmq_event = self.receive_message().to_dict(jsondict_as_string=True)

        # TODO search for existing events

        # else insert a new one

        new_misp_event = pymisp.MISPEvent()

        new_misp_event.info = 'Created by IntelMQ MISP API Output Bot.'
        new_misp_event.add_tag(self.parameters.misp_tag_for_bot)

        obj = new_misp_event.add_object(name='intelmq_event')
        for object_relation, value in intelmq_event.items():
            try:
                obj.add_attribute(object_relation, value=value)
            except NewAttributeError:
                msg = 'Ignoring "{}":"{}" because not in hamonization file.'
                self.logger.debug(msg.format(object_relation, value))

        misp_event = self.misp.add_event(new_misp_event)
        self.logger.info(
                'Inserted new MISP event with id: {}'.format(misp_event.id))

        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        required_parameters = ['misp_url', 'misp_key', 'misp_tag_for_bot']
        missing_parameters = []
        for para in required_parameters:
            if para not in parameters:
                missing_parameters.append(para)

        if len(missing_parameters) > 0 :
            return [["error", "Parameters missing: " + str(missing_parameters)]]

BOT = MISPAPIOutputBot
