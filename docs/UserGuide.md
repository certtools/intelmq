**Table of Contents**

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Management](#management)
4. [Upgrade](#upgrade)
5. [Uninstall](#uninstall)
6. [Frequently Asked Questions](#faq)


<a name="requirements"></a>
# Requirements

The following instructions assume:
* Debian or Ubuntu Operating System


<a name="installation"></a>
# Installation

### Install Dependencies

```
apt-get install python-pip git build-essential python-dev redis-server
```


### Install IntelMQ

```
sudo su -

git clone https://github.com/certtools/intelmq.git
cd intelmq/
python setup.py install
useradd -d /opt/intelmq -U -s /bin/bash intelmq
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

<a name="management"></a>
# Management

### How it Works

Before start running all bots, user should know the system details that will help configure and start bots.

* Each bot instance starts completely independent and MUST have a 'bot id'.

* The 'bot id' is used to reference in '/opt/intelmq/etc/pipeline.conf', '/opt/intelmq/etc/startup.conf' and '/opt/intelmq/etc/runtime.conf' the specific configurations for each bot instance.

* Global configuration for intelmq is at file '/opt/intelmq/etc/system.conf'. Please note that logger in DEBUG mode will write in logs all bots parameteres configured, including passwords.


### Web interface

IntelMQ has a tool called IntelMQ Manager that gives to user a easy way to configure all pipeline with bots that your CERT needs. Click [here](https://github.com/certtools/intelmq-manager).

### Command-line interface

**Syntax:**

```
# su - intelmq

$ intelmqctl --h
usage: 
        intelmqctl --bot [start|stop|restart|status] --id=cymru-expert
        intelmqctl --botnet [start|stop|restart|status]
        intelmqctl --list [bots|queues]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --id BOT_ID           bot ID
  --type {text,json}    choose if it should return regular text or other forms
                        of output
  --log [log-level]:[number-of-lines]
  --bot [start|stop|restart|status]
  --botnet [start|stop|restart|status]
  --list [bots|queues]

description: intelmqctl is the tool to control intelmq system
```


### Utilities

#### Monitoring Logs

```
$ tail -f /opt/intelmq/var/log/*
```

#### Reset Pipeline and Cache (be careful)
```
$ redis-cli FLUSHDB
$ redis-cli FLUSHALL
```


### Additional Information

#### Perfomance Tests

Somes tests have been made with a virtual machine with the following specifications:
* CPU: 1 core dedicated from i7 processor
* Memory: 4GB
* HDD: 10GB

The entire solution didnt have any problem handling 2.000.000 queued events in memory with bots diggesting the messages.


<a name="upgrade"></a>
# Upgrade

### Stop IntelMQ and Backup

* Make sure that your IntelMQ system is completely stopped.
* Create a backup of your configurations.

```
sudo su -

cp /opt/intelmq/etc/system.conf /opt/intelmq/etc/system.conf.bk
cp /opt/intelmq/etc/startup.conf /opt/intelmq/etc/startup.conf.bk
cp /opt/intelmq/etc/runtime.conf /opt/intelmq/etc/runtime.conf.bk
cp /opt/intelmq/etc/pipeline.conf /opt/intelmq/etc/pipeline.conf.bk
```

### Upgrade

```
cd intelmq/
git pull
python setup.py install
```

### Restore Configurations

* Apply your configurations backup.

```
mv /opt/intelmq/etc/system.conf.bk /opt/intelmq/etc/system.conf
mv /opt/intelmq/etc/startup.conf.bk /opt/intelmq/etc/startup.conf
mv /opt/intelmq/etc/runtime.conf.bk /opt/intelmq/etc/runtime.conf
mv /opt/intelmq/etc/pipeline.conf.bk /opt/intelmq/etc/pipeline.conf
```


# Uninstall

<a name="uninstall"></a>
```
pip uninstall intelmq
```

<a name="faq"></a>
# Frequently Asked Questions

Consult the [FAQ](https://github.com/certtools/intelmq/blob/master/docs/FAQ.md) if you encountered any problem.
