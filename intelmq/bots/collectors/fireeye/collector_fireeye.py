# -*- coding: utf-8 -*-
"""
Fireeye collector bot

Parameters:
http_username, http_password: string
http_timeout_max_tries: an integer depicting how often a connection attempt is retried
dns_name : dns name of the local machine
request_duration: how old date should be fetched eg 24_hours or 48_hours
"""
import base64
import json
import MissingDependencyError

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import unzip, create_request_session_from_bot


try:
    import xmltodict
except ImportError:
    requests = None


class FireeyeCollectorBot(CollectorBot):

    def xml_processor(self, uuid, token, new_report, dns_name, product):
        with requests.Session() as s:
            url = 'https://' + dns_name + '/wsapis/v2.0.0/openioc?alert_uuid=' + uuid
            headers = {'X-FeApi-Token': token}
            httpResponse = requests.get(url, headers=headers, verify=False)
            binary = httpResponse.content
            self.logger.debug('Collecting information for UUID: %r', uuid)
            mybool = 1
            try:
                status = my_dict['fireeyeapis']['httpStatus']
                self.logger.debug("status ist:" + status)
                if status == '404':
                    mybool = 0
                    self.logger.info("status 404")
            except:
                self.logger.DEBUG("no 404 error")
            if mybool == 1:
                try:
                    my_dict = xmltodict.parse(binary)
                    for indicator in my_dict['OpenIOC']['criteria']['Indicator']['IndicatorItem']:
                        hashValue = indicator['Content']['#text']
                        indicatorType = indicator['Context']['@search']
                        if indicatorType == 'FileItem/Md5sum':
                            new_report = self.new_report()
                            new_report.add("raw", binary)
                            self.send_message(new_report)
                except KeyError:
                    self.logger.debug("No Iocs Available")

    def init(self):
        if xmltodict is None:
            raise MissingDependencyError("xmltodict")

        self.set_request_parameters()
        self.session = create_request_session_from_bot(self)
        
        if self.parameters.http_proxy and self.parameters.https_proxy:
            elf.session.proxies = {'http': self.parameters.http_proxy,
                     'https': self.parameters.https_proxy}
        else: 
            self.session.proxies = {}

        dns_name = self.parameters.dns_name
        request_duration = self.parameters.request_duration
        user = self.parameters.http_username
        pw = self.parameters.http_password
        # create auth token
        token = user + ":" + pw
        message_bytes = token.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        http_header = {'Authorization': 'Basic ' + base64_message}
        auth_url = "https://" + dns_name + "/wsapis/v2.0.0/auth/login"


    def process(self):
        # get token for requestst     
        resp = self.session.post(url=auth_url, headers=http_header)

        # extract token and build auth header
        token = resp.headers['X-FeApi-Token']
        http_header = {'X-FeApi-Token': token, 'Accept': 'application/json'}
        http_url = "https://" + dns_name + "/wsapis/v2.0.0/alerts?duration=" + request_duration

        self.logger.debug("Downloading report from %r.", http_url)
        resp = self.session.get(url=http_url, headers=http_header)
        if resp.status_code // 100 != 2:
            raise ValueError('Could not connect to appliance check User/PW. HTTP response status code was %i.' % resp.status_code)

        self.logger.debug("Report downloaded.")
        message = json.loads(resp.content)
        if message['alert'][0]:
            new_report = self.new_report()
            for alert in message['alert']:
                self.logger.debug("got a new message")
                self.logger.debug('PRODUCT: ' + alert['product'] + "  UUID:  " + alert['uuid'])
                if alert['product'] == 'EMAIL_MPS' and alert['name'] == 'MALWARE_OBJECT':
                    for k, v in alert['src'].items():
                        uuid = alert['uuid']
                        event = self.xml_processor(uuid, token, new_report, dns_name, product="EMAIL_MPS")
                if alert['product'] == 'MAS' and alert['name'] == 'MALWARE_OBJECT':
                    uuid = alert['uuid']
                    self.xml_processor(uuid, token, new_report, dns_name, product="MAS")



BOT = FireeyeCollectorBot