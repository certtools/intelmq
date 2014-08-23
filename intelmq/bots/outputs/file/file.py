from intelmq.lib.bot import Bot, sys
from intelmq.lib.utils import encode

class FileBot(Bot):

    def init(self):
        self.logger.debug("Opening %s file" % self.parameters.file)
        self.file = open(self.parameters.file, 'a')
        self.logger.info("File %s is open." % self.parameters.file)

    def process(self):
        event = self.receive_message()
        
        if event:
            event_data = unicode(event)
            event_data = encode(event_data)
            self.file.write(event_data)
            self.file.write("\n")
            self.file.flush()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = FileBot(sys.argv[1])
    bot.start()
