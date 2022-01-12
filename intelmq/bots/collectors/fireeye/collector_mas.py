# SPDX-FileCopyrightText: 2021 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Fireeye collector bot

Parameters:
http_username, http_password: string
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
host : dns name of the local appliance
request_duration: how old date should be fetched eg 24_hours or 48_hours
"""
from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.mixins import HttpMixin

try:
    import xmltodict
except ImportError:
    xmltodict = None


class FireeyeMASCollectorBot(CollectorBot, HttpMixin):

    host: str = None
    request_duration: str = None
    http_username: str = None
    http_password: str = None

    def xml_processor(self, uuid, token, new_report, host, product):

        http_url = f'https://{host}/wsapis/v2.0.0/openioc?alert_uuid={uuid}'
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
            self.logger.debug("No Iocs for UUID: %r.', uuid")

    def init(self):
        if xmltodict is None:
            raise MissingDependencyError("xmltodict")

        if self.host is None:
            raise ValueError('No host provided.')
        if self.request_duration is None:
            raise ValueError('No request_duration provided.')
        if self.http_username is None:
            raise ValueError('No http_username provided.')
        if self.http_password is None:
            raise ValueError('No http_password provided.')

        # create auth token
        self.session = self.http_session()
        self.custom_auth_url = f"https://{self.host}/wsapis/v2.0.0/auth/login"

    def process(self):
        # get token for request
        resp = self.session.post(url=self.custom_auth_url, headers=self.http_header)
        if not resp.ok:
            raise ValueError('Could not connect to appliance check User/PW. HTTP response status code was %i.' % resp.status_code)
        # extract token and build auth header
        token = resp.headers['X-FeApi-Token']
        http_header = {'X-FeApi-Token': token, 'Accept': 'application/json'}
        http_url = f"https://{self.host}/wsapis/v2.0.0/alerts?duration={self.request_duration}"
        self.logger.debug("Downloading report from %r.", http_url)
        resp = self.session.get(url=http_url, headers=http_header)
        self.logger.debug("Report downloaded.")
        message = resp.json()
        if message['alert'][0]:
            new_report = self.new_report()
            for alert in message['alert']:
                self.logger.debug('Got a new message from product %r with UUID %r.', alert['product'], alert['uuid'])
                if alert['product'] == 'EMAIL_MPS' and alert['name'] == 'MALWARE_OBJECT':
                    uuid = alert['uuid']
                    self.xml_processor(uuid, token, new_report, self.host, product="EMAIL_MPS")
                if alert['product'] == 'MAS' and alert['name'] == 'MALWARE_OBJECT':
                    uuid = alert['uuid']
                    self.xml_processor(uuid, token, new_report, self.host, product="MAS")


BOT = FireeyeMASCollectorBot
