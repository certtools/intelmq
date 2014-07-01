import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

class VXVaultHarmonizerBot(Bot):

    def process(self):
        event = self.receive_message()
        
        if event:
            event.add('feed', 'vxvault')
            event.add('feed url', 'http://vxvault.siri-urz.net/URL_List.php')
            ip_value = event.value('ip')
            event.add('source ip', ip_value)
            event.add('reported ip', ip_value)
            event.add('type', 'malware')

            self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = VXVaultHarmonizerBot(sys.argv[1])
    bot.start()
