# Deduplicator

Bot responsible for ignore duplicated messages. The bot can be configured to perform deduplication just looking to specific fields on the message.

## Parameters

### Parameters for connecting to cache
* `redis_cache_host` - redis host to connect (e.g. `127.0.0.1`)
* `redis_cache_db` - redis db to connect (e.g. `6`)
* `redis_cache_ttl` - ttl (in seconds) for each entry inserted on cache (e.g. `86400`)
* `redis_cache_password` - password to access redis (by default is None)

### Parameters for "fine-grained" deduplication

* `filter_type`: type of the filtering which can be "blacklist" or "whitelist". The filter type will be used to define how Deduplicator bot will interpret the the parameter `filter_keys` in order to decide whether an event has already been seen or not, i.e., duplicated event or a completely new event.
  * "whitelist" configuration: only the keys listed in `filter_keys` will be considered to verify if an event is duplicated or not.
  * "blacklist" configuration: all keys except those in `filter_keys` will be considered to verify if an event is duplicated or not.
* `filter_keys`: string with multiple keys separated by comma. Please note that `time.observation` key will not be considered even if defined, because the system always ignore that key.


### Parameters Configuration Example

#### Example 1

The bot with this configuration will detect duplication only based on `source.ip` and `destination.ip` keys.

```
"parameters": {
    "redis_cache_db": 6,
    "redis_cache_host": "127.0.0.1",
    "redis_cache_password": null,
    "redis_cache_port": 6379,
    "redis_cache_ttl": 86400,
    "filter_type": "whitelist",
    "filter_keys": "source.ip,destination.ip",
}
```

#### Example 2

The bot with this configuration will detect duplication based on all keys, except `source.ip` and `destination.ip` keys.

```
"parameters": {
    "redis_cache_db": 6,
    "redis_cache_host": "127.0.0.1",
    "redis_cache_password": null,
    "redis_cache_port": 6379,
    "redis_cache_ttl": 86400,
    "filter_type": "blacklist",
    "filter_keys": "source.ip,destination.ip",
}
```
