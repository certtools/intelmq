import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class ArborFeedBot(Bot):

    def process(self):
        url = "http://atlas-public.ec2.arbor.net/public/ssh_attackers"
        report = fetch_url(url, timeout = 60.0, chunk_size = 16384)
        self.send_message(force_decode(report))


if __name__ == "__main__":
    bot = ArborFeedBot(sys.argv[1])
    bot.start()
