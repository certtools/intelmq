"""
SPDX-FileCopyrightText: 2025 Ladislav Baco
SPDX-License-Identifier: AGPL-3.0-or-later

Parse indicators objects in STIX format received from TAXII collector
"""

import json


from intelmq.lib.bot import ParserBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import stix2patterns.v21.pattern as stix2_pattern
except ImportError:
    stix2_pattern = None


class StixParserBot(ParserBot):
    """Parse STIX indicators"""
    parse = ParserBot.parse_json_stream
    recover_line = ParserBot.recover_line_json_stream

    def init(self):
        if stix2_pattern is None:
            raise MissingDependencyError('stix2-patterns')

    def parse_line(self, line, report):
        """ Parse one STIX object of indicator type """
        object_type = line.get('type', '')
        if object_type == 'indicator':
            pattern = line.get('pattern', '')
            # stix, pcre, sigma, snort, suricata, yara
            pattern_type = line.get('pattern_type', '')

            if pattern_type == 'stix':
                indicators = StixParserBot.parse_stix_pattern(pattern, self.logger)
                for indicator_type, indicator_value in indicators:
                    event = self.new_event(report)
                    event.add('raw', json.dumps(line))
                    event.add('comment', line.get('description', ''))
                    event.add('extra.labels', line.get('labels', None))
                    event.add('time.source', line.get('valid_from', '1970-01-01T00:00:00Z'))

                    # IP address may be passed in Domain feeds or Domain may be passed in URL feeds
                    # It violates the STIX format, however, in some sources it happens (e.g. in ETI)
                    # Drop such events without failures and exceptions which slowing down the processing
                    event.add(indicator_type, indicator_value, raise_failure=False)

                    # classification can be overridden by vendor-specific parser below
                    event.add('classification.type', 'undetermined')
                    self.parse_vendor_specific(event, line, report)
                    yield event
            else:
                self.logger.warning('Unexpected type of pattern expression: %r, pattern: %r', pattern_type, pattern)
        else:
            self.logger.warning('Unexpected type of STIX object: %r', object_type)

    def parse_vendor_specific(self, event, line, report):
        """
        Parse vendor specific details from the STIX 2.1 Indicator object.
        This method by default does nothing and it is called just before IntelMQ event is yielded.
        If we need vendor-specific STIX parser, we can inherit from this class and override this one method.
        """
        return

    @staticmethod
    def _get_value_from_comparison_expression(comparison, logger=None):
        """
        STIX Comparison Expressions:
        https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_boiciucr9smf

        comparison is a tuple obtained from stix2patterns.v21.pattern.Pattern(pattern).inspect().comparisons,
        e.g. (['value'], '=', "'http://example.org'"), (['value'], '=', "'127.0.0.1/32'")
        """
        if len(comparison) != 3:
            if logger:
                logger.warning('Unexpected Comparison Expressions. Expression: {}'.format(comparison))
            return

        property_name, operator, value = comparison
        supported_property_names = [['value'],
                                    ['hashes', 'MD5'],
                                    ['hashes', 'SHA-1'],
                                    ['hashes', 'SHA-256'],
                                    # Based on 10.7 Hashing Algorithm Vocabulary, these keys are not valid, but they are used in some feeds (e.g. ETI)
                                    # https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_ths0b11wzxv3
                                    ['hashes', 'SHA1'],
                                    ['hashes', 'SHA256']
                                    ]
        if not (property_name in supported_property_names) or (operator != '=') or not value.startswith("'") or not value.endswith("'"):
            if logger:
                logger.info('Unsupported Comparison Expression. Only Comparison Expressions with "equal" comparison operator and "value" or "hashes" property are supported. Expression: {}'.format(comparison))
            return

        # remove single quotes from returned value
        return value[1:-1]

    @staticmethod
    def parse_stix_pattern(pattern, logger=None):
        """
        STIX Patterning:
        https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_e8slinrhxcc9
        """

        indicators = []
        comparisons = stix2_pattern.Pattern(pattern).inspect().comparisons
        for key in comparisons.keys():
            comparison_expressions = comparisons.get(key, [])
            for comparison in comparison_expressions:
                value = StixParserBot._get_value_from_comparison_expression(comparison, logger)
                if not value:
                    pass
                if key == 'url':
                    indicators.append(('source.url', value))
                elif key == 'domain-name':
                    indicators.append(('source.fqdn', value))
                elif key == 'ipv4-addr':
                    # remove port, sometimes the port is present in ETI
                    value = value.split(':')[0]
                    # strip CIDR if IPv4 network contains single host only
                    value = value[:-3] if value.endswith('/32') else value
                    # check if pattern is in CIDR notation
                    if value.rfind('/') > -1:
                        indicators.append(('source.network', value))
                    else:
                        indicators.append(('source.ip', value))
                elif key == 'ipv6-addr':
                    # strip CIDR if IPv6 network contains single host only
                    value = value[:-4] if value.endswith('/128') else value
                    # check if pattern is in CIDR notation
                    if value.rfind('/') > -1:
                        indicators.append(('source.network', value))
                    else:
                        indicators.append(('source.ip', value))
                elif key == 'file':
                    if len(comparison) == 3 and len(comparison[0]) == 2 and comparison[0][0] == 'hashes':
                        # converts MD5, SHA-1, SHA1, SHA-256, SHA256 to md5, sha1, sha256 used in IntelMQ
                        hash_algo = comparison[0][1].lower().replace('-', '')
                        indicators.append(('malware.hash.' + hash_algo, value))
                else:
                    if logger:
                        logger.warning('Unsupported Object Type "{}" in Pattern Expression. Pattern: {}'.format(key, pattern))

        return indicators


BOT = StixParserBot
