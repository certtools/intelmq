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
from intelmq.lib.bot import ParserBot
from intelmq.lib.message import Event

from intelmq.lib.exceptions import InvalidValue, InvalidKey

import intelmq.bots.parsers.shadowserver.config as config


class ShadowserverParserBot(ParserBot):

    def init(self):
        self.sparser_config = None
        if hasattr(self.parameters, 'feedname'):
            feedname = self.parameters.feedname
            self.sparser_config = config.get_feed(feedname)

        if not self.sparser_config:
            self.logger.error('No feedname provided or feedname not in conf.')
            self.stop()

        self.csv_params = {'quoting': csv.QUOTE_NONE,
                           'escapechar': None,
                           'quotechar': '',
                           'dialect': 'unix'}

        # Set a switch if the parser shall reset the feed.name,
        # code and feedurl for this event
        self.override = False
        if hasattr(self.parameters, 'override'):
            if self.parameters.override:
                self.override = True

    def parse(self, report):
        raw_report = utils.base64_decode(report["raw"])
        csvr = csv.DictReader(io.StringIO(raw_report))

        # create an array of fieldnames,
        # those were automagically created by the dictreader
        self.fieldnames = csvr.fieldnames
        self.csv_fieldnames = map(self.conv_csv_shadowserver, self.fieldnames)
        self.header = ','.join(self.csv_fieldnames)

        for row in csvr:
            yield row

    def conv_csv_shadowserver(self, value):
        """
        Converts a dict to shadowservers csv quoting format.

        Numeric: no quoting
        Empty string: no quoting
        Else: " quoting
        """
        try:
            if str(int(value)) == value:
                return str(value)
        except ValueError:
            if hasattr(value, '__len__') and not len(value):
                return ''
            else:
                return '"'+value+'"'

    def parse_line(self, row, report):

        conf = self.sparser_config

        # we need to copy here...
        fields = copy.copy(self.fieldnames)
        # We will use this variable later.
        # Each time a field was successfully added to the
        # intelmq-event, this field will be removed from
        # the fields array.
        # at the end, all remaining fields are added to the
        # extra field.

        event = Event(report)
        extra = {}  # The Json-Object which will be populated with the
        # fields that coul not be added to the standard intelmq fields
        # the parser is going to write this information into an object
        # one level below the "extra root"
        # e.g.: extra {'cc_dns': '127.0.0.1'}

        # set feed.name and code, honor the override parameter

        if hasattr(self.parameters, 'feedname'):
            if 'feed.name' in event and self.override:
                event.add('feed.name', self.parameters.feedname, force=True)
            elif 'feed.name' not in event:
                event.add('feed.name', self.parameters.feedname)

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
                if len(item) == 4 and item[3]:
                    value = conv(raw_value, row)
                else:
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
                if len(item) == 4 and item[3]:
                    value = conv(raw_value, row)
                else:
                    value = conv(raw_value)

            if value is not None:
                if intelmqkey == 'extra.':
                    extra[shadowkey] = value
                    fields.remove(shadowkey)
                    continue
                try:
                    event.add(intelmqkey, value)
                    fields.remove(shadowkey)
                except InvalidValue:
                    self.logger.info(
                        'Could not add key "{}";'
                        ' adding it to extras...'.format(shadowkey)
                    )
                    self.logger.debug('The value of the event is %s', value)
                except InvalidKey:
                    extra[intelmqkey] = value
                    fields.remove(shadowkey)
            else:
                fields.remove(shadowkey)

        # Now add additional constant fields.
        for key, value in conf.get('constant_fields', {}).items():
            event.add(key, value)

        raw_line = {k: self.conv_csv_shadowserver(v) for k, v in row.items()}
        event.add('raw', self.recover_line(raw_line))

        # Add everything which could not be resolved to extra.
        for f in fields:
            val = row[f]
            if not val == "":
                extra[f] = val

        if extra:
            event.add('extra', extra)

        yield event

    def recover_line(self, line):
        out = self.header + '\n'
        ordered_line = [line[v] for v in self.fieldnames]
        out += ','.join(ordered_line) + '\n'
        return out


if __name__ == "__main__":
    bot = ShadowserverParserBot(sys.argv[1])
    bot.start()
