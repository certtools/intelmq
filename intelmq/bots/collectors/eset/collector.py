import datetime
import json
from intelmq.lib.bot import CollectorBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    import cabby
except ImportError:
    cabby = None


class ESETCollectorBot(CollectorBot):
    def init(self):
        if cabby is None:
            raise MissingDependencyError('cabby')
        self.user = self.parameters.username
        self.passwd = self.parameters.password
        self.endpoint = self.parameters.endpoint
        self.time_delta = int(self.parameters.time_delta)
        self.collection = self.parameters.collection

    def process(self):
        domains = []
        end = datetime.datetime.now(datetime.timezone.utc)
        start = end - datetime.timedelta(seconds=self.time_delta)

        self.logger.debug('Fetching data back to %s.', start.isoformat(timespec='seconds'))

        self.logger.debug('Authenticating.')

        client = cabby.create_client(self.endpoint, discovery_path="/taxiiservice/discovery", use_https=True)
        client.set_auth(username=self.user, password=self.passwd)

        self.logger.debug('Authentication succeeded. Polling data from ESET TAXII endpoint.')

        for item in client.poll(self.collection, begin_date=start, end_date=end):
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
        report.add("feed.url", "https://%s/taxiiservice/discovery" % self.endpoint)
        report.add('raw', json.dumps(domains))
        self.send_message(report)


BOT = ESETCollectorBot
