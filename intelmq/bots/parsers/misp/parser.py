# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urljoin

from intelmq.lib import utils
from intelmq.lib.bot import Bot


class MISPParserBot(Bot):

    # Taxonomy library from ecsirt (default in MISP)
    # Mapping to the IntelMQ taxonomy
    MISP_TAXONOMY_MAPPING = {
        'ecsirt:fraud="phishing"': 'phishing',
        'ecsirt:availability="ddos"': 'ddos',
        'ecsirt:abusive-content="spam"': 'spam',
        'ecsirt:information-gathering="scanner"': 'scanner',
        'ecsirt:information-content-security="dropzone"': 'dropzone',
        'ecsirt:malicious-code="malware"': 'malware',
        'ecsirt:malicious-code="botnet-drone"': 'infected-system',
        'ecsirt:malicious-code="ransomware"': 'ransomware',
        'ecsirt:malicious-code="malware-configuration"': 'malware-configuration',
        'ecsirt:malicious-code="c2server"': 'c2server',
        'ecsirt:intrusion-attempts="exploit"': 'exploit',
        'ecsirt:intrusion-attempts="brute-force"': 'brute-force',
        'ecsirt:intrusion-attempts="ids-alert"': 'ids-alert',
        'ecsirt:intrusions="defacement"': 'defacement',
        'ecsirt:intrusions="compromised"': 'compromised',
        'ecsirt:intrusions="backdoor"': 'backdoor',
        'ecsirt:vulnerable="vulnerable-service"': 'vulnerable service',
        'ecsirt:other="blacklist"': 'blacklist',
        'ecsirt:other="unknown"': 'unknown',
        'ecsirt:test="test"': 'test',
    }

    # Event categories we process
    SUPPORTED_MISP_CATEGORIES = [
        'Payload delivery',
        'Artifacts dropped',
        'Payload installation',
        'Network activity',
    ]

    # MISP to IntelMQ data type mapping
    MISP_TYPE_MAPPING = {
        'domain': 'source.fqdn',
        'hostname': 'source.fqdn',
        'md5': 'malware.hash.md5',
        'sha1': 'malware.hash.sha1',
        'ip-src': 'source.ip',
        'ip-dst': 'source.ip',
        'email-src': 'source.account',
        'url': 'source.url',
    }

    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))
        misp_event = json.loads(raw_report)

        # Set the classifier based on the ecsirt tag
        classifier = None
        if misp_event.get('Tag'):
            for tag in misp_event['Tag']:
                if tag['name'] in self.MISP_TAXONOMY_MAPPING:
                    classifier = self.MISP_TAXONOMY_MAPPING[tag['name']]
                    break

        # get the attributes from the event
        event_attributes = misp_event['Attribute']

        # add object attributes to the list
        if 'Object' in misp_event:
            for obj in misp_event['Object']:
                event_attributes += obj['Attribute']

        # payload type - get malware variant for the event
        malware_variant = None
        for attribute in event_attributes:
            if attribute['category'] == 'Payload type':
                malware_variant = attribute['value'].lower()

        # MISP event URL
        url_path = 'events/view/{}'.format(misp_event['id'])
        misp_event_url = urljoin(report['feed.url'], url_path)

        # Process MISP event attributes as separate IntelMQ events
        for attribute in event_attributes:

            # get details of attribute
            value = attribute['value']
            uuid = attribute['uuid']
            comment = attribute['comment']
            timestamp = attribute['timestamp']
            category = attribute['category']
            type_ = attribute['type']

            # create intelmq events based on the category
            if (category in self.SUPPORTED_MISP_CATEGORIES and
                    type_ in self.MISP_TYPE_MAPPING):

                # Create and send the intelmq event
                event = self.new_event(report)
                event.add('raw', json.dumps(attribute, sort_keys=True))
                event.add(self.MISP_TYPE_MAPPING[type_], value)
                event.add('misp.event_uuid', misp_event['uuid'])
                event.add('misp.attribute_uuid', uuid)
                event.add('comment', comment)
                event.add('event_description.text', category)
                event.add('event_description.url', misp_event_url)
                event.add('malware.name', malware_variant, raise_failure=False)
                event.add('classification.type', classifier)
                event.add('time.source', '{} UTC'.format(
                          datetime.utcfromtimestamp(float(timestamp))))
                self.send_message(event)

        self.acknowledge_message()


BOT = MISPParserBot
