# Sieve Bot

The sieve bot is used to filter and/or modify bots based on a set of rules. The
rules are specified in an external configuration file and with a syntax similar
to the [Sieve language](http://sieve.info/) used for mail filtering.

Each rule defines a set of matching conditions on received events. Events can be
matched based on keys and values in the event. If the processed event matches a
rule's conditions, the corresponding actions are performed. Actions can specify
whether the event should be kept or dropped in the pipeline (filtering actions)
or if keys and values should be changed (modification actions).

## Examples
The following excerpts illustrate the basic features of the sieve file format.

### Filtering based on event properties

```
if source.ip == '127.0.0.1' {
  drop
}

if :notexists source.abuse_contact || source.abuse_contact =~ '.*@example.com' {
  drop
}
```

### Modification based on event properties

```
if classification.type == ['phishing', 'malware'] && source.fqdn =~ '.*\.(ch|li)$' {
  add comment = 'domainabuse'
  modify classification.taxonomy = 'fraud'
  remove extra.comments
}
```

## Parameters
 * `file` - filesystem path the the sieve file
