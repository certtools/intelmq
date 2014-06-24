# Installation

## Install Dependencies
```
apt-get install redis-server rabbitmq-server python-dateutil python-pip git
pip install geoip2 dnspython pika==0.9.13 redis
```

## Install IntelMQ

```
useradd -m -d /opt/intelmq -s /bin/bash -U intelmq
passwd intelmq
git clone https://bitbucket.org/ahshare/intelmq.git /tmp/intelmq
cp -R /tmp/intelmq/src/* /opt/intelmq/
chown -R intelmq.intelmq /opt/intelmq/*
chmod -R 755 /opt/intelmq/*
echo "export PYTHONPATH=\$PYTHONPATH:/opt/intelmq/" >> /opt/intelmq/.profile
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
< bot_id >  =  < source queue > | < destination queue >
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
su - intelmq -c "bash run-botnet-example.sh"
```

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
