# AMQPTopic Bot

### Output Bot that sends events to a remote AMQP Topic

See https://www.rabbitmq.com/tutorials/amqp-concepts.html for more details on amqp topic exchange.

Bot parameters: 

* connection_attempts   : The number of connection attempts to defined server, defaults to 3
* connection_heartbeat  : Heartbeat to server, in seconds, defaults to 3600
* connection_host       : Name/IP for the AMQP server, defaults to 127.0.0.1
* connection_port       : Port for the AMQP server, defaults to 5672
* connection_vhost      : Virtual host to connect, on a http(s) connection would be http:/IP/<your virtual host>
* content_type          : Content type to deliver to AMQP server, currently only supports "application/json"
* delivery_mode         : 1 - Non-persistent, 2 - Persistent. On persistent mode, messages are delivered to 'durable' queues and will be saved to disk.
* exchange_durable      : If set to True, the exchange will survive broker restart, otherwise will be a transient exchange.
* exchange_name         : The name of the exchange to use
* exchange_type         : Type of the exchange, presently only "topic" is supported
* keep_raw_field        : If set to True, the message 'raw' field will be sent
* password              : Password for authentication on your AMQP server
* require_confirmation  : If set to True, an exception will be raised if a confirmation error is received
* routing_key           : The routing key for your amqptopic
* username              : Username for authentication on your AMQP server

### Examples of usage:

* Useful to send events to a RabbitMQ exchange topic to be further processed in other platforms.

### Confirmation

If routing key or exchange name are invalid or non existent, the message is
accepted by the server but we receive no confirmation.
If parameter require_confirmation is True and no confirmation is received, an
error is raised.
