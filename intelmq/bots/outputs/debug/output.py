from intelmq.lib.bot import Bot, sys

class DebugBot(Bot):

    def process(self):
        event = self.receive_message()
        print event.to_json()
        self.acknowledge_message()


if __name__ == "__main__":
    bot = DebugBot(sys.argv[1])
    bot.start()
