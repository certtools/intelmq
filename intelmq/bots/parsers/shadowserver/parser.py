# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 by Bundesamt für Sicherheit in der Informationstechnik
Software engineering by Intevation GmbH

This is an "all-in-one" parser for a lot of shadowserver feeds.
It depends on the configuration in the file "config.py"
which holds information on how to treat certain shadowserverfeeds.
It uses the report field extra.file_name to determine wich config should apply,
so this field is required.

This parser will only work with csv files named like
2019-01-01-scan_http-country-geo.csv.

Optional parameters:
    keep_feedname: Bool, default False. If True, it keeps the report's
    feed.name and does not override it with the corresponding feed name.
"""
import copy
import re

import intelmq.bots.parsers.shadowserver.config as config
from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue
from intelmq.lib import utils


class ShadowserverParserBot(ParserBot):

    recover_line = ParserBot.recover_line_csv_dict
    csv_params = {'dialect': 'unix'}
    __is_filename_regex = re.compile(r'\d{4}-\d{2}-\d{2}-(\w+)(-\w+)*\.csv')

    def init(self):

        # Set a switch if the parser shall keep the report's feed.name,
        self.keep_feedname= False
        if hasattr(self.parameters, 'keep_feedname'):
            if self.parameters.keep_feedname:
                self.keep_feedname = True


    def parse(self, report):

        # Set config to parse report
        self.sparser_config = None
        self.report_name = report.get('extra.file_name')
        filename_search = self.__is_filename_regex.search(self.report_name)

        if not filename_search:
            raise ValueError('Report\'s extra.file_name \'{}\' is not valid.'.format(self.report_name))
        else:
            self.report_name = filename_search.group(1)
            self.logger.info('Report name: {}.'.format(self.report_name))
            self.sparser_config = config.get_feed(self.report_name)

            if not self.sparser_config:
                raise ValueError('Could not get a config for \'{}\', check feed_idx '
                                 'in config.py.'.format(self.report_name))

        # Delete constant field feed.name if keep_feedname is true so it won't
        # be updated later
        if self.keep_feedname:
            self.sparser_config.get("constant_fields", None).pop("feed.name",None)

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
                    raise ValueError('Required column \'{}\' not found in feed \'{}\'. Possible change in data'
                                     ' format or misconfiguration.'.format(shadowkey, self.report_name))
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
                    self.logger.warning('Optional key \'{}\' not found in feed \'{}\'. Possible change in data'
                                        ' format or misconfiguration.'.format(shadowkey, self.report_name))
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
                                          shadowkey, self.report_name, raw_value, conv_func.__name__)
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
                                      shadowkey, self.report_name)
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
