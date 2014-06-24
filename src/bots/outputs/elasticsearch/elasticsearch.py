# Deduplication.
# System check if it already saw a specific message

import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *
import traceback
import json

# TODO: meter isto numa config
post_url = 'http://localhost:9200/indexname/document_type/'

class ElasticSearchBot(Bot):

    def process(self):
        event = self.pipeline.receive()

        if event:
            to_send = event
            try:
                to_send = json.dumps(dict(event))
            finally:
                response = post_url(post_url, to_send)
                if response.getcode() >= 200 and response.getcode() < 300:
                    self.pipeline.acknowledge()
                else:
                    # TODO: print error or something like it
        else:
            self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = ElasticSearchBot(sys.argv[1])
    bot.start()
