# Installation

## Install Dependencies

### Debian-based
```
apt-get install redis-server rabbitmq-server python-dateutil python-pip git
pip install geoip2 dnspython pika==0.9.13 redis pymongo
```

### RedHat-based
```
# Note: install epel repository

yum install git redis rabbitmq-server python-dateutil python-pip
pip install geoip2 dnspython pika==0.9.13 redis pymongo
```

## Install IntelMQ (need review)

```
useradd -m -d /opt/intelmq -s /bin/bash -U intelmq
passwd intelmq
git clone https://github.com/certtools/intelmq.git /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq/*
chmod -R 755 /opt/intelmq/*
echo "export PYTHONPATH=\$PYTHONPATH:/opt/intelmq/src/" >> /opt/intelmq/.profile
```

# How it Works

## System Details
Before start running all bots, user should know the system details that will help configure and start bots.

* Each bot instance starts completely independent and MUST have a 'bot_id'.

* The 'bot_id' is used to reference in 'pipeline.conf' and 'bots.conf' the specific configurations for each bot instance.

* Bots should be executed by 'intelmq' user. Use the command 'login intelmq' to login with intelmq user.


## Pipeline Configuration

**Syntax:**

```
[Pipeline]
< bot_id >  =  < source queue > | < destination queues >
```

**Example:**

```
[Pipeline]
arbor-feed   =  None               |  arbor-parser-queue
arbor-parser =  arbor-parser-queue |  output-queue
```

**Notes:** if bot doest not need a source queue, (ex.: when bot gets a report from URL) write 'None' and source queue will be ignored. The same is for destination queue.

## Bots Configuration

**Syntax:**

```
[< bot_id >]
< option_parameter > = < value >
```

**Example:**

```
[arbor-feed]
processing_interval = 3600

[logcollector]
ip = 192.168.1.243
port = 5000
```

**Notes:** The '[default]' section contains all default values for each bot and, if necessary, a 'bot_id' section can override all default options. Each option/value specified in 'bots.conf' is available in the correspondent bot using the, for example, 'self.parameters.ip' or 'self.parameters.processing_interval'.


## Run Bots

**Syntax:**

```
su - intelmq -c "python -m bots.< inputs | experts | outputs >.< bot folder >.< bot >  < bot_id >"
```

**Example:**

```
su - intelmq -c "python -m bots.inputs.arbor.feed arbor-feed"
```

**Note:** first argument for each bot is the bot ID. This ID is used to get from pipeline.conf the source and destination queues.


## Run Botnet Example

```
su - intelmq -c "bash src/tools/run-botnet-example.sh"
```

# How to write bots

...description..
**Notes**
...Explain self.parameters from bots.conf...

## Template

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
        # process message
        # ------
                
        # send message to destination queue in pipeline
        self.send_message(new_message)

        # acknowledge message received to source queue in pipeline
        self.acknowledge_message()

if __name__ == "__main__":
    bot = ExampleBot(sys.argv[1])
    bot.start()
```

## Example

<description>


# Utils

## Monitoring IntelMQ

```
watch -n 0.5 rabbitmqctl list_queues
```

## Reset Queues

```
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
```

## Reset Cache
```
redis-cli FLUSHDB
redis-cli FLUSHALL
```
