**Table of Contents**

1. [System](#system)
2. [Create Bot](#create)

<a name="system"></a>
## System


#### Main Components
Redis is used as:
* message queue for pipeline
* memcache for bots


#### Code Architecture

![Code Architecture](http://s28.postimg.org/5wmak1upp/intelmq_arch_schema.png)


<a name="create"></a>
## Create New Bot

#### Template

```
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event
from intelmq.bots import utils

class ExampleBot(Bot):

    def process(self):
        
        # get message from source queue in pipeline
        message = self.receive_message()

        # ------
        # write the code here to process the message
        # ------
                
        # send message to destination queue in pipeline
        self.send_message(new_message)

        # acknowledge message received to source queue in pipeline
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ExampleBot(sys.argv[1])
    bot.start()
```

** Examples **

* Check [taxonomy](https://github.com/certtools/intelmq/blob/master/intelmq/bots/experts/taxonomy/taxonomy.py) expert bot
* Check [arbor](https://github.com/certtools/intelmq/blob/master/intelmq/bots/parsers/arbor/parser.py) parser bot

#### Configure IntelMQ

In the end, the new information about the new bot should be added to BOTS file located at intelmq/intelmq/bots on repository.
