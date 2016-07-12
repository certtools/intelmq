# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This is a "generic" parser for a lot of shadowserver feeds.
It depends on the configuration in the file "config"
which holds information on how to treat certain shadowserverfeeds.

Most, if not all, feeds from shadowserver are in csv format.
This parser will only work with those.
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


class ShadowserverParserBot(Bot):

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

        # Set a switch if the parser shall reset the feed.name,
        # code and feedurl for this event
        self.override = False
        if hasattr(self.parameters, 'override'):
            if self.parameters.override:
                self.override = True

        for row in csvr:

            # we need to copy here...
            fields = copy.copy(allfields)
            # We will use this variable later.
            # Each time a field was successfully added to the
            # intelmq-event, this field will be removed from
            # the fields array.
            # at the end, all remaining fields are added to the
            # extra field.

            event = Event(report)
            extra = {}  # The Json-Object which might get into the Extra field
            sserver = {}  # The Json-Object which will be populated with the
            # fields that coul not be added to the standard intelmq fields
            # the parser is going to write this information into an object
            # one level below the "extra root"
            # e.g.: extra {'shadowserver': {'cc_dns': '127.0.0.1'}

            # set classification.type
            # TODO this might get dynamic in some feeds.
            # How to handle that?

            if not conf.get('classification_type'):
                self.logger.warn("The classification type for "
                    + self.parameters.feedname
                    + " could not be determined. Check ParserConfig!")
            else:
                event.add('classification.type', conf.get('classification_type'))

            # set feed.name and url, honor the override parameter

            if 'feed.url' in event and self.override:
                event.add('feed.url', conf.get('feed_url'), force=True)
            else:
                event.add('feed.url', conf.get('feed_url'))


            if hasattr(self.parameters, 'feedname'):
                if 'feed.name' in event and self.override:
                    event.add('feed.name', self.parameters.feedname, force=True)
                else:
                    event.add('feed.name', self.parameters.feedname)


            if hasattr(self.parameters, 'feedcode'):
                if 'feed.code' in event and self.override:
                    event.add('feed.code', self.parameters.feedcode, force=True)
                else:
                    event.add('feed.code', self.parameters.feedcode)

            # Add constant fields
            for (intelmqkey, value) in conf.get('constant_fields'):
                event.add(intelmqkey, value)

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
                        self.logger.info(
                            'Could not add event "{}";' \
                            ' adding it to extras...'.format(shadowkey)
                        )
                        self.logger.debug('The value of the event is %s', value)

            event.add('raw', '"'+','.join(map(str, row.items()))+'"')

            # Add everything which could not be resolved to extra.
            for f in fields:
                val = row[f]
                if not val == "":
                    sserver[f] = val

            if sserver:
                extra['shadowserver'] = sserver
                event.add('extra', extra)

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ShadowserverParserBot(sys.argv[1])
    bot.start()

