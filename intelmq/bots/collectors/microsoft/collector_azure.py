# -*- coding: utf-8 -*-
"""
Uses the azure.storage.blob module. Tested with version 12.13.1
"""
import gzip
import io

from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError
from intelmq.lib.cache import Cache

try:
    from azure.storage.blob import ContainerClient
except ImportError:
    ContainerClient = None  # noqa
try:
    from azure.storage.blob._shared.base_client import create_configuration
except ImportError:
    create_configuration = None  # noqa


class MicrosoftAzureCollectorBot(CollectorBot):
    def init(self):
        if ContainerClient is None or create_configuration is None:
            raise MissingDependencyError("azure.storage")

        self.config = create_configuration(storage_sdk='blob')
        if hasattr(self.parameters, 'https_proxy'):
            # Create a storage configuration object and update the proxy policy
            self.config.proxy_policy.proxies = {
                'http': self.parameters.http_proxy,
                'https': self.parameters.https_proxy,
            }

        self.cache = Cache(self.parameters.redis_cache_host,
                           self.parameters.redis_cache_port,
                           self.parameters.redis_cache_db,
                           getattr(self.parameters, 'redis_cache_ttl', 864000),  # 10 days
                           getattr(self.parameters, "redis_cache_password",
                                   None)
                           )

    def process(self):
        container_client = ContainerClient.from_connection_string(conn_str=self.parameters.connection_string,
                                                                  container_name=self.parameters.container_name,
                                                                  _configuration=self.config)
        for blob in container_client.list_blobs():
            if self.cache.get(blob.name):
                self.logger.debug('Processed file %r already.', blob.name)
                continue
            self.logger.debug('Processing blob %r.', blob.name)
            blob_obj = io.BytesIO()
            container_client.download_blob(blob).readinto(blob_obj)
            blob_obj.seek(0)
            report = self.new_report()
            report.add('raw', gzip.GzipFile(fileobj=blob_obj).read().decode())
            self.send_message(report)
            self.cache.set(blob.name, 1)  # Redis-py >= 3.0.0 does not allow True


BOT = MicrosoftAzureCollectorBot
