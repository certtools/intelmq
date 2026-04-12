<!-- comment
   SPDX-FileCopyrightText: 2026 Institute for Common Good Technology
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Connecting IntelMQ instances

The same methods can be used to connect to link up with other systems via

## Use cases

### Connecting multiple IntelMQ instances in the same organization

* Separate IntelMQ instances for different purposes
* IntelMQ instances running in different departments
* Workload management, load balancing and redundancy: Especially effective with AMQP

### Data feeds

One organization generates a data feed, processes it with IntelMQ and another organization wants to receive it with IntelMQ.

### Connections between trusted organizations

If two organizations both use IntelMQ, they can route messages to each other.

### Connections between arbitrary organizations

FIXME

Injection of

## Architecture

FIXME

### From IntelMQ outwards

FIXME

### Message broker

FIXME

It does not matter whether the message broker is technically or organizationally located in the sending or receiving side.

### Into IntelMQ

FIXME

## Security Considerations

FIXME

## Data exchange methods

FIXME

### AMQP

FIXME: Diagram

This is the most sophisticated option and gives the best security, data flow control, stability.
The downside is, that it is more complex to setup and to operate.

#### Security considerations

FIXME

#### Prerequisites

Install the Python Library `pika` for AMQP on both the sender and the receiver:
``` bash
# Debian/Ubuntu
sudo apt install python3-pika
```

#### On the receiver

##### Collector

FIXME

Module: `intelmq.bots.collectors.amqp.collector_amqp`

###### Parameters

These configuration parameters are required:

- `connection_host`: Hostname of the AMQP server.
- `connection_port` Port of the AMQP server. Defaults to 5672.
- `connection_vhost`: Virtual host to connect, on an HTTP(S) connection would be `<http:/IP/><your virtual host>`.
- `expect_intelmq_message`: `true`. FIXME This parameter denotes whether the the data is from IntelMQ or not. If true, then the data can be any Report or Event and will be passed to the next bot as is. Otherwise a new Report is created with the raw data. Defaults to false.
* `queue_name`: (optional, string) The name of the queue to fetch the data from.
* `username`: Optional username for authentication to the AMQP server.
* `password`: Optional Password
* `use_ssl`: Use of TLS for the connection. Make sure to also set the correct port. Defaults to false.

A full description and all parameters of the bot are in the [AMQP collector's documentation](../../user/bots.md#intelmq.bots.collectors.amqp.collector_amqp).

##### Parser

No parser is needed.

When configuring this via the IntelMQ Manager, it will notify you that the parser is missing. In this case, you can ignore this message.

#### On the sender

##### Output

Module: `intelmq.bots.outputs.amqptopic.output`

###### Parameters

AMQP Connection:

- `connection_host`:  Hostname of the AMQP server
- `connection_port`: Port of the AMQP server. Defaults to 5672.
- `connection_vhost`:  (optional, string) Virtual host to connect, on an http(s) connection would be `http://IP/<your virtual host>`. FIXME test
- `use_ssl`:  Set to `true` to use SSL/TLS. Also adapt the connection port
- `delivery_mode`: `2`  for persistent delivery
- `require_confirmation`: `true` to guarantee delivery

AMQP Routing:

- `exchange_durable`: `true` to make the exchange survive server restarts
- `exchange_name`:  Optional name of the exchange
- `exchange_type`: `topic`
- `routing_key`: The routing key for the AMQP Topic

If authentication is in place:

- `username`:  Optional username for authentication
- `password`:  Optional password for authentication

Message settings:

- `keep_raw_field`: `true` to keep the data original
* `message_hierarchical_output`: `false` (the default value)
* `message_with_type`: `true`
* `message_jsondict_as_string`: `true`

A full description and all parameters of the bot are in the [AMQP output's documentation](../../user/bots.md#intelmq.bots.outputs.amqptopic.output).

### ValKey / Redis

FIXME: Diagram

Open Redis ports

### API

FIXME: Diagram

#### Security considerations

FIXME

#### Prerequisites

Install the HTTP server library `tornado` (4.5.3 or later) on the receiver:
``` bash
# Debian/Ubuntu
sudo apt install python3-tornado
```

#### On the receiver

##### Collector

This bot starts a minimalist HTTP server and processes all messages that are received under the `/intelmq/push` path.

Module: `intelmq.bots.outputs.api.collector`

###### Parameters

- `port`: The port to listen on. Default: 5000
- All parameters related to UNIX sockets are not used for inter-machine communication

A full description and all parameters of the bot are in the [API collector's documentation](../../user/bots.md#intelmq.bots.collectors.api.collector).

##### Parser

No parser is needed.

When configuring this via the IntelMQ Manager, it will notify you that the parser is missing. In this case, you can ignore this message.

#### On the sender

##### Output

Module: `intelmq.bots.outputs.restapi.output`

###### Parameters

- `host`: The full URL, e.g. `https://intelmq.example.com:4433/intelmq/push`
- `auth_type`, `auth_token` and `auth_token_name`: Optional if there is an additional reverse proxy with authentication in between
- `hierarchical_output`: `false` (the default value)
- `use_json`: `true` (the default value)

A full description and all parameters of the bot are in the [API output's documentation](../../user/bots.md#intelmq.bots.outputs.restapi.output).
