import datetime
import json
from intelmq.lib.bot import CollectorBot

try:
    import cabby
except ImportError:
    cabby = None


class ESETCollectorBot(CollectorBot):
    def init(self):
        if cabby is None:
            raise ValueError('Library "cabby" not installed')

    def process(self):
        user = self.parameters.username
        passwd = self.parameters.password
        endpoint = self.parameters.endpoint
        time_delta = self.parameters.time_delta
        collection = self.parameters.collection

        domains = []
        end = datetime.datetime.now(datetime.timezone.utc)
        start = end - datetime.timedelta(seconds=time_delta)  # only fetch from up to time_delta seconds ago

        self.logger.debug('Authenticating.')

        client = cabby.create_client(endpoint, discovery_path="/taxiiservice/discovery", use_https=True)
        client.set_auth(username=user, password=passwd)

        self.logger.debug('Fetching data from ESET TAXII endpoint.')

        for item in client.poll(collection, begin_date=start, end_date=end):
            if not item.content:
                continue  # skip empty items

            data = json.loads(item.content)
            self.logger.debug('data: ' + str(data))
            self.logger.debug('domains: ' + str(domains))
            for domain in data:
                domain['_eset_feed'] = self.parameters.collection

            domains += data

        self.logger.debug('Submitting data.')

        report = self.new_report()
        report.add('raw', json.dumps(domains))
        self.send_message(report)


BOT = ESETCollectorBot
