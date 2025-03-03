# Redis Pipeline (Message broker)
<!-- comment
   SPDX-FileCopyrightText: 2025 Sebastian Wagner, Intevation GmbH <sebix@sebix.at>
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

The default IntelMQ Pipeline (the message exchange between bots) is [Redis](https://redis.io/) or its OpenSource successor [Valkey](https://valkey.io/).

For AMQP (RabbitMQ) see [Using AMQP Message Broker](../beta-features.md#using-amqp-message-broker) in the section about Beta features.

## Usage of databases

You can use any redis database for any purpose. There are no hardcoded defaults or other requirements in IntelMQ.

It's also possible to use the same database for two different bots. Just make sure, that their data doesn't collide.

These are some of the usages of redis databases using the IntelMQ default values:

- 2: Pipeline (Queues)
- 4: IntelMQ Tests
- 6: Deduplicator Expert
- 7: Reverse DNS Expert
- 8: RDAP Expert, Aggregate Expert
- 10: RIPE Expert
- 12: Shadowserver Reports API Collector
- 15: SMTP Batch Output

By default, Redis/valkey have a maximum of 16 databases (0-15). In it the Redis/valkey server configuration file, this value can be increased.
While the number of maximum databases [is unlimited](https://redis.io/docs/latest/embeds/how-many-databases-software/), the practical limit is INT_32.

## Setup tips

SWAP space should be bigger or equal to your memory. See also [Hardware requirements](../hardware-requirements.md).

### Redis memory overcommitting

It is [recommended](https://redis.io/docs/latest/operate/oss_and_stack/management/admin/#linux) to enable memory overcommitting for Redis.

Run `sysctl vm.overcommit_memory=1` to set it for the current session.
To enable it permanently, create a file with `vm.overcommit_memory = 1` in `/etc/sysctl.d/intelmq.conf`.

### Maxmemory

To limit the maximum memory used by Redis and also to mitigate possible downsides of memory overcommitting, you can set a maximum memory usage in the Redis/Valkey server configuration with setting `maxmemory <bytes>`.
