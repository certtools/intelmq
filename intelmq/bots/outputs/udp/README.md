# UDP Output Bot

### Output Bot that sends events to a remote UDP server.

Bot parameters: 
* field_delimiter   : If the format is 'delimited' this will be added between fields
* format            : Can be 'Json' or 'delimited'. The Json format outputs the event 'as-is'. Delimited will descontruct the event and print each field separated by the field delimit. See examples bellow.
* header            : Header text to be sent in the udp datagram 
* ip                : IP address of the UDP server
* port              : PORT to connect to
* raw_field         : Can be 'keep' or 'drop'. Drop will not send the raw field in the message


### Examples of usage:

####Consider the following event:

Event = {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}

#### Parameters 1

format      : json
Header      : header example
raw_field   : keep

Output to syslog:

Apr 29 11:01:29 header example {"raw": "MjAxNi8wNC8yNV8xMTozOSxzY2hpenppbm8ub21hcmF0aG9uLmNvbS9na0NDSnVUSE0vRFBlQ1pFay9XdFZOSERLbC1tWFllRk5Iai8sODUuMjUuMTYwLjExNCxzdGF0aWMtaXAtODUtMjUtMTYwLTExNC5pbmFkZHIuaXAtcG9vbC5jb20uLEFuZ2xlciBFSywtLDg5NzI=", "source": {"asn": 8972, "ip": "85.25.160.114", "url": "http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/", "reverse_dns": "static-ip-85-25-160-114.inaddr.ip-pool.com"}, "classification": {"type": "malware"}, "event_description": {"text": "Angler EK"}, "feed": {"url": "http://www.malwaredomainlist.com/updatescsv.php", "name": "Malware Domain List", "accuracy": 100.0}, "time": {"observation": "2016-04-29T10:59:34+00:00", "source": "2016-04-25T11:39:00+00:00"}}

#### Parameters 2

field_delimiter : :::
format      : delimited
Header      : header example
raw_field   : drop

Output to syslog:

Apr 29 11:05:21 header example: ::source.asn:8972:::feed.name:Malware Domain List:::source.ip:85.25.160.114:::time.source:2016-04-25T11:39:00+00:00:::source.reverse_dns:static-ip-85-25-160-114.inaddr.ip-pool.com:::time.observation:2016-04-29T11:05:19+00:00:::classification.type:malware:::source.url:http://schizzino.omarathon.com/gkCCJuTHM/DPeCZEk/WtVNHDKl-mXYeFNHj/:::feed.accuracy:100.0:::event_description.text:Angler EK:::feed.url:http://www.malwaredomainlist.com/updatescsv.php