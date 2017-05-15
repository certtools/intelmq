# Redis Bot

### Output Bot that sends events to a remote Redis server/queue.

Bot parameters: 
* redis_db          : remote server database, e.g.: 2
* redis_password    : remote server password
* redis_queue       : remote server list (queue), e.g.: "remote-server-queue"
* redis_server_ip   : remote server IP address, e.g.: 127.0.0.1
* redis_server_port : remote server Port, e.g: 6379
* redis_timeout     : Connection timeout, in msecs, e.g.: 50000


### Examples of usage:

* Can be used to send events to be processed in another system. E.g.: send events to Logstash.

* In a multi tenant installation can be used to send events to external/remote IntelMQ instance. Any expert bot queue can receive the events.

* In a complex configuration can be used to create logical sets in IntelMQ-Manager. 
