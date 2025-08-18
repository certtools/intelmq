"""
SPDX-FileCopyrightText: 2025 Ladislav Baco
SPDX-License-Identifier: AGPL-3.0-or-later

Get indicator objects from TAXII server

Configuration parameters: taxii collection (feed) url, username and password.
"""

import datetime
import json
from requests.exceptions import HTTPError

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import taxii2client.v21 as taxii2
except ImportError:
    taxii2 = None


class TaxiiCollectorBot(CollectorBot):
    """Collect data from TAXII Server"""
    collection: str = None
    username: str = None
    password: str = None
    rate_limit: int = 3600
    time_delta: int = 3600

    def init(self):
        if taxii2 is None:
            raise MissingDependencyError('taxii2-client')

        if self.collection is None:
            raise ValueError('No TAXII collection URL provided.')
        if self.username is None:
            raise ValueError('No TAXII username provided.')
        if self.password is None:
            raise ValueError('No TAXII password provided.')

        self._date_after = datetime.datetime.now() - datetime.timedelta(seconds=int(self.time_delta))

        self._taxii_collection = taxii2.Collection(self.collection, user=self.username, password=self.password)

    def process(self):
        try:
            title = self._taxii_collection.title
            self.logger.info('Collection title: %r.', title)

            # get the indicator objects
            objects = self._taxii_collection.get_objects(added_after=self._date_after, type='indicator').get('objects', [])
            for obj in objects:
                report = self.new_report()
                report.add('raw', json.dumps(obj))
                report.add('feed.url', self.collection)
                report.add('feed.code', title)
                self.send_message(report)

        except HTTPError as e:
            self.logger.error('Connection error: %r!', e)


BOT = TaxiiCollectorBot
