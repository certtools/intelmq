## How to write bots

### Template

```
import sys
from lib.bot import *
from lib.utils import *
from lib.event import *
from lib.cache import *

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

### Example

Check [taxonomy](https://github.com/certtools/intelmq/blob/master/src/bots/experts/taxonomy/taxonomy.py) expert bot



### TODO
* How to use send/receive/acknowledge messages methods
* some code write rules....
