**Table of Contents**

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Upgrade](#upgrade)
4. [Management](#management)
5. [Frequently Asked Questions](#faq)


<a name="requirements"></a>
# Requirements

The following instructions assume:
* Debian or Ubuntu Operatin System


<a name="installation"></a>
# Installation

### Install Dependencies

```
apt-get install python-pip git
apt-get install build-essential python-dev
apt-get install redis-server
```


### Install IntelMQ

```
useradd -M -U -s /bin/bash intelmq
pip install git+https://<your_user_account>@github.com/certtools/intelmq.git

chmod -R 770 /etc/intelmq/
chmod -R 700 /var/run/intelmq
chmod -R 700 /var/lib/intelmq
chmod -R 700 /usr/local/bin/intelmqctl
chmod -R 700 /var/log/intelmq

chown -R intelmq.intelmq /etc/intelmq/
chown -R intelmq.intelmq /var/run/intelmq
chown -R intelmq.intelmq /var/lib/intelmq
chown -R intelmq.intelmq /usr/local/bin/intelmqctl
chown -R intelmq.intelmq /var/log/intelmq

```

<a name="upgrade"></a>
# Upgrade

### Stop IntelMQ and Backup

* Make sure that your IntelMQ system is completely stopped.
* Create a backup of your configurations.

```
cp /etc/intelmq/system.conf /etc/intelmq/system.conf.bk
cp /etc/intelmq/startup.conf /etc/intelmq/startup.conf.bk
cp /etc/intelmq/runtime.conf /etc/intelmq/runtime.conf.bk
cp /etc/intelmq/pipeline.conf /etc/intelmq/pipeline.conf.bk
```

### Upgrade

```
pip install --upgrade git+https://<your_user_account>@github.com/certtools/intelmq.git
```

### Restore Configurations

* Apply your configurations backup.

```
mv /etc/intelmq/system.conf.bk /etc/intelmq/system.conf
mv /etc/intelmq/startup.conf.bk /etc/intelmq/startup.conf
mv /etc/intelmq/runtime.conf.bk /etc/intelmq/runtime.conf
mv /etc/intelmq/pipeline.conf.bk /etc/intelmq/pipeline.conf
```

<a name="management"></a>
# Management

### How it Works

Before start running all bots, user should know the system details that will help configure and start bots.

* Each bot instance starts completely independent and MUST have a 'bot id'.

* The 'bot id' is used to reference in '/etc/intelmq/pipeline.conf', '/etc/intelmq/startup.conf' and '/etc/intelmq/runtime.conf' the specific configurations for each bot instance.

* Global configuration for intelmq is at file '/etc/intelmq/system.conf'. Please note that logger in DEBUG will write in logs all bots parameteres configured, including passwords.


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
$ tail -f /var/log/intelmq/*
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



<a name="faq"></a>
# FAQ

Consult the [FAQ](https://github.com/certtools/intelmq/blob/master/docs/FAQ.md) if you encountered any problem.
