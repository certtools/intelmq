# REST API Documentation
Currently this more of an examples doc than a full scope documentation. The API is JSON based.

## Bots Management

### `GET /bots`
Retrieves the complete bot configuration (runtime.conf).

Optional parameters:
* `/bots/{bots-group}` - only a group of bots (`collectors`,`parsers`,`experts`, `outputs`)
* `/bots/{bot-id}` - only one specified bot
* `?s` or `?short` - returns only ID's of bots

Example request:
```
GET /bots/experts?short
```
Example response (short):
```json
[
    "cymru-whois-expert",
    "deduplicator-expert",
    "taxonomy-expert",
    "url2fqdn-expert"
]
```

### `PUT /bots/{bot-id}`
Adds or modifies bot configuration for one particular bot.

Example request:
```
POST /bots/file-output


{
    "description": "File is the bot responsible to send events to a file.",
    "enabled": true,
    "group": "Output",
    "module": "intelmq.bots.outputs.file.output",
    "name": "File",
    "parameters": {
        "file": "/opt/intelmq/var/lib/bots/file-output/events.txt",
        "hierarchical_output": false,
        "single_key": null
        }
}
```

Example response:
```json
{
    "status": "OK"
}
```
  
### `DELETE /bots/{bot-id}`
Stops the bot (if running) and deletes it from configuration. Does not delete/clear it's queues!
 
### `GET /bots/status`
Returns status of bots (`running`, `stopped`, `unknown`, `disabled`).
 
Optional parameters:
* `/bots/status/{bots-group}` - only a group of bots (`collectors`,`parsers`,`experts`, `outputs`)
* `/bots/status/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "stopped",
    "deduplicator-expert": "running",
    "file-output": "disabled",
    "taxonomy-expert": "stopped",
    "url2fqdn-expert": "stopped"
}
```

### `GET /bots/logs`
Retrieves logs for all bots.

Optional parameters:
* `/bots/status/{bots-group}` - only a group of bots (`collectors`,`parsers`,`experts`, `outputs`)
* `/bots/status/{bot-id}` - only one specified bot
* `level` - starting level of log entries to retrieve (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
* `lines` - number of log entries to retrieve

Example request: 

```GET /bots/logs/deduplicator-expert?level=INFO&lines=3```

Example response:
```json
{
    "deduplicator-expert": [
        {
            "bot_id": "deduplicator-expert",
            "date": "2020-04-27T13:52:02.574000",
            "log_level": "INFO",
            "message": "Bot initialization completed.",
            "thread_id": null
        },
        {
            "bot_id": "deduplicator-expert",
            "date": "2020-04-27T13:52:03.765000",
            "log_level": "INFO",
            "message": "Forwarded 500 messages since last logging.",
            "thread_id": null
        },
        {
            "bot_id": "deduplicator-expert",
            "date": "2020-04-27T13:52:09.504000",
            "log_level": "INFO",
            "message": "Received SIGTERM.",
            "thread_id": null
        }
    ]
}
```

### `POST /bots/start`
Starts all enabled bots. Returns bot starting status (`starting`, `disabled`, `failed`).

Optional parameters:
* `/bots/start/{bots-group}` - starts only a group of bots
* `/bots/start/{bot-id}` - starts only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "starting",
    "deduplicator-expert": "starting",
    "file-output": "disabled",
    "taxonomy-expert": "starting",
    "url2fqdn-expert": "failed"
}
```

### `POST /bots/stop`
Stops all running bots. Returns bot stopping status (`stopping`, `failed`).

Optional parameters:
* `/bots/stop/{bots-group}` - reloads only a group of bots
* `/bots/stop/{bot-id}` - reloads only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "stopping",
    "deduplicator-expert": "stopping",
    "taxonomy-expert": "failed"
}
```

### `POST /bots/reload`
Reloads the configuration of all running bots. Returns bot reloading status (`reloading`, `failed`).

Optional parameters:
* `/bots/reload/{bots-group}` - only a group of bots
* `/bots/reload/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "reloading",
    "deduplicator-expert": "reloading",
    "taxonomy-expert": "failed"
}
```

### `POST /bots/restart`
Restarts all running bots. Bots are not restarted if they failed to stop. Returns bot starting status  (`starting`, `failed`) for successfully stopped bots.

Optional parameters:
* `/bots/restart/{bots-group}` - only a group of bots
* `/bots/restart/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "starting",
    "deduplicator-expert": "starting",
    "taxonomy-expert": "failed"
}
```

### `POST /bots/enable`
Sets the bots configuration to enabled. Returns a list of all enabled bots by this call. Does not start the bots!

Optional parameters:
* `/bots/enable/{bots-group}` - only a group of bots
* `/bots/enable/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "enabled",
    "deduplicator-expert": "enabled",
    "taxonomy-expert": "enabled",
    "url2fqdn-expert": "enabled"
}
```

### `POST /bots/disable`
Sets the bots configuration to disabled. Returns a list of all disabled bots by this call. Does not stop the bots!

Optional parameters:
* `/bots/disable/{bots-group}` - only a group of bots
* `/bots/disable/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": "disabled",
    "deduplicator-expert": "disabled",
    "taxonomy-expert": "disabled",
    "url2fqdn-expert": "disabled"
}
```

### `GET /bots/queues`
Returns queue names for bots.

Optional parameters:
* `/bots/queues/{bots-group}` - only a group of bots
* `/bots/queues/{bot-id}` - only one specified bot

Example response:
```json
{
    "feodo-tracker-browse-collector": {
        "destination-queues": [
            "feodo-tracker-browse-parser-queue"
        ]
    },
    "malc0de-windows-format-collector": {
        "destination-queues": [
            "malc0de-parser-queue"
        ]
    }
}
```

### `GET /bots/queues/status`
Returns status of queues for bots.

Optional parameters:
* `/bots/queues/status/{bots-group}` - only a group of bots
* `/bots/queues/status/{bot-id}` - only one specified bot

Example response:
```json
{
    "cymru-whois-expert": {
        "destination_queues": [
            {
                "file-output-queue": 281
            }
        ],
        "internal_queue": 1,
        "source_queue": {
            "cymru-whois-expert-queue": 151
        }
    }
}
```

### `PUT /bots/queues/{bot-id}`
Inserts/updates new queues configuration for a bot. Returns status.

Example response:
```json
{
    "status": "OK"
}
```

### `DELETE /bots/queues/{bot-id}`
Deletes queues configuration for a bot. Does not delete/clear queue in the message broker!

```json
{
    "status": "OK"
}
```

## Queues Management

### `GET /queues`
Returns an array of all queues names (not of type `internal`).

Optional parameters:
* `/queues/status/{queue-type}` - only a certain type of queues (`internal`, `source`)
* `/queues/status/{queue-id}` - only one specified queue

Example response:
```json
[
    "cymru-whois-expert-queue",
    "deduplicator-expert-queue",
    "feodo-tracker-browse-parser-queue",
    "file-output-queue",
    "gethostbyname-1-expert-queue",
    "gethostbyname-2-expert-queue",
    "malc0de-parser-queue",
    "malware-domain-list-parser-queue",
    "spamhaus-drop-parser-queue",
    "taxonomy-expert-queue",
    "url2fqdn-expert-queue"
]
```

### `GET /queues/status`
Returns a status of source queues of all bots.

Optional parameters:
* `/queues/status/{queue-type}` - only a certain type of queues (`internal`, `source`)
* `/queues/status/{queue-id}` - only one specified queue
 
Example reponse:
```json
{
    "cymru-whois-expert-queue": 151,
    "deduplicator-expert-queue": 0,
    "feodo-tracker-browse-parser-queue": 1,
    "file-output-queue": 281,
    "gethostbyname-1-expert-queue": 395,
    "gethostbyname-2-expert-queue": 0,
    "malc0de-parser-queue": 0,
    "malware-domain-list-parser-queue": 0,
    "spamhaus-drop-parser-queue": 0,
    "taxonomy-expert-queue": 0,
    "url2fqdn-expert-queue": 0
}
```

### `POST /queues/clear`
Clears the specified queues. Returns a list of cleared queues.

Optional parameters:
* `/queues/status/{queue-type}` - only a certain type of queues (`internal`, `source`)
* `/queues/status/{queue-id}` - only one specified queue

Example request:
```
POST /queues/clear/feodo-tracker-browse-parser-queue
```

Example response:
```json
[
    "feodo-tracker-browse-parser-queue"
]
```

