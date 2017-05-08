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
import copy
import csv
import io

import intelmq.bots.parsers.shadowserver.config as config
from intelmq.lib import utils
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue


class ShadowserverParserBot(ParserBot):

    def init(self):
        self.sparser_config = None
        if hasattr(self.parameters, 'feedname'):
            self.feedname = self.parameters.feedname
            self.sparser_config = config.get_feed(self.feedname)

        if not self.sparser_config:
            self.logger.error('No feedname provided or feedname not in conf.')
            self.stop()

        # Set a switch if the parser shall reset the feed.name,
        # code and feedurl for this event
        self.overwrite = False
        if hasattr(self.parameters, 'override'):  # TODOv1.1: remove
            self.logger.error('Parameter "override" is deprecated, '
                              'it is now called "overwrite". Stopping now. '
                              '(This warning will be removed before v1.1.)')
            self.stop()
        if hasattr(self.parameters, 'overwrite'):
            if self.parameters.overwrite:
                self.overwrite = True

        # Already warned about deprecation
        self.depr_warning = False

    def parse(self, report):
        raw_report = utils.base64_decode(report["raw"])
        csvr = csv.DictReader(io.StringIO(raw_report))

        # create an array of fieldnames,
        # those were automagically created by the dictreader
        self.fieldnames = csvr.fieldnames

        for row in csvr:
            yield row

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

        event = self.new_event(report)
        extra = {}  # The Json-Object which will be populated with the
        # fields that could not be added to the standard intelmq fields
        # the parser is going to write this information into an object
        # one level below the "extra root"
        # e.g.: extra {'cc_dns': '127.0.0.1'}

        # set feed.name and code, honor the overwrite parameter

        if hasattr(self.parameters, 'feedname'):
            if 'feed.name' in event and self.overwrite:
                event.add('feed.name', self.parameters.feedname, overwrite=True)
            elif 'feed.name' not in event:
                event.add('feed.name', self.parameters.feedname)

        # Iterate Config, add required fields.
        # Fail hard if not possible:
        for item in conf.get('required_fields'):
            intelmqkey, shadowkey = item[:2]
            if shadowkey not in fields:  # key does not exist in data (not even in the header)
                self.logger.warning('Required key %r not found data. Possible change in data'
                                    ' format or misconfiguration.', shadowkey)
            if len(item) > 2:
                conv_func = item[2]
            else:
                conv_func = None

            raw_value = row.get(shadowkey)

            value = raw_value

            if conv_func is not None and raw_value is not None:
                if len(item) == 4 and item[3]:
                    value = conv_func(raw_value, row)
                else:
                    value = conv_func(raw_value)

            if value is not None:
                event.add(intelmqkey, value)
                fields.remove(shadowkey)

        # Now add optional fields.
        # This action may fail, the value is added to
        # extra if an add operation failed
        for item in conf.get('optional_fields'):
            intelmqkey, shadowkey = item[:2]
            if shadowkey not in fields:  # key does not exist in data (not even in the header)
                self.logger.warning('Optional key %r not found data. Possible change in data'
                                    ' format or misconfiguration.', shadowkey)
                continue
            if len(item) > 2:
                conv_func = item[2]
            else:
                conv_func = None
            raw_value = row.get(shadowkey)
            value = raw_value

            if conv_func is not None and raw_value is not None:
                if len(item) == 4 and item[3]:
                    value = conv_func(raw_value, row)
                else:
                    try:
                        value = conv_func(raw_value)
                    except Exception:
                        self.logger.error('Could not convert shadowkey: %r, '
                                          'value: %r via conversion function %r.',
                                          shadowkey, raw_value, conv_func)
                        value = None
                        # """ fail early and often in this case. We want to be able to convert everything """
                        # self.stop()

            if value is not None:
                if intelmqkey == 'extra.':
                    extra[shadowkey] = value
                    fields.remove(shadowkey)
                    continue
                try:
                    event.add(intelmqkey, value)
                    fields.remove(shadowkey)
                except InvalidValue:
                    self.logger.debug('Could not add key %r adding it to extras.', shadowkey)
                except InvalidKey:
                    extra[intelmqkey] = value
                    fields.remove(shadowkey)
            else:
                fields.remove(shadowkey)

        # Now add additional constant fields.
        dict.update(event, conf.get('constant_fields', {}))  # TODO: rewrite in 1.0

        event.add('raw', self.recover_line(row))

        # Add everything which could not be resolved to extra.
        for f in fields:
            val = row[f]
            if not val == "":
                extra[f] = val

        if extra:
            event.add('extra', extra)

        yield event

    def recover_line(self, line):
        out = io.StringIO()
        writer = csv.DictWriter(out, self.fieldnames,
                                dialect='unix',
                                extrasaction='ignore')
        writer.writeheader()
        writer.writerow(line)
        return out.getvalue()


BOT = ShadowserverParserBot
