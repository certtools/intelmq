# -*- coding: utf-8 -*-
import datetime
import json
from pathlib import Path
from uuid import uuid4
import re

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.utils import parse_relative

try:
    from pymisp import MISPEvent, MISPOrganisation, NewAttributeError
    from pymisp.tools import feed_meta_generator
except ImportError:
    # catching SyntaxError because of https://github.com/MISP/PyMISP/issues/501
    MISPEvent = None
    import_fail_reason = 'import'
except SyntaxError:
    # catching SyntaxError because of https://github.com/MISP/PyMISP/issues/501
    MISPEvent = None
    import_fail_reason = 'syntax'


# NOTE: This module is compatible with Python 3.6+


class MISPFeedOutputBot(OutputBot):
    is_multithreadable = False

    @staticmethod
    def check_output_dir(dirname):
        output_dir = Path(dirname)
        if not output_dir.exists():
            output_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
            return True

    def init(self):
        if MISPEvent is None and import_fail_reason == 'syntax':
            raise MissingDependencyError("pymisp",
                                         version='>=2.4.117.3',
                                         additional_text="Python versions below 3.6 are "
                                                         "only supported by pymisp <= 2.4.119.1.")
        elif MISPEvent is None:
            raise MissingDependencyError('pymisp', version='>=2.4.117.3')

        self.current_event = None

        self.misp_org = MISPOrganisation()
        self.misp_org.name = self.parameters.misp_org_name
        self.misp_org.uuid = self.parameters.misp_org_uuid

        self.output_dir = Path(self.parameters.output_dir)
        MISPFeedOutputBot.check_output_dir(self.output_dir)

        if not hasattr(self.parameters, 'interval_event'):
            self.timedelta = datetime.timedelta(hours=1)
        else:
            self.timedelta = datetime.timedelta(minutes=parse_relative(self.parameters.interval_event))

        if (self.output_dir / '.current').exists():
            with (self.output_dir / '.current').open() as f:
                self.current_file = Path(f.read())
            self.current_event = MISPEvent()
            self.current_event.load_file(self.current_file)

            last_min_time, last_max_time = re.findall('IntelMQ event (.*) - (.*)', self.current_event.info)[0]
            last_min_time = datetime.datetime.strptime(last_min_time, '%Y-%m-%dT%H:%M:%S.%f')
            last_max_time = datetime.datetime.strptime(last_max_time, '%Y-%m-%dT%H:%M:%S.%f')
            if last_max_time < datetime.datetime.now():
                self.min_time_current = datetime.datetime.now()
                self.max_time_current = self.min_time_current + self.timedelta
                self.current_event = None
            else:
                self.min_time_current = last_min_time
                self.max_time_current = last_max_time
        else:
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta

    def process(self):

        if not self.current_event or datetime.datetime.now() > self.max_time_current:
            self.min_time_current = datetime.datetime.now()
            self.max_time_current = self.min_time_current + self.timedelta
            self.current_event = MISPEvent()
            self.current_event.info = ('IntelMQ event {begin} - {end}'
                                       ''.format(begin=self.min_time_current.isoformat(),
                                                 end=self.max_time_current.isoformat()))
            self.current_event.set_date(datetime.date.today())
            self.current_event.Orgc = self.misp_org
            self.current_event.uuid = str(uuid4())
            self.current_file = self.output_dir / '{self.current_event.uuid}.json'.format(self=self)
            with (self.output_dir / '.current').open('w') as f:
                f.write(str(self.current_file))

        event = self.receive_message().to_dict(jsondict_as_string=True)

        obj = self.current_event.add_object(name='intelmq_event')
        for object_relation, value in event.items():
            try:
                obj.add_attribute(object_relation, value=value)
            except NewAttributeError:
                # This entry isn't listed in the harmonization file, ignoring.
                pass

        feed_output = self.current_event.to_feed(with_meta=False)

        with self.current_file.open('w') as f:
            json.dump(feed_output, f)

        feed_meta_generator(self.output_dir)
        self.acknowledge_message()

    @staticmethod
    def check(parameters):
        if 'output_dir' not in parameters:
            return [["error", "Parameter 'output_dir' not given."]]
        try:
            created = MISPFeedOutputBot.check_output_dir(parameters['output_dir'])
        except IOError:
            return [["error",
                     "Directory %r of parameter 'output_dir' does not exist and could not be created." % parameters['output_dir']]]
        else:
            if created:
                return [["info",
                         "Directory %r of parameter 'output_dir' did not exist, but has now been created."
                         "" % parameters['output_dir']]]


BOT = MISPFeedOutputBot
