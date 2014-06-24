# System

## Goals

* reduce the complexity of system administration
* reduce the complexity of writing new bots for new data feeds
* reduce the probability of events lost in all process (even system down time)
* provide easy communication with other systems via API
* use and improve the existing Data Harmonization Ontology
* use the existing AbuseHelper Event-like syntax: event.add("domain", "example.com")
* use JSON format for all messages
* use messages tags: report, abuse-event, pastebin, tweet

## Main Components
* RabbitMQ as message queue for pipeline
* Redis as memcache for bots

## Architecture

![Architecture](https://bitbucket.org/ahshare/intelmq/downloads/poc_arch.jpg)

## System Details

* Configuration - <details>
* How to dedup using Redis TTL - <details>
* Experts using Redis as a cache and TTL - <details>
* RabbitMQ Queues - <details>

## How to install

Check INSTALLATION.md file.


## How to write a bots

<description>


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
		message = self.pipeline.receive()

        # ------
        # process message
        # ------
		
		# send message to destination queue in pipeline
		self.pipeline.send(new_message)

		# acknowledge message received to source queue in pipeline
        self.pipeline.acknowledge()

if __name__ == "__main__":
    bot = ExampleBot(sys.argv[1])
    bot.start()
```

### Example

<description>

# Incident Handling Automation Project

* ** URL:** http://www.enisa.europa.eu/activities/cert/support/incident-handling-automation
* ** Mailing-list:** ihap@lists.trusted-introducer.org
* ** Data Harmonization Ontology:** https://bitbucket.org/clarifiednetworks/abusehelper/wiki/Data%20Harmonization%20Ontology

