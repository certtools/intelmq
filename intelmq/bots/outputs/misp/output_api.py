"""Connect to MISP instance and add event as MISPObject if not reported already.

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Reiter <bernhard@intevation.de>

Parameters:
  - misp_url: URL of the MISP server
  - misp_key: API key for accessing MISP
  - misp_verify: true or false, check the validity of the certificate

TODO, this is just a stub, WIP
Tested with pymisp v2.4.120 (which needs python v>=3.6).
"""
import json
from uuid import uuid4

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import pymisp
except ImportError:
    MISPEvent = None

class MISPAPIOutputBot(OutputBot):
    is_multithreadable = False

    def init(self):
        if MISPEvent is None:
            raise MissingDependencyError('pymisp', version='>=2.4.120')


        # Initialize MISP connection
        self.misp = PyMISP(self.parameters.misp_url,
                           self.parameters.misp_key,
                           self.parameters.http_verify_cert)


        self.current_event = None

        self.misp_org = pymisp.MISPOrganisation()
        self.misp_org.name = self.parameters.misp_org_name
        self.misp_org.uuid = self.parameters.misp_org_uuid

        self.current_event = MISPEvent()


    def process(self):

            self.current_event = MISPEvent()
            self.current_event.info = ('IntelMQ event {begin} - {end}'
                                       ''.format(begin=self.min_time_current.isoformat(),
                                                 end=self.max_time_current.isoformat()))
            self.current_event.set_date(datetime.date.today())
            self.current_event.Orgc = self.misp_org
            self.current_event.uuid = str(uuid4())

        event = self.receive_message().to_dict(jsondict_as_string=True)

        obj = self.current_event.add_object(name='intelmq_event')
        for object_relation, value in event.items():
            try:
                obj.add_attribute(object_relation, value=value)
            except NewAttributeError:
                # This entry isn't listed in the harmonization file, ignoring.
                pass

        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        pass


BOT = MISPAPIOutputBot
