from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

from azure.storage import BlobService

import parsedatetime
import time
import gzip
import StringIO


class DCUCollectorBot(Bot):
    # This IntelMQ collector is for getting a blob
    # from an azure account (Microsoft dcu).
    # It opens the account and
    # reads all containers, which aren't ignored.

    def process(self):
        account_name = getattr(self.parameters, "azure_account_name")
        account_key = getattr(self.parameters, "azure_account_key")

        ts_format = getattr(self.parameters, "timestamp_format", "%Y-%m-%d")
        dt_str = getattr(self.parameters, "date", None)

        # parsing the configured date string before usage
        if dt_str:
            cal = parsedatetime.Calendar()
            date = time.strftime(ts_format, cal.parse(dt_str)[0])
        else:
            date = None

        delete_flag = getattr(self.parameters, "delete", False)

        blob_service = BlobService(account_name, account_key)

        for container in blob_service.list_containers():
            container_name = container.name
            if container_name == "heartbeat":
                continue
            if date and not (container_name == "processed-" + date):
                continue

            for blob in blob_service.list_blobs(container_name):
                self.logger.info("Fetching blob %s in container %s" % (container_name, blob.name))
                data = blob_service.get_blob(container_name, blob.name)
                cs = StringIO.StringIO(data)
                report = gzip.GzipFile(fileobj=cs).read()

                self.send_message(report)

                if delete_flag:
                    self.logger.info("Deleting DCU blob \"%s\"" % blob.name)
                    blob_service.delete_blob(container_name, blob.name)
            if delete_flag:
                self.logger.info("Deleting azure container \"%s\"" % container_name)
                blob_service.delete_container(container_name)

if __name__ == "__main__":
    bot = DCUCollectorBot(sys.argv[1])
    bot.start()
