"""Connect to a CIFv3 instance and add indicator(s).

SPDX-License-Identifier: AGPL-3.0-or-later
SPDX-FileCopyrightText: 2022 REN-ISAC

A shortened copy of this documentation is kept at `docs/user/bots.rst`, please
keep it current, when changing something.

Parameters:
  - add_feed_provider_as_tag: bool, use false when in doubt
  - cif3_additional_tags: list of tags to set on submitted indicator(s)
  - cif3_feed_confidence: float, used when mapping a feed's confidence fails or
        if static confidence param is true
  - cif3_static_confidence: bool (use false when in doubt)
  - cif3_token: str, API key for accessing CIF
  - cif3_url: str, URL of the CIFv3 instance
  - fireball: int, used to batch events before submitting to a CIFv3 instance
        (default is 500 per batch, use 0 to disable batch and send each event as received)
  - http_verify_cert: bool, used to tell whether the CIFv3 instance cert should be verified
        (default true, but can be set to false if using a local test instance)

Example (of some parameters in JSON):

    "add_feed_provider_as_tag": true,
    "cif3_additional_tags": ["intelmq"]


"""
try:
    import ujson as json
except ImportError:
    JsonLib = None

from datetime import datetime
from typing import Optional, List

from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import IntelMQException, MissingDependencyError

try:
    from cifsdk.client.http import HTTP as HttpClient
    from csirtg_indicator import Indicator
    from cifsdk._version import get_versions as get_cifsdk_version
except ImportError:
    HttpClient = None

INTELMQ_TO_CIF_FIELDS_MAP = {
    'source.ip': 'indicator',
    'source.fqdn': 'indicator',
    'source.url': 'indicator',
    'source.network': 'indicator',
    'source.port': 'port',
    'feed.url': 'reference',
    'time.source': 'lasttime',
    'time.observation': 'reporttime',
    'event_description.text': 'description',
    'event_description.url': 'reference',
    'malware.hash.md5': 'indicator',
    'malware.hash.sha1': 'indicator',
    'malware.hash.sha256': 'indicator',
    'malware.name': 'description',
    'protocol.application': 'application',
    'protocol.transport': 'protocol',
    'tlp': 'tlp',
}

INTELMQ_CLASSIFICATION_TO_CIF_TAGS_MAP = {
    'c2-server': 'botnet,c2',
    'undetermined': 'suspicious',
    'brute-force': 'bruteforce',
    'other': 'suspicious',
}


class CIF3OutputBot(OutputBot):
    """
    Submits indicators to a CIFv3 instance


    IntelMQ-Bot-Name: CIFv3 API
    """
    add_feed_provider_as_tag: bool = False
    cif3_feed_confidence: float = 5
    cif3_static_confidence: bool = False
    cif3_additional_tags: List[str] = []
    cif3_token: Optional[str] = None
    cif3_url: Optional[str] = None
    fireball: int = 500
    http_verify_cert: bool = True

    _is_multithreadable = False

    def init(self):
        try:
            cifsdk_version = int(get_cifsdk_version().get('version').split('.')[0])
        except NameError:
            cifsdk_version = 0
        # installed cifsdk version must be >=3 and < 4
        if not 3 <= cifsdk_version < 4:
            HttpClient = None
        if HttpClient is None:
            raise MissingDependencyError(
                'cifsdk',
                version='3.0.0rc4,<4.0'
            )
        elif JsonLib is None:
            raise MissingDependencyError(
                'ujson',
                version='>=2.0'
            )

        self.cif3_url = self.cif3_url.rstrip('/')

        self.logger.info(f"Connecting to CIFv3 instance at {self.cif3_url!r}.")
        self.cli = HttpClient(self.cif3_url,
                              self.cif3_token,
                              verify_ssl=self.http_verify_cert)

        try:
            _ = self.cli.ping(write=True)
        except Exception as err:
            raise ValueError(f"Error connecting to CIFv3 instance: {err}")
        else:
            self.logger.info('Connected to CIFv3 instance.')

        self.indicator_list = []
        self.indicator_list_max_records = self.fireball
        self.indicator_list_max_seconds = 5
        self.last_flushed = None

    def process(self):
        intelmq_event = self.receive_message().to_dict(jsondict_as_string=True)

        cif3_indicator = self._parse_event_to_cif3(intelmq_event)

        if not self.fireball:
            self._submit_cif3_indicator(cif3_indicator)
        elif len(self.indicator_list) > 0 and (
            (
                (datetime.now() - self.last_flushed).total_seconds() >
                self.indicator_list_max_seconds
            ) or
                len(self.indicator_list) >= self.indicator_list_max_records
        ):
            self._submit_cif3_indicator(self.indicator_list)
            self.indicator_list.clear()
        else:
            if len(self.indicator_list) == 0:
                self.last_flushed = datetime.now()
            self.indicator_list.append(cif3_indicator)

        self.acknowledge_message()

    def _parse_event_to_cif3(self, intelmq_event):
        """
        Takes in an IntelMQ event, parses fields to those used by CIFv3
        Returns CIFv3 Indicator object
        """
        # build new cif3 indicator dict
        new_cif3_dict = {}
        new_cif3_dict['tags'] = []

        new_cif3_dict['provider'] = intelmq_event.get('feed.provider', 'IntelMQ')

        # set the tags
        if (self.add_feed_provider_as_tag and
                'feed.provider' in intelmq_event):
            new_tag = intelmq_event['feed.provider']
            new_cif3_dict['tags'].append(new_tag)

        matched_tag = False
        if 'classification.type' in intelmq_event:
            for classification in INTELMQ_CLASSIFICATION_TO_CIF_TAGS_MAP.keys():
                if classification in intelmq_event['classification.type']:
                    new_cif3_dict['tags'].extend(
                        INTELMQ_CLASSIFICATION_TO_CIF_TAGS_MAP[classification].split(','))
                    matched_tag = True
            if not matched_tag:
                new_cif3_dict['tags'].append(intelmq_event['classification.type'])

        for new_tag in self.cif3_additional_tags:
            new_cif3_dict['tags'].append(new_tag)

        # map the confidence
        if 'feed.accuracy' in intelmq_event:
            if not self.cif3_static_confidence:
                new_cif3_dict['confidence'] = (intelmq_event['feed.accuracy'] / 10)
        if not new_cif3_dict.get('confidence'):
            new_cif3_dict['confidence'] = self.cif3_feed_confidence

        # map remaining IntelMQ fields to CIFv3 fields
        for intelmq_type in INTELMQ_TO_CIF_FIELDS_MAP.keys():
            if intelmq_type in intelmq_event:
                cif3_field = INTELMQ_TO_CIF_FIELDS_MAP[intelmq_type]
                new_cif3_dict[cif3_field] = intelmq_event[intelmq_type]

        # build the CIFv3 indicator object from the dict
        new_indicator = None
        try:
            new_indicator = Indicator(**new_cif3_dict)
        except Exception as err:
            self.logger.error(f"Error creating indicator: {err}")
            raise

        return new_indicator

    def _submit_cif3_indicator(self, indicators):
        # build the CIFv3 indicator object from the dict
        self.logger.debug(f"Sending {len(indicators)} indicator(s).")
        try:
            resp = self.cli.indicators_create(indicators)
        except Exception as err:
            self.logger.error(f"Error submitting indicator(s): {err}")
            raise
        else:
            if isinstance(resp, list):
                resp = json.loads(resp[0])
                if resp.get('status') == 'success':
                    resp = resp['data']
            self.logger.debug(f"CIFv3 instance successfully inserted {resp} new indicator(s).")

    @staticmethod
    def check(parameters):
        required_parameters = [
            'cif3_token',
            'cif3_url',
        ]
        missing_parameters = []
        for para in required_parameters:
            if parameters[para] is None:
                missing_parameters.append(para)

        if len(missing_parameters) > 0:
            return [["error",
                     f"These parameters must be set (not null): {missing_parameters!s}."]]


BOT = CIF3OutputBot
