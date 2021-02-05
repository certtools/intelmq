"""
Shadowserver JSON Parser

SPDX-FileCopyrightText: 2020 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import re
from typing import Any

from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import InvalidKey, InvalidValue
import intelmq.bots.parsers.shadowserver.config as config
import intelmq.lib.message as libmessage


class ShadowserverJSONParserBot(ParserBot):
    """
    Shadowserver JSON Parser

    Parameters
    ----------
    feedname: str
        The name of the feed

    """
    __is_filename_regex = re.compile(r'^(?:\d{4}-\d{2}-\d{2}-)?(\w+)(-\w+)*\.csv$')
    reporttype_fn = None
    feedname = None
    sparser_config = None
    recover_line = ParserBot.recover_line_json

    def init(self):
        if getattr(self.parameters, 'feedname', None):
            feedname = self.parameters.feedname
            self.sparser_config = config.get_feed_by_feedname(feedname)
            if self.sparser_config:
                self.logger.info('Using fixed feed name %r for parsing reports.', feedname)
            else:
                self.logger.info('Could not determine the feed by the feed name %r given by parameter. '
                                 'Will determine the feed from the file names.', feedname)

    def parse(self, report):
        report_name = report.get('extra.file_name')
        if not report_name:
            raise ValueError("No feedname given as parameter and the "
                             "processed report has no 'extra.file_name'. "
                             "Ensure that at least one is given. "
                             "Also have a look at the documentation of the bot.")

        filename_search = self.__is_filename_regex.search(report_name)

        if not filename_search:
            raise ValueError("Report's 'extra.file_name' {!r} is not valid.".format(report_name))
        report_name = filename_search.group(1)

        self.logger.debug("Detected report's file name: %s.", report_name)
        retval = config.get_feed_by_filename(report_name)

        if not retval:
            raise ValueError('Could not get a config for {!r}, check the documentation.'
                             ''.format(report_name))
        self.feedname, self.sparser_config = retval

        return self.parse_json(report)

    def parse_line(self, line: Any, report: libmessage.Report):
        conf = self.sparser_config
        processedkeys = []

        event = self.new_event(report)
        event.add('feed.name', self.feedname)

        extra = {}

        for entry in conf.get('required_fields'):
            intelmqkey, shadowserverkey = entry[0], entry[1]
            value = self.get_value_from_config(line, entry)

            if value is not None:
                event.add(intelmqkey, value)
                processedkeys.append(shadowserverkey)

        # Now add optional fields.
        # This action may fail, the value is added to
        # extra if an add operation failed
        for entry in conf.get('optional_fields'):
            intelmqkey, shadowserverkey = entry[0], entry[1]
            try:
                value = self.get_value_from_config(line, entry)
            except ValueError:
                self.logger.warning('Optional key %s not found in feed %s. Possible change in data'
                                    ' format or misconfiguration.', shadowserverkey, self.feedname)
                continue

            intelmqkey, shadowserverkey = entry[0], entry[1]
            if value is not None:
                if intelmqkey == 'extra.':
                    extra[shadowserverkey] = value
                    processedkeys.append(shadowserverkey)
                    continue
                elif intelmqkey and intelmqkey.startswith('extra.'):
                    extra[intelmqkey.replace('extra.', '', 1)] = value
                    processedkeys.append(shadowserverkey)
                    continue
                elif intelmqkey is False:
                    # ignore it explicitly
                    processedkeys.append(shadowserverkey)
                    continue
                try:
                    event.add(intelmqkey, value)
                    processedkeys.append(shadowserverkey)
                except InvalidValue:
                    self.logger.debug('Could not add key %r in feed %r, adding it to extras.',
                                      shadowserverkey, self.feedname)
                except InvalidKey:
                    extra[intelmqkey] = value
                    processedkeys.append(shadowserverkey)
            else:
                processedkeys.append(shadowserverkey)

        # Now add additional constant fields.
        event.update(conf.get('constant_fields', {}))

        event.add('raw', self.recover_line_json(line))

        # Add everything which could not be resolved to extra.
        for key in line:
            if key not in processedkeys:
                val = line[key]
                if not val == "":
                    extra[key] = val

        if extra:
            event.add('extra', extra)

        yield event

    def get_value_from_config(self, data, entry):
        """
        Given a specific config, get the value for that data based on the entry
        """
        conv_fun = None

        shadowserverkey = entry[1]
        raw_value = data.get(shadowserverkey, None)
        value = raw_value

        if raw_value is None:
            raise ValueError('Key {!r} not found in feed {!r}. Possible change in data'
                             ' format or misconfiguration.'.format(shadowserverkey, self.feedname))
        if len(entry) > 2:
            conv_fun = entry[2]

        if conv_fun is not None and raw_value is not None:
            if len(entry) == 4 and entry[3]:
                try:
                    value = conv_fun(raw_value, data)
                except Exception:
                    self.logger.error('Could not convert shadowserverkey: %r in feed %r, '
                                      'value: %r via conversion function %r.',
                                      shadowserverkey, self.feedname, raw_value, conv_fun.__name__)
                    raise
            else:
                try:
                    value = conv_fun(raw_value)
                except Exception:
                    self.logger.error('Could not convert shadowserverkey: %r in feed %r, '
                                      'value: %r via conversion function %r.',
                                      shadowserverkey, self.feedname, raw_value, conv_fun.__name__)
                    raise
        return value


BOT = ShadowserverJSONParserBot
