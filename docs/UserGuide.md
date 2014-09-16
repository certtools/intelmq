# Installation

## Install Dependencies

### Debian-based
```
apt-get install python-pip git
apt-get install build-essential python-dev
apt-get install redis-server
```

### RedHat-based

**Note:** Install EPEL Repository
```
yum install git
yum install gcc python-devel
yum install centos-release-SCL
yum install python27
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

## Update IntelMQ

* Make sure that your IntelMQ system is completely stopped.
* Create a backup of your configurations.

```
cp /etc/intelmq/system.conf /etc/intelmq/system.conf.bk
cp /etc/intelmq/startup.conf /etc/intelmq/startup.conf.bk
cp /etc/intelmq/runtime.conf /etc/intelmq/runtime.conf.bk
cp /etc/intelmq/pipeline.conf /etc/intelmq/pipeline.conf.bk
```

* Upgrade IntelMQ

```
pip install --upgrade git+https://<your_user_account>@github.com/certtools/intelmq.git
```

* Apply your configurations backup.

```
mv /etc/intelmq/system.conf.bk /etc/intelmq/system.conf
mv /etc/intelmq/startup.conf.bk /etc/intelmq/startup.conf
mv /etc/intelmq/runtime.conf.bk /etc/intelmq/runtime.conf
mv /etc/intelmq/pipeline.conf.bk /etc/intelmq/pipeline.conf
```


## How it Works

Before start running all bots, user should know the system details that will help configure and start bots.

* Each bot instance starts completely independent and MUST have a 'bot id'.

* The 'bot id' is used to reference in '/etc/intelmq/pipeline.conf', '/etc/intelmq/startup.conf' and '/etc/intelmq/runtime.conf' the specific configurations for each bot instance.

* Global configuration for intelmq is at file '/etc/intelmq/system.conf'. Please note that logger in DEBUG will write in logs all bots parameteres configured, including passwords.

## Management

#### Web interface

IntelMQ has a tool called IntelMQ Manager that gives to user a easy way to configure all pipeline with bots that your CERT needs. Click [here](https://github.com/certtools/intelmq-manager).

#### Command-line interface

**Syntax:**

```
# intelmqctl --h
usage: 
        intelmqctl --bot [start|stop|restart|status] --id=cymru-expert
        intelmqctl --botnet [start|stop|restart|status]
        intelmqctl --list [bots]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --id BOT_ID           bot ID
  --bot [start|stop|restart|status]
  --botnet [start|stop|restart|status]
  --list [bots]

description: intelmqctl is the tool to control intelmq system

```

**Example:**

```
# intelmqctl --list bots
# intelmqctl --botnet start
# intelmqctl --botnet status
```


## Utilities

### Monitoring Logs

```
$ tail -f /var/log/intelmq/*
```

### Monitoring Pipeline

```
$ watch -n 0.5 rabbitmqctl list_queues
```

### Reset Pipeline Queues

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



