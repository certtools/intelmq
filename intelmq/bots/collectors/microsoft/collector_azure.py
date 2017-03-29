# -*- coding: utf-8 -*-
"""
Uses the azure.storage module from https://pypi.python.org/pypi/azure-storage/0.33.0
Tested with 0.33, probably works with >0.30 too.
"""
import datetime
import gzip
import io

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

    def process(self):
        storage_client = azure.storage.CloudStorageAccount(self.parameters.account_name,
                                                           self.parameters.account_key)
        blob_service = storage_client.create_block_blob_service()
        containers = blob_service.list_containers()
        for container in containers:
            self.logger.info('Processing Container %r.' % container.name)
            if container.name == 'heartbeat':
                if self.parameters.delete:
                        blob_service.delete_container(container.name)
                continue
            time_container_fetch = datetime.datetime.now(pytz.timezone('UTC'))
            for blob in blob_service.list_blobs(container.name):
                self.logger.debug('Processing blob %r.' % blob.name)
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
