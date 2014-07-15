import sys
from intelmq.lib.bot import *
from intelmq.lib.utils import *
from intelmq.lib.event import *
from intelmq.lib.cache import *

class ArborFeedBot(Bot):

    def process(self):
        url = "http://atlas-public.ec2.arbor.net/public/ssh_attackers"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(report)


if __name__ == "__main__":
    bot = ArborFeedBot(sys.argv[1])
    bot.start()
