# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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
import gzip
import io
import re
import sys
from datetime import datetime, timedelta

import pytz
from dateutil import parser

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin, CacheMixin
from intelmq.lib.utils import parse_relative
from intelmq.lib.exceptions import MissingDependencyError

URL_LIST = 'https://interflow.azure-api.net/file/api/file/listsharedfiles'
URL_DOWNLOAD = 'https://interflow.azure-api.net/file/api/file/download?fileName=%s'


class MicrosoftInterflowCollectorBot(CollectorBot, HttpMixin, CacheMixin):
    "Fetch data from the Microsoft Interflow API"
    api_key: str = ""
    file_match = None  # TODO type
    http_timeout_sec: int = 300
    not_older_than: str = "2 days"
    rate_limit: int = 3600
    redis_cache_db: str = "5"  # TODO type: int?
    redis_cache_host: str = "127.0.0.1"  # TODO type ipadress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 604800

    def check_ttl_time(self):
        """
        Checks if the cache's TTL is big enough compared to the chosen
        time frame so that the bot does not process the same data over and
        over.
        """
        if isinstance(self.time_match, datetime):  # absolute
            now = datetime.now(tz=pytz.timezone('UTC'))
            if now - timedelta(seconds=self.redis_cache_ttl) > self.time_match:
                raise ValueError("The cache's TTL must be higher than 'not_older_than', "
                                 "otherwise the bot is processing the same data over and over again.")

    def init(self):
        self.http_header['Ocp-Apim-Subscription-Key'] = self.api_key
        if self.file_match:
            self.file_match = re.compile(self.file_match)
        else:
            self.file_match = None

        if self.not_older_than:
            try:
                self.time_match = timedelta(minutes=parse_relative(self.not_older_than))
            except ValueError:
                self.time_match = parser.parse(self.not_older_than).astimezone(pytz.utc)
                self.logger.info("Filtering files absolute %r.", self.time_match)
                self.check_ttl_time()
            else:
                self.logger.info("Filtering files relative %r.", self.time_match)
                if timedelta(seconds=self.redis_cache_ttl) < self.time_match:
                    raise ValueError("The cache's TTL must be higher than 'not_older_than', "
                                     "otherwise the bot is processing the same data over and over again.")
        else:
            self.time_match = None

    def process(self):
        self.check_ttl_time()
        self.logger.debug('Downloading file list.')
        files = self.http_get(URL_LIST)
        files.raise_for_status()
        self.logger.debug('Downloaded file list, %s entries.', len(files.json()))
        for file in files.json():
            if self.cache_get(file['Name']):
                self.logger.debug('Processed file %s already.', file['Name'])
                continue
            if self.file_match and not self.file_match.match(file['Name']):
                self.logger.debug('File %r does not match filename filter.', file['Name'])
                continue
            filetime = parser.parse(file['LastModified'])
            if isinstance(self.time_match, datetime) and filetime < self.time_match:
                self.logger.debug('File %r does not match absolute time filter.', file['Name'])
                continue
            else:
                now = datetime.now(tz=pytz.timezone('UTC'))
                if isinstance(self.time_match, timedelta) and filetime < (now - self.time_match):
                    self.logger.debug('File %r does not match relative time filter.', file['Name'])
                    continue

            self.logger.debug('Processing file %r.', file['Name'])
            download_url = URL_DOWNLOAD % file['Name']
            download = self.http_get(download_url)
            download.raise_for_status()
            if download_url.endswith('.gz'):
                raw = gzip.open(io.BytesIO(download.content)).read().decode()
            else:
                raw = download.text
            report = self.new_report()
            report.add('feed.url', download_url)
            report.add('raw', raw)
            self.send_message(report)
            # redis-py >= 3.0.0 does no longer support boolean values, cast to string explicitly, also for backwards compatibility
            self.cache_set(file['Name'], "True")

    def print_filelist(self):
        """ Can be called from the debugger for example. """
        self.logger.debug('Downloading file list.')
        files = self.http_get(URL_LIST)
        files.raise_for_status()
        self.logger.debug('Downloaded file list, %s entries.', len(files.json()))
        print(files.text)


BOT = MicrosoftInterflowCollectorBot
