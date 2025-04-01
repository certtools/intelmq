from collections.abc import Mapping
from datetime import datetime
from json import loads
from intelmq.lib.bot import OutputBot
from intelmq.lib.exceptions import MissingDependencyError

try:
    from opensearch import Opensearch
except ImportError:
    Opensearch = None

ROTATE_OPTIONS = {
    'never': None,
    'daily': '%Y-%m-%d',
    'weekly': '%Y-%W',
    'monthly': '%Y-%m',
    'yearly': '%Y'
}

def replace_keys(obj, key_char='.', replacement='_'):
    """Replace dots in dictionary keys with a specified character."""
    if isinstance(obj, Mapping):
        replacement_obj = {}
        for key, val in obj.items():
            replacement_key = key.replace(key_char, replacement)
            replacement_obj[replacement_key] = replace_keys(val, key_char, replacement)
        return replacement_obj
    return obj

def get_event_date(event_dict: dict) -> datetime.date:
    """Extract the event date from time.source or time.observation fields."""
    event_date = None
    for t in [event_dict.get('time.source', None), event_dict.get('time.observation', None)]:
        try:
            event_date = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S+00:00').date()
            break
        except (TypeError, ValueError):
            event_date = None
            continue
    return event_date

class OpensearchOutputBot(OutputBot):
    """Send events to an Opensearch database server."""
    opensearch_host: str = '127.0.0.1'
    opensearch_index: str = 'intelmq'
    opensearch_port: int = 9200
    flatten_fields = ['extra']
    http_password: str = None
    http_username: str = None
    http_verify_cert: bool = False
    replacement_char = None
    rotate_index: str = 'never'
    ssl_ca_certificate: str = None
    ssl_show_warnings: bool = True
    use_ssl: bool = False

    def init(self):
        """Initialize the Opensearch connection and verify index setup."""
        if Opensearch is None:
            raise MissingDependencyError('opensearch-py', version='2.0.0,<3.0.0')

        if isinstance(self.flatten_fields, str):
            self.flatten_fields = self.flatten_fields.split(',')

        self.set_request_parameters()  # Sets self.auth from parent class

        self.es = Opensearch([{'host': self.opensearch_host, 'port': self.opensearch_port}],
                             http_auth=self.auth,
                             use_ssl=self.use_ssl,
                             verify_certs=self.http_verify_cert,
                             ca_certs=self.ssl_ca_certificate,
                             ssl_show_warn=self.ssl_show_warnings)

        if self.should_rotate():
            # Fixed: Use self.opensearch_index instead of self.elastic_index
            if not self.es.indices.exists_template(name=self.opensearch_index):
                raise RuntimeError(f"No template with the name '{self.opensearch_index}' exists on the Opensearch host, "
                                   "but 'rotate_index' is set. Have you created the template?")
        else:
            if not self.es.indices.exists(self.opensearch_index):
                self.es.indices.create(index=self.opensearch_index, ignore=400)

    def process(self):
        """Process and send an event to Opensearch."""
        event = self.receive_message()
        event_dict = event.to_dict(hierarchical=False)

        for field in self.flatten_fields:
            if field in event_dict:
                val = event_dict[field]
                if isinstance(val, str):
                    try:
                        val = loads(val)
                    except ValueError:
                        pass
                if isinstance(val, Mapping):
                    for key, value in val.items():
                        event_dict[field + '_' + key] = value
                    event_dict.pop(field)

        if self.replacement_char and self.replacement_char != '.':
            event_dict = replace_keys(event_dict, replacement=self.replacement_char)

        try:
            self.es.index(index=self.get_index(event_dict, default_date=datetime.today().date()),
                          body=event_dict)
        except Exception as e:
            self.logger.error(f"Failed to index event: {e}")
            # Continue processing instead of crashing

        self.acknowledge_message()

    def should_rotate(self):
        """Check if index rotation is enabled."""
        return self.rotate_index and ROTATE_OPTIONS.get(self.rotate_index)

    def get_index(self, event_dict: dict, default_date: datetime.date = None,
                  default_string: str = "unknown-date") -> str:
        """Determine the index name based on rotation settings."""
        if self.should_rotate():
            event_date = get_event_date(event_dict) or default_date
            event_date = event_date.strftime(ROTATE_OPTIONS.get(self.rotate_index)) if event_date else default_string
            return f"{self.opensearch_index}-{event_date}"
        else:
            return self.opensearch_index

BOT = OpensearchOutputBot