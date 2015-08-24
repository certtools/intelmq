import sys

from intelmq.lib.bot import Bot


class FilterBot(Bot):

    def init(self):
        if not self.parameters.filter_key:
            self.logger.warn("No filter_key parameter found.")
            self.stop()
        elif not self.parameters.filter_value:
            self.logger.warn("No filter_value parameter found.")
            self.stop()
        elif not (self.parameters.filter_action == "drop" or
                  self.parameters.filter_action == "keep"):
            self.logger.warn("No filter_action parameter found.")
            self.stop()

    def process(self):
        event = self.receive_message()

        if self.parameters.filter_action == "drop":
            if (event.contains(self.parameters.filter_key) and
                    event.value(self.parameters.filter_key) ==
                    self.parameters.filter_value):
                self.acknowledge_message()
            else:
                self.send_message(event)
                self.acknowledge_message()

        if self.parameters.filter_action == "keep":
            if (event.contains(self.parameters.filter_key) and
                    event.value(self.parameters.filter_key) ==
                    self.parameters.filter_value):
                self.send_message(event)
                self.acknowledge_message()
            else:
                self.acknowledge_message()

        self.acknowledge_message()

if __name__ == "__main__":
    bot = FilterBot(sys.argv[1])
    bot.start()
