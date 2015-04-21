from intelmq.lib.bot import Bot, sys
from intelmq.lib.cache import Cache
from intelmq.lib.message import Event


class CustomFilterBot(Bot):

    def meet_condition(self):
        for rule in self.rules.filter:
            if self.rules[rule] != self.parameters.xxparametr[rule]:
                return False
        return True

    def init(self):
        # load filter rules from json
        with open('rules.json') as data_file:
            self.rules = json.load(data_file)
        pass

    def process(self):
        message = self.receive_message()

        conforming = self.meet_condition()
        if self.rules.type == "exclude" and conforming:
            # zahodit radek
            pass
        elif self.rules.type == "include" and conforming:
            # propustit radek
            pass
        else:
            raise ValueError("Unknown filter type %s." % self.rules.type)

        # self.send_message(message)
	# self.acknowledge_message()


if __name__ == "__main__":    
    bot = CustomFilterBot(sys.argv[1])
    bot.start()