# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This is an "all-in-one" parser for a lot of shadowserver feeds.
It depends on the configuration in the file "config.py"
which holds information on how to treat certain shadowserverfeeds.
It uses the report field extra.file_name to determine which config should apply,
so this field is required.

This parser will only work with csv files named like
2019-01-01-scan_http-country-geo.csv.

Optional parameters:
    overwrite: Bool, default False. If True, it keeps the report's
        feed.name and does not override it with the corresponding feed name.
    feedname: The fixed feed name to use if it should not automatically detected.
"""
import copy
import re

import intelmq.bots.parsers.shadowserver.config as config
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue


class ShadowserverParserBot(ParserBot):

    recover_line = ParserBot.recover_line_csv_dict
    csv_params = {'dialect': 'unix'}
    __is_filename_regex = re.compile(r'^(?:\d{4}-\d{2}-\d{2}-)?(\w+)(-\w+)*\.csv$')
    sparser_config = None
    feedname = None
    mode = None

    def init(self):
        if getattr(self.parameters, 'feedname', None):
            self.feedname = self.parameters.feedname
            self.sparser_config = config.get_feed_by_feedname(self.feedname)
            if self.sparser_config:
                self.logger.info('Using fixed feed name %r for parsing reports.' % self.feedname)
                self.mode = 'fixed'
            else:
                self.logger.info('Could not determine the feed by the feed name %r given by parameter. '
                                 'Will determine the feed from the file names.',
                                 self.feedname)
                self.mode = 'detect'
        else:
            self.mode = 'detect'

        # Set a switch if the parser shall reset the feed.name,
        #  for this event
        self.overwrite = False
        if hasattr(self.parameters, 'overwrite'):
            if self.parameters.overwrite:
                self.overwrite = True

    def parse(self, report):
        if self.mode == 'fixed':
            return self.parse_csv_dict(report)

        # Set config to parse report
        self.report_name = report.get('extra.file_name')
        if not self.report_name:
            raise ValueError("No feedname given as parameter and the "
                             "processed report has no 'extra.file_name'. "
                             "Ensure that at least one is given. "
                             "Also have a look at the documentation of the bot.")
        filename_search = self.__is_filename_regex.search(self.report_name)

        if not filename_search:
            raise ValueError("Report's 'extra.file_name' {!r} is not valid.".format(self.report_name))
        else:
            self.report_name = filename_search.group(1)
            self.logger.debug("Detected report's file name: {!r}.".format(self.report_name))
            retval = config.get_feed_by_filename(self.report_name)

            if not retval:
                raise ValueError('Could not get a config for {!r}, check the documentation.'
                                 ''.format(self.report_name))
            self.feedname, self.sparser_config = retval

        # Set default csv parse function
        return self.parse_csv_dict(report)

    def parse_line(self, row, report):

        conf = self.sparser_config

        # https://github.com/certtools/intelmq/issues/1271
        if conf == config.drone and row.get('infection') == 'spam':
            conf = config.drone_spam

        # we need to copy here...
        fields = copy.copy(self.csv_fieldnames)
        # We will use this variable later.
        # Each time a field was successfully added to the
        # intelmq-event, this field will be removed from
        # the fields array.
        # at the end, all remaining fields are added to the
        # extra field.

        event = self.new_event(report)
        # set feed.name and code, honor the overwrite parameter
        event.add('feed.name', self.feedname, overwrite=self.overwrite)

        extra = {}  # The Json-Object which will be populated with the
        # fields that could not be added to the standard intelmq fields
        # the parser is going to write this information into an object
        # one level below the "extra root"
        # e.g.: extra {'cc_dns': '127.0.0.1'}

        # Iterate Config, add required fields.
        # Fail hard if not possible:
        for item in conf.get('required_fields'):
            intelmqkey, shadowkey = item[:2]
            if shadowkey not in fields:
                if not row.get(shadowkey):  # key does not exist in data (not even in the header)
                    raise ValueError('Required column {!r} not found in feed {!r}. Possible change in data'
                                     ' format or misconfiguration.'.format(shadowkey, self.feedname))
                else:  # key is used twice
                    fields.append(shadowkey)
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
            if shadowkey not in fields:
                if not row.get(shadowkey):  # key does not exist in data (not even in the header)
                    self.logger.warning('Optional key {!r} not found in feed {!r}. Possible change in data'
                                        ' format or misconfiguration.'.format(shadowkey, self.feedname))
                    continue
                else:  # key is used twice
                    fields.append(shadowkey)
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
                        """ fail early and often in this case. We want to be able to convert everything """
                        self.logger.error('Could not convert shadowkey: %r in feed %r, '
                                          'value: %r via conversion function %r.',
                                          shadowkey, self.feedname, raw_value, conv_func.__name__)
                        raise

            if value is not None:
                if intelmqkey == 'extra.':
                    extra[shadowkey] = value
                    fields.remove(shadowkey)
                    continue
                elif intelmqkey and intelmqkey.startswith('extra.'):
                    extra[intelmqkey.replace('extra.', '', 1)] = value
                    fields.remove(shadowkey)
                    continue
                elif intelmqkey is False:
                    # ignore it explicitly
                    fields.remove(shadowkey)
                    continue
                try:
                    event.add(intelmqkey, value)
                    fields.remove(shadowkey)
                except InvalidValue:
                    self.logger.debug('Could not add key %r in feed %r, adding it to extras.',
                                      shadowkey, self.feedname)
                except InvalidKey:
                    extra[intelmqkey] = value
                    fields.remove(shadowkey)
            else:
                fields.remove(shadowkey)

        # Now add additional constant fields.
        event.update(conf.get('constant_fields', {}))

        event.add('raw', self.recover_line(row))

        # Add everything which could not be resolved to extra.
        for f in fields:
            val = row[f]
            if not val == "":
                extra[f] = val

        if extra:
            event.add('extra', extra)

        yield event


BOT = ShadowserverParserBot
