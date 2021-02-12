"""
Shadowserver Reports API Collector Bot

SPDX-FileCopyrightText: 2020 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from datetime import datetime, timedelta
import hashlib
import hmac

from intelmq.lib.bot import CollectorBot
from intelmq.lib.cache import Cache
from intelmq.lib.utils import create_request_session
from intelmq.lib.exceptions import MissingDependencyError

try:
    import requests
except ImportError:
    requests = None

APIROOT = 'https://transform.shadowserver.org/api2/'


class ShadowServerAPICollectorBot(CollectorBot):
    """
    Shadowserver Reports API Collector Bot

    Parameters
    ----------
    api_key: str
        Your Shadowserver API key
    secret: str
        Your Shadowserver API secret
    country: str
        The country you want to download reports for (i.e. 'austria')
    types: list
        A list of strings or a string of comma-separated values with the names of reporttypes you want to process. If you leave this empty, all the available reports will be downloaded and processed (i.e. 'scan', 'drones', 'intel', 'sandbox_connection', 'sinkhole_combined').
    """

    def init(self):
        self.apikey = getattr(self.parameters, "api_key", None)
        if self.apikey is None:
            raise ValueError('No api_key provided.')
        self.secret = getattr(self.parameters, "secret", None)
        if self.secret is None:
            raise ValueError('No secret provided.')
        self.country = getattr(self.parameters, "country", None)
        if self.country is None:
            raise ValueError('No country provided.')

        self.types = getattr(self.parameters, 'types', None)
        if isinstance(self.types, str):
            self.types = self.types.split(',')

        self.preamble = '{{ "apikey": "{}" '.format(self.apikey)

        self.set_request_parameters()
        self.session = create_request_session(self)

        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           getattr(self.parameters, 'redis_cache_ttl', 864000),  # 10 days
                           getattr(self.parameters, "redis_cache_password", None)
                           )

    def _headers(self, data):
        return {'HMAC2': hmac.new(self.secret.encode(), data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()}

    def _reports_list(self, date=None):
        """
        Get a list of all the reports shadowserver has for a specific country
        via the reports/list endpoint. If a list of types is set in the
        parameters, we only process reports with those types.
        To be on the safe side regarding different calculations of timestamps,
        we request reports over a timespan of four days: two days in the past
        until one day in the future.
        The names of processed reports are cached and therefore not processed
        again.
        """
        if date is None:
            date = datetime.today().date()
        daybefore = date - timedelta(2)
        dayafter = date + timedelta(1)

        data = self.preamble
        data += ',"report": ["{}"] '.format(self.country)
        data += ',"date": "{}:{}" '.format(daybefore.isoformat(), dayafter.isoformat())
        data += '}'
        self.logger.debug('Downloading report list with data: %s.', data)

        response = self.session.post(APIROOT + 'reports/list', data=data, headers=self._headers(data))
        response.raise_for_status()

        reports = response.json()
        self.logger.debug('Downloaded report list, %s entries.', len(reports))

        if 'error' in reports:
            self.logger.debug('There was an error downloading the reports: %s', reports['error'])
            return None

        if self.types is not None:
            reports = [report for report in reports if any(rtype in report['file'] for rtype in self.types)]

        return reports

    def _report_download(self, reportid: str):
        """
        Download one report from the shadowserver API via the reports/download endpoint
        """
        data = self.preamble
        data += ',"id": "{}"}}'.format(reportid)
        self.logger.debug('Downloading report with data: %s.', data)

        response = self.session.post(APIROOT + 'reports/download', data=data, headers=self._headers(data))
        response.raise_for_status()

        return response.text

    def process(self):
        """
        Download reports and send them.
        Cache the filename of the report to not download the same report again.
        """
        reportslist = self._reports_list()
        self.logger.debug('Reports list contains %s entries after filtering.', len(reportslist))

        for item in reportslist:
            filename = item['file']
            if self.cache.get(filename):
                self.logger.debug('Processed file %r already.', filename)
                continue
            self.logger.debug('Processing file %s.', filename)
            reportdata = self._report_download(item['id'])
            report = self.new_report()
            report.add('extra.file_name', filename)
            report.add('raw', str(reportdata))
            self.send_message(report)
            self.cache.set(filename, 1)
            self.logger.debug('Sent report: %s.', filename)


BOT = ShadowServerAPICollectorBot
