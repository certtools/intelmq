# -*- coding: utf-8 -*-
import json

from intelmq.lib import test, utils


REPORT_TEMPLATE = {
    'feed.url': 'https://feed.caad.fkie.fraunhofer.de/ddosattackfeed',
    '__type': 'Report',
    'feed.name': 'Fraunhofer DDoS Attack Feed',
    'time.observation': '2018-01-01T00:00:00+00:00',
}


class FraunhoferDdosAttackTestCase(test.BotTestCase):
    def set_input_message(self, *message):
        self.input_message = [create_report(m) for m in message]


def create_report(raw_data):
    report = dict(REPORT_TEMPLATE)
    report['raw'] = utils.base64_encode(json.dumps(raw_data))
    return report


def create_event(template, fields, original_message):
    event = dict(template)
    event['raw'] = utils.base64_encode(json.dumps(original_message))
    event.update(fields)
    return event


def ddos_message(domain=None, targets=None, **kwargs):
    message = {
        'cnc': {
            'domain': domain,
            'ip': '1.2.3.4',
            'port': 4711
        },
        'cnctype': 'classic_cnc',
        'message': {
            'attack': 'someattack',
            'duration': 20,
            'flags': {
                'len': '1024'
            },
            'targets': targets or ['4.3.2.1/32']
        },
        'messagetype': 'cnc_message',
        'name': 'some_malware',
        'ts': '2018-02-05T10:15:42Z'
    }
    message.update(kwargs)
    return message
