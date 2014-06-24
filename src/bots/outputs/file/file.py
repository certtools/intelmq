import sys
import json

from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *


class FileBot(Bot):

    def __init__(self, bot_id):
        super(FileBot, self).__init__(bot_id)
        self.file = open(self.parameters.file, 'a')

    def process(self):
        event = self.pipeline.receive()
        
        if event:
            text = unicode(event).encode('utf-8')
            self.file.write(text)
            self.file.write("\n")
            self.file.flush()
        self.pipeline.acknowledge()


if __name__ == "__main__":
    bot = FileBot(sys.argv[1])
    bot.start()
