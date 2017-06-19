# -*- coding: utf-8 -*-
"""
Uses the azure.storage module from https://pypi.python.org/pypi/azure-storage/0.33.0
Tested with 0.33, probably works with >0.30 too.
"""
import datetime
import gzip
import io
import urllib.parse

import pytz

from intelmq.lib.bot import CollectorBot

try:
    import azure.storage
except ImportError:
    azure = None  # noqa


class MicrosoftAzureCollectorBot(CollectorBot):
    def init(self):
        if azure is None:
            raise ValueError('Could not import azure.storage. Please install it.')

        if hasattr(self.parameters, 'https_proxy'):
            parsed = urllib.parse.urlparse(self.parameters.https_proxy)
            self.proxy = {'host': parsed.hostname, 'port': parsed.port,
                          'user': parsed.username, 'password': parsed.password}
        else:
            self.proxy = None

    def process(self):
        storage_client = azure.storage.CloudStorageAccount(self.parameters.account_name,
                                                           self.parameters.account_key)
        blob_service = storage_client.create_block_blob_service()
        if self.proxy:
            blob_service.set_proxy(**self.proxy)
        containers = blob_service.list_containers()
        for container in containers:
            self.logger.info('Processing Container %r.', container.name)
            if container.name == 'heartbeat':
                if self.parameters.delete:
                    blob_service.delete_container(container.name)
                continue
            time_container_fetch = datetime.datetime.now(pytz.timezone('UTC'))
            for blob in blob_service.list_blobs(container.name):
                self.logger.debug('Processing blob %r.', blob.name)
                time_blob_fetch = datetime.datetime.now(pytz.timezone('UTC'))
                blob_obj = io.BytesIO(blob_service.get_blob_to_bytes(container.name,
                                                                     blob.name).content)
                unzipped = gzip.GzipFile(fileobj=blob_obj).read().decode()
                report = self.new_report()
                report.add('raw', unzipped)
                self.send_message(report)
                if self.parameters.delete:
                    blob_service.delete_blob(container.name, blob.name,
                                             if_unmodified_since=time_blob_fetch)
            if self.parameters.delete:
                blob_service.delete_container(container.name,
                                              if_unmodified_since=time_container_fetch)


BOT = MicrosoftAzureCollectorBot
