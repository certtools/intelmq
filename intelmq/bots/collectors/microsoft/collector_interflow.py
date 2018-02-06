# -*- coding: utf-8 -*-
"""
https://interflow.portal.azure-api.net/

Example:

[{
"indicatorthreattype": "Botnet",
"description": "B106-Dynamer",
"indicatorexpirationdatetime": "2017-04- 05T20:21:09.0000000Z",
"tlplevel": "Green",
"severity": 60,
"firstreporteddatetime": 131356377289905913,
"version": 1.5,
"tags": [“ccTLD”,“ASN”],
"networksourceipv4": "xxx.xxx.xxx.xxx",
Microsoft Confidential"networksourceport": 23041,
"networkdestinationipv4": "yyy.yyy.yyy.yyy",
"networkdestinationport": 9003,
"isproductlicensed": "True",
"ispartnershareable": "True"
}]

Parameter:
* api_key: The API key
* file_match: an optional regex to match filenames
* not_older_than: optional
"""
import re
from datetime import datetime, timedelta

import pytz
import requests
from dateutil import parser

from intelmq.lib.bot import CollectorBot
from intelmq.lib.utils import parse_relative

URL_LIST = 'https://interflow.azure-api.net/file/api/file/listsharedfiles'
URL_DOWNLOAD = 'https://interflow.azure-api.net/file/api/file/download?fileName=%s'


class MicrosoftInterflowCollectorBot(CollectorBot):
    def init(self):
        self.set_request_parameters()
        self.http_header['Ocp-Apim-Subscription-Key'] = self.parameters.api_key
        if self.parameters.file_match:
            self.file_match = re.compile(self.parameters.file_match)
        else:
            self.file_match = None

        if self.parameters.not_older_than:
            try:
                self.time_match = parser.parse(self.parameters.not_older_than)
            except ValueError:
                self.time_match = timedelta(minutes=parse_relative(self.parameters.not_older_than))
                self.logger.info("Filtering files relative %r.", self.time_match)
            else:
                self.logger.info("Filtering files absolute %r.", self.time_match)
        else:
            self.time_match = None

    def process(self):
        files = requests.get(URL_LIST,
                             auth=self.auth,
                             proxies=self.proxy,
                             headers=self.http_header,
                             verify=self.http_verify_cert,
                             cert=self.ssl_client_cert,
                             timeout=self.http_timeout_sec)
        files.raise_for_status()
        self.logger.debug('Downloaded file list, %s entries.', len(files.json()))
        for file in files.json():
            if self.file_match and not self.file_match.match(file['Name']):
                continue
            filetime = parser.parse(file['LastModified'])
            if isinstance(self.time_match, datetime) and filetime < self.time_match:
                continue
            else:
                now = datetime.now(tz=pytz.timezone('UTC'))
                if isinstance(self.time_match, timedelta) and filetime < (now - self.time_match):
                    continue

            self.logger.debug('Processing file %r.', file['Name'])
            download_url = URL_DOWNLOAD % file['Name']
            download = requests.get(download_url,
                                    auth=self.auth,
                                    proxies=self.proxy,
                                    headers=self.http_header,
                                    verify=self.http_verify_cert,
                                    cert=self.ssl_client_cert,
                                    timeout=self.http_timeout_sec)
            download.raise_for_status()
            report = self.new_report()
            report.add('feed.url', download_url)
            report.add('raw', download.text)
            self.send_message(report)


BOT = MicrosoftInterflowCollectorBot
