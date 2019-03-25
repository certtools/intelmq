# Sieve Bot

The sieve bot is used to filter and/or modify events based on a set of rules. The
rules are specified in an external configuration file and with a syntax similar
to the [Sieve language](http://sieve.info/) used for mail filtering.

Each rule defines a set of matching conditions on received events. Events can be
matched based on keys and values in the event. If the processed event matches a
rule's conditions, the corresponding actions are performed. Actions can specify
whether the event should be kept or dropped in the pipeline (filtering actions)
or if keys and values should be changed (modification actions).


## Examples

The following excerpts illustrate some of the basic features of the sieve file
format:

```
if :exists source.fqdn {
  keep  // aborts processing of subsequent rules and forwards the event.
}


if :notexists source.abuse_contact || source.abuse_contact =~ '.*@example.com' {
  drop  // aborts processing of subsequent rules and drops the event.
}

if source.ip << '192.0.0.0/24' {
    add! comment = 'bogon'
}

if classification.type == ['phishing', 'malware'] && source.fqdn =~ '.*\.(ch|li)$' {
  add! comment = 'domainabuse'
  keep
} elif classification.type == 'scanner' {
  add! comment = 'ignore'
  drop
} else {
  remove comment
}
```


## Parameters

The sieve bot takes only one parameter:
 * `file` - filesystem path of the sieve file


## Reference

### Sieve File Structure

The sieve file contains an arbitrary number of rules of the form:

```
if EXPRESSION {
    ACTIONS
} elif EXPRESSION {
    ACTIONS
} else {
    ACTIONS
}
```


###  Expressions

Each rule specifies on or more expressions to match an event based on its keys
and values. Event keys are specified as strings without quotes. String values
must be enclosed in single quotes. Numeric values can be specified as integers
or floats and are unquoted. IP addresses and network ranges (IPv4 and IPv6) are
specified with quotes. Following operators may be used to match events:

 * `:exists` and `:notexists` match if a given key exists, for example:

    ```if :exists source.fqdn { ... }```

 * `==` and `!=` match for equality of strings and numbers, for example:

   ```if feed.name != 'acme-security' || feed.accuracy == 100 { ... }```

 * `:contains` matches on substrings.

 * `=~` matches strings based on the given regex. `!~` is the inverse regex
 match.

 * Numerical comparisons are evaluated with `<`, `<=`, `>`, `>=`.

 * `<<` matches if an IP address is contained in the specified network range:

   ```if source.ip << '10.0.0.0/8' { ... }```

 * Values to match against can also be specified as list, in which case any one
 of the values will result in a match:

   ```if source.ip == ['8.8.8.8', '8.8.4.4'] { ... }```

  In this case, the event will match if it contains a key `source.ip` with
  either value `8.8.8.8` or `8.8.4.4`.


### Actions

If part of a rule matches the given conditions, the actions enclosed in `{` and
`}` are applied. By default, all events that are matched or not matched by rules
in the sieve file will be forwarded to the next bot in the pipeline, unless the
`drop` action is applied.

 * `add` adds a key value pair to the event. This action only applies if the key
 is not yet defined in the event. If the key is already defined, the action is
 ignored. Example:

   ```add comment = 'hello, world'```

 * `add!` same as above, but will force overwrite the key in the event.

 * `update` modifies an existing value for a key. Only applies if the key is
already defined. If the key is not defined in the event, this action is ignored.
Example:

   ```update feed.accuracy = 50```

 * `remove` removes a key/value from the event. Action is ignored if the key is
 not defined in the event. Example:

    ```remove extra.comments```

 * `keep` sends the message to the next bot in the pipeline
 (same as the default behaviour), and stops sieve file processing.

   ```keep```

 * `path` sets the path (named queue) the message should be sent to (implicitly
   or with the command `keep`. The named queue needs to configured in the
   pipeline, see the User Guide for more information.

   ```path 'named-queue```

 * `drop` marks the event to be dropped. The event will not be forwarded to the
 next bot in the pipeline. The sieve file processing is interrupted upon
 reaching this action. No other actions may be specified besides the `drop`
 action within `{` and `}`.


### Comments

Comments may be used in the sieve file: all characters after `//` and until the end of the line will be ignored.


## Validating a sieve file

Use the following command to validate your sieve files:
```
$ intelmq.bots.experts.sieve.validator
usage: intelmq.bots.experts.sieve.validator [-h] sievefile

Validates the syntax of sievebot files.

positional arguments:
  sievefile   Sieve file

optional arguments:
  -h, --help  show this help message and exit
```

## Installation

To use this bot, you need to install the required dependencies:
```
$ pip install -r REQUIREMENTS.txt
```
