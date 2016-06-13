# -*- coding: utf-8 -*-
"""
This is a "generic" parser for a lot of shadowserver feeds.
It depends on the configuration in the file "config"
which holds information on how to treat certain shadowserverfeeds.

Most, if not all, feeds from shadowserver are in csv format.
This parser will only work with those.

TODO: Evaluate new line-based IntelMQ Parser.

"""
import csv
import io
import sys
import copy

from intelmq.lib import utils
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

from intelmq.lib.exceptions import InvalidValue

import intelmq.bots.parsers.shadowserver.config as config

class ShadowserverParser(Bot):

    def init(self):
        self.sparser_config = None
        if hasattr(self.parameters, 'feedname'):
            feedname = self.parameters.feedname
            self.sparser_config = config.get_feed(feedname)

        if not self.sparser_config:
            self.logger.error('No feedname provided or feedname not in conf.')
            self.stop()

    def process(self):
        conf = self.sparser_config

        report = self.receive_message()

        raw_report = utils.base64_decode(report["raw"])
        csvr = csv.DictReader(io.StringIO(raw_report))

        # create an array of fieldnames,
        # those were automagically created by the dictreader
        allfields = csvr.fieldnames

        for row in csvr:

            # we need to copy here...
            fields = copy.copy(allfields)
            # We will uses this variable later.
            # Each time a field was successfully added to the
            # intelmq-event, this field will be removed from
            # the fields array.
            # at the end, all remaining fields are added to the
            # extra field.

            event = Event(report)
            extra = {}

            # Iterate Config, add required fields.
            # Fail hard if not possible:
            for item in conf.get('required_fields'):
                intelmqkey, shadowkey = item[:2]
                if len(item) > 2:
                    conv = item[2]
                else:
                    conv = None

                raw_value = row.get(shadowkey)

                value = raw_value

                if conv is not None and raw_value is not None:
                    value = conv(raw_value)

                if value is not None:
                    event.add(intelmqkey, value)
                    fields.remove(shadowkey)

            # Now add optional fields.
            # This action may fail, the value is added to
            # extra if an add operation failed
            for item in conf.get('optional_fields'):
                intelmqkey, shadowkey = item[:2]
                if len(item) > 2:
                    conv = item[2]
                else:
                    conv = None
                raw_value = row.get(shadowkey)
                value = raw_value

                if conv is not None and raw_value is not None:
                    value = conv(raw_value)

                if value is not None:
                    try:
                        event.add(intelmqkey, value)
                        fields.remove(shadowkey)
                    except InvalidValue:
                        self.logger.warn(
                            'Could not add event "{}";' \
                            ' adding it to extras...'.format(shadowkey)
                        )

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')

            # Add everything which could not be resolved to extra.
            for f in fields:
                extra[f] = row[f]

            if extra:
                event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowserverParser(sys.argv[1])
    bot.start()