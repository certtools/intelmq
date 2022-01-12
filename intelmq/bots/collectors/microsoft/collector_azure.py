# SPDX-FileCopyrightText: 2017 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Uses the azure.storage.blob module. Tested with version 12.13.1
"""
import gzip
import io

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.mixins import CacheMixin

try:
    from azure.storage.blob import ContainerClient
except ImportError:
    ContainerClient = None  # noqa
try:
    from azure.storage.blob._shared.base_client import create_configuration
except ImportError:
    create_configuration = None  # noqa


class MicrosoftAzureCollectorBot(CollectorBot, CacheMixin):
    "Fetch data blobs from a Microsoft Azure container"
    connection_string: str = "<insert your connection string here>"
    container_name: str = "<insert the container name>"
    rate_limit: int = 3600
    redis_cache_db = "5"  # TODO could this be int?
    redis_cache_host: str = "127.0.0.1"  # TODO could this be ip
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 864000  # 10 days

    def init(self):
        if ContainerClient is None or create_configuration is None:
            raise MissingDependencyError("azure.storage", version='>=12.0.0')

        self.config = create_configuration(storage_sdk='blob')
        if hasattr(self, 'https_proxy'):
            # Create a storage configuration object and update the proxy policy
            self.config.proxy_policy.proxies = {
                'http': self.http_proxy,
                'https': self.https_proxy,
            }

    def process(self):
        container_client = ContainerClient.from_connection_string(conn_str=self.connection_string,
                                                                  container_name=self.container_name,
                                                                  _configuration=self.config)
        for blob in container_client.list_blobs():
            if self.cache_get(blob.name):
                self.logger.debug('Processed file %r already.', blob.name)
                continue
            self.logger.debug('Processing blob %r.', blob.name)
            blob_obj = io.BytesIO()
            container_client.download_blob(blob).readinto(blob_obj)
            blob_obj.seek(0)
            report = self.new_report()
            report.add('raw', gzip.GzipFile(fileobj=blob_obj).read().decode())
            self.send_message(report)
            self.cache_set(blob.name, 1)  # Redis-py >= 3.0.0 does not allow True


BOT = MicrosoftAzureCollectorBot
