# -*- coding: utf-8 -*-
"""
Fireeye collector bot

Parameters:
http_username, http_password: string
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
dns_name : dns name of the local appliance
request_duration: how old date should be fetched eg 24_hours or 48_hours
"""
import base64
import json

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import unzip, create_request_session_from_bot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import xmltodict
except ImportError:
    xmltodict = None


class FireeyeCollectorBot(CollectorBot):

    def xml_processor(self, uuid, token, new_report, dns_name, product):

        http_url = 'https://' + dns_name + '/wsapis/v2.0.0/openioc?alert_uuid=' + uuid
        http_header = {'X-FeApi-Token': token}
        httpResponse = self.session.get(url=http_url, headers=http_header)
        binary = httpResponse.content
        self.logger.debug('Collecting information for UUID: %r .', uuid)
        try:
            my_dict = xmltodict.parse(binary)
            for indicator in my_dict['OpenIOC']['criteria']['Indicator']['IndicatorItem']:
                indicatorType = indicator['Context']['@search']
                if indicatorType == 'FileItem/Md5sum':
                    new_report = self.new_report()
                    new_report.add("raw", binary)
                    self.send_message(new_report)
        except KeyError:
            self.logger.debug("No Iocs for UUID: %r .', uuid")

    def init(self):
        if xmltodict is None:
            raise MissingDependencyError("xmltodict")

        self.set_request_parameters()
        self.session = create_request_session_from_bot(self)
        self.dns_name = getattr(self.parameters, "dns_name", None)
        if self.dns_name is None:
            raise ValueError('No dns name provided.')
        self.request_duration = getattr(self.parameters, "request_duration", None)
        if self.request_duration is None:
            raise ValueError('No request_duration provided.')
        user = getattr(self.parameters, "http_username", None)
        if user is None:
            raise ValueError('No http_username provided.')
        pw = getattr(self.parameters, "http_password", None)
        if pw is None:
            raise ValueError('No http_password provided.')

        # create auth token
        token = user + ":" + pw
        message_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        self.http_header = {'Authorization': 'Basic ' + base64_message}
        self.custom_auth_url = "https://" + self.dns_name + "/wsapis/v2.0.0/auth/login"

    def process(self):
        # get token for request
        resp = self.session.post(url=self.custom_auth_url, headers=self.http_header)
        if not resp.ok:
            raise ValueError('Could not connect to appliance check User/PW. HTTP response status code was %i.' % resp.status_code)
        # extract token and build auth header
        token = resp.headers['X-FeApi-Token']
        http_header = {'X-FeApi-Token': token, 'Accept': 'application/json'}
        http_url = "https://" + self.dns_name + "/wsapis/v2.0.0/alerts?duration=" + self.request_duration
        self.logger.debug("Downloading report from %r.", http_url)
        resp = self.session.get(url=http_url, headers=http_header)
        self.logger.debug("Report downloaded.")
        message = resp.json()
        if message['alert'][0]:
            new_report = self.new_report()
            for alert in message['alert']:
                self.logger.debug('Got a new message from PRODUCT: ' + alert['product'] + "  UUID:  " + alert['uuid'] + '.')
                if alert['product'] == 'EMAIL_MPS' and alert['name'] == 'MALWARE_OBJECT':
                    uuid = alert['uuid']
                    self.xml_processor(uuid, token, new_report, self.dns_name, product="EMAIL_MPS")
                if alert['product'] == 'MAS' and alert['name'] == 'MALWARE_OBJECT':
                    uuid = alert['uuid']
                    self.xml_processor(uuid, token, new_report, self.dns_name, product="MAS")


BOT = FireeyeCollectorBot
