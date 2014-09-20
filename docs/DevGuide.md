## System


### Main Components
Redis is used as:
* message queue for pipeline
* memcache for bots


### Code Architecture

![Code Architecture](http://s28.postimg.org/5wmak1upp/intelmq_arch_schema.png)


## How to write bots

### Template

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

### Examples

* Check [taxonomy](https://github.com/certtools/intelmq/blob/master/intelmq/bots/experts/taxonomy/taxonomy.py) expert bot
* Check [arbor](https://github.com/certtools/intelmq/blob/master/intelmq/bots/parsers/arbor/parser.py) parser bot



### TODO
* How to use send/receive/acknowledge messages methods
* some code write rules....
