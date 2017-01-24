# UDP Output Bot

### Output Bot that sends events to a remote UDP server.

*Bot parameters:* 
* field_delimiter   : If the format is 'delimited' this will be added between fields.
* format            : Can be 'Json' or 'delimited'. The Json format outputs the event 'as-is'. Delimited will descontruct the event and print each field:value separated by the field delimit. See examples bellow.
* header            : Header text to be sent in the udp datagram. 
* ip                : IP address of the UDP server
* port              : PORT to connect to.
* keep_raw_field    : Can be 'True' or 'False'. False will not send the raw field in the message.

### Examples of usage:

#####Consider the following event:
*Event = {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}*
##### With the following Parameters:
---

* field_delimiter   : |
* format            : json
* Header            : header example
* keep_raw_field    : true
* ip                : 127.0.0.1
* port              : 514

**Line in syslog:**

`
Apr 29 11:01:29 header example {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}
`
##### With the following Parameters:
---

* field_delimiter   : |
* format            : delimited
* Header            : IntelMQ-event
* keep_raw_field    : false
* ip                : 127.0.0.1
* port              : 514

**Line in syslog:**

`
Apr 29 11:17:47 localhost IntelMQ-event|source.ip: 85.25.160.114|time.source:2016-04-25T11:39:00+00:00|feed.url:http://www.malwaredomainlist.com/updatescsv.php|time.observation:2016-04-29T11:17:44+00:00|source.reverse_dns:static-ip-85-25-160-114.inaddr.ip-pool.com|feed.name:Malware Domain List|event_description.text:Angler EK|source.url:http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/|source.asn:8972|classification.type:malware|feed.accuracy:100.0
`
