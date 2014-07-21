from intelmq.lib.bot import Bot, sys

class FileBot(Bot):

    def init(self):
        self.file = open(self.parameters.file, 'a')

    def process(self):
        event = self.receive_message()
        
        if event:
            text = event.encode('utf-8')
            self.file.write(text)
            self.file.write("\n")
            self.file.flush()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = FileBot(sys.argv[1])
    bot.start()
