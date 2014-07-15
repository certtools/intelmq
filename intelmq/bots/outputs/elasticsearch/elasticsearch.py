# Deduplication.
# System check if it already saw a specific message

import sys
from intelmq.lib.bot import *
from intelmq.lib.utils import *
from intelmq.lib.event import *
from intelmq.lib.cache import *
import traceback
import json

# TODO: meter isto numa config
post_url = 'http://localhost:9200/indexname/document_type/'

class ElasticSearchBot(Bot):

    def process(self):
        event = self.receive_message()

        if event:
            to_send = event
            try:
                to_send = json.dumps(dict(event))
            finally:
                response = post_url(post_url, to_send)
                if response.getcode() >= 200 and response.getcode() < 300:
                    self.acknowledge_message()
                else:
                    # TODO: print error or something like it
        else:
            self.acknowledge_message()


if __name__ == "__main__":
    bot = ElasticSearchBot(sys.argv[1])
    bot.start()
