# SPDX-FileCopyrightText: 2016 by Bundesamt für Sicherheit in der Informationstechnik
#
# SPDX-License-Identifier: AGPL-3.0-or-later
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
import os
import tempfile

from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue
from intelmq.bin.intelmqctl import IntelMQController
import intelmq.lib.utils as utils
import intelmq.bots.parsers.shadowserver._config as config


class ShadowserverParserBot(ParserBot):
    """
    Parse all ShadowServer feeds

    Parameters:
        auto_update (boolean): Enable automatic schema download
        test_mode (boolean): Use test schema
    """

    recover_line = ParserBot.recover_line_csv_dict
    _csv_params = {'dialect': 'unix'}
    __is_filename_regex = re.compile(r'^(?:\d{4}-\d{2}-\d{2}-)?(\w+)(-\w+)*\.csv$')
    _sparser_config = None
    feedname = None
    _mode = None
    overwrite = False
    auto_update = False
    test_mode = False

    def init(self):
        config.set_logger(self.logger)
        if self.test_mode:
            config.enable_test_mode(True)
        if self.auto_update:
            config.enable_auto_update(True)
            self.logger.debug("Feature 'auto_update' is enabled.")
        config.reload()

        if self.feedname is not None:
            self._sparser_config = config.get_feed_by_feedname(self.feedname)
            if self._sparser_config:
                self.logger.info('Using fixed feed name %r for parsing reports.' % self.feedname)
                self._mode = 'fixed'
            else:
                self.logger.info('Could not determine the feed by the feed name %r given by parameter. '
                                 'Will determine the feed from the file names.',
                                 self.feedname)
                self._mode = 'detect'
        else:
            self._mode = 'detect'

    def parse(self, report):
        if self._mode == 'fixed':
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
            raise ValueError(f"Report's 'extra.file_name' {self.report_name!r} is not valid.")
        else:
            self.report_name = filename_search.group(1)
            self.logger.debug(f"Detected report's file name: {self.report_name!r}.")
            retval = config.get_feed_by_filename(self.report_name)

            if not retval:
                raise ValueError('Could not get a config for {!r}, check the documentation.'
                                 ''.format(self.report_name))
            self.feedname, self._sparser_config = retval

        # Set default csv parse function
        return self.parse_csv_dict(report)

    def parse_line(self, row, report):

        conf = self._sparser_config

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
                if shadowkey not in row:  # key does not exist in data (not even in the header)
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
                try:
                    if len(item) == 4 and item[3]:
                        value = config.functions[conv_func](raw_value, row)
                    else:
                        value = config.functions[conv_func](raw_value)
                except Exception:
                    """ fail early and often in this case. We want to be able to convert everything """
                    self.logger.error('Could not convert shadowkey: %r in feed %r, '
                                      'value: %r via conversion function %r.',
                                      shadowkey, self.feedname, raw_value, conv_func)
                    raise

            if value is not None:
                event.add(intelmqkey, value)
                fields.remove(shadowkey)

        # Now add optional fields.
        # This action may fail, the value is added to
        # extra if an add operation failed
        for item in conf.get('optional_fields'):
            intelmqkey, shadowkey = item[:2]
            if shadowkey not in fields:
                if shadowkey not in row:  # key does not exist in data (not even in the header)
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
                try:
                    if len(item) == 4 and item[3]:
                        value = config.functions[conv_func](raw_value, row)
                    else:
                        value = config.functions[conv_func](raw_value)
                except Exception:
                    """ fail early and often in this case. We want to be able to convert everything """
                    self.logger.error('Could not convert shadowkey: %r in feed %r, '
                                      'value: %r via conversion function %r.',
                                      shadowkey, self.feedname, raw_value, conv_func)
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

        event.add('raw', self.recover_line())

        # Add everything which could not be resolved to extra.
        for f in fields:
            val = row[f]
            if not val == "":
                extra[f] = val

        if extra:
            event.add('extra', extra)

        yield event

    def shutdown(self):
        self.feedname = None

    @classmethod
    def _create_argparser(cls):
        argparser = super()._create_argparser()
        argparser.add_argument("--update-schema", action='store_true', help='downloads latest report schema')
        argparser.add_argument("--verbose", action='store_true', help='be verbose')
        return argparser

    @classmethod
    def run(cls, parsed_args=None):
        if not parsed_args:
            parsed_args = cls._create_argparser().parse_args()
        if parsed_args.update_schema:
            logger = utils.log(__name__, log_path=None)
            if parsed_args.verbose:
                logger.setLevel('INFO')
            else:
                logger.setLevel('ERROR')
            config.set_logger(logger)
            if config.update_schema():
                runtime_conf = utils.get_bots_settings()
                try:
                    ctl = IntelMQController()
                    for bot in runtime_conf:
                        if runtime_conf[bot]["module"] == __name__:
                            ctl.bot_reload(bot)
                except Exception as e:
                    logger.error("Failed to signal bot: %r" % str(e))
        else:
            super().run(parsed_args=parsed_args)

    def test_update_schema(cls):
        with tempfile.TemporaryDirectory() as tmp_dir:
            schema_file = config.prepare_update_schema_test(tmp_dir)
            return config.update_schema()


BOT = ShadowserverParserBot
