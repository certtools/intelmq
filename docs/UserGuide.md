# Installation

## Install Dependencies

### Debian-based
```
apt-get install python-pip git
apt-get install build-essential python-dev
apt-get install redis-server rabbitmq-server
```

### RedHat-based

**Note:** Install EPEL Repository
```
yum install git
yum install gcc python-devel
yum install centos-release-SCL
yum install rabbitmq-server python27
scl enable python27 bash
easy_install pip
echo "scl enable python27 bash" >> /opt/intelmq/.bashrc

rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
yum --enablerepo=remi,remi-test install redis

sudo nano /etc/sysctl.conf
     vm.overcommit_memory=1
 
sysctl -w fs.file-max=100000

chkconfig --add redis
chkconfig --level 345 redis on
service redis start/stop/restart
```
Source: https://gist.github.com/nghuuphuoc/7801123

## Install IntelMQ

```
pip install git+https://<your_user_account>@github.com/certtools/intelmq.git
```


## How it Works

Before start running all bots, user should know the system details that will help configure and start bots.

* Each bot instance starts completely independent and MUST have a 'bot id'.

* The 'bot id' is used to reference in '/etc/intelmq/pipeline.conf' and '/etc/intelmq/bots.conf' the specific configurations for each bot instance.


### System Configuration

* Global configuration for intelmq is at file '/etc/intelmq/system.conf'. Please note that logger in DEBUG will write in logs the bots password when its provided by parameters in 'bots.conf' file.

### Pipeline Configuration

**Location:** /etc/intelmq/pipeline.conf

**Syntax:**
```
[Pipeline]
< bot id >  =  < source queue > | < destination queues >
```

**Example:**
```
[Pipeline]
arbor-collector =                  |  arbor-parser-queue
arbor-parser =  arbor-parser-queue |  output-queue
```

**Notes:** if bot doest not need a source queue, (e.g.: when bot gets a report from URL) do not write anything and bot will ignore the source queue. The same is for destination queue. The system also support multiple destination queues in [fanout](https://www.rabbitmq.com/tutorials/amqp-concepts.html) mode. To use this functionality see the following example:

**Example:**
```
[Pipeline]
arbor-collector =                  |  arbor-parser-queue
arbor-parser =  arbor-parser-queue |  database-queue, file-queue
```


### Bots Configuration

**Location:** /etc/intelmq/bots.conf

**Syntax:**
```
[< bot id >]
< option_parameter > = < value >
```

**Example:**
```
[default]
processing_interval = 0
cache_host = 127.0.0.1
cache_port = 6379
cache_id = 10
cache_ttl = 86400

[arbor-collector]
processing_interval = 3600
url = http://atlas-public.ec2.arbor.net/public/ssh_attackers

[logcollector]
ip = 192.168.1.243
port = 5000
```

**Notes:** The '[default]' section contains all default values for each bot and, if necessary, a 'bot id' section can override all default options. Each option/value specified in 'bots.conf' is available in the correspondent bot using, for example, 'self.parameters.ip' or 'self.parameters.processing_interval'.

**Example:** search for self.parameters.database in GeoIPExpertBot example to see how it works.

File: /usr/local/lib/python2.7/dist-packages/intelmq-*/intelmq/bots/experts/geoip/geoip.py
```
class GeoIPExpertBot(Bot):

    def init(self):
        try:
            self.database = geoip2.database.Reader(self.parameters.database)
        except IOError:
            self.logger.error("GeoIP Database does not exist or could not be accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/geoip/README' and follow the procedure")
            self.stop()
```

File: /etc/intelmq/bots.conf
```
[geoip-expert]
database = /var/lib/intelmq/geoip/GeoLite2-City.mmdb
```



### Run Bots

**Syntax:**

```
$ nohup python -m intelmq.bots.< collectors | parsers | experts | outputs >.< bot folder >.< bot >  < bot id > &
```

**Examples:**

```
$ nohup python -m intelmq.bots.collectors.url.collector arbor-collector &

$ nohup python -m intelmq.bots.parsers.arbor.parser arbor-parser &

$ nohup python -m intelmq.bots.experts.geoip.geoip geoip-expert &

$ nohup python -m intelmq.bots.outputs.file.file archive &
```

**Note 1:** the 'python -m' command means python package. Since intelmq is a python package, it will always accessible by python env path and thats the reason to use 'intelmq.bots.outputs.file.file', which means <python path>/intelmq/bots/outputs/file/file.py.

**Note 2:** first argument for each bot is the bot ID. This ID is used to get from 'pipeline.conf' the source and destination queues. In 'file' bot example, the bot ID is 'archive'.

### Run Botnet Example

```
$ run-intelmq-botnet
```

**Location:** /usr/local/bin/run-intelmq-botnet

## Utilities

### IntelMQHelper

IntelMQ Helper is a simple tool that will help you choose and configure bots.

```
$ intelmqhelper

Bot Types:
  [1] Collector
  [2] Expert
  [3] Output
  [4] Parser

Choose option: 2

Bots List:
  [1] Cymru
  [2] Deduplicator
  [3] GeoIP
  [4] Sanitizer
  [5] Taxonomy

Choose option: 3


Information
===========

Bot Name: GeoIP
Description: GeoIP (MaxMind) is the bot responsible to add geolocation information to the events (Country, City, Longitude, Latitude, etc..)

Module: intelmq.bots.experts.geoip.geoip

Bot Configuration Required ('/etc/intelmq/bots.conf'):
----------------------------------
[geoip-expert]
processing_interval = 0
database = /var/lib/intelmq/geoip/GeoLite2-City.mmdb
----------------------------------

```

### Monitoring IntelMQ

```
$ watch -n 0.5 rabbitmqctl list_queues
```

```
$ tail -f /var/log/intelmq/*
```

### Reset Queues

```
$ rabbitmqctl stop_app
$ rabbitmqctl reset
$ rabbitmqctl start_app
```

### Reset Cache
```
$ redis-cli FLUSHDB
$ redis-cli FLUSHALL
```


## Additional Information

### Perfomance Tests

Somes tests have been made with a virtual machine with the following specifications:
* CPU: 1 core dedicated from i7 processor
* Memory: 4GB
* HDD: 10GB

The entire solution didnt have any problem handling 2.000.000 queued events in memory with bots diggesting the messages.



