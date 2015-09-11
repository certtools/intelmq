Bots documentation
==================

Experts
-------

| name | IPv6 | lookup | public | cache: redis db | information | comment |
|:-----|:-----|:---------|:--------|
| abusix | n | ? | y | 5 | ip to abuse contact | ipv6 implementation missing |
| asn-lookup | n | local db | y | - | ip to asn | [IPv6 bugreport](https://github.com/hadiasghari/pyasn/issues/14)
| certat-contact | n | https | y | - | asn to cert abuse contact, cc |
| cymru-whois | y | cymru dns | y | 6 | ip to geolocation, asn, network |
| deduplicator | y | redis cache | y | 7 | - | not tested |
| filter | y | - | y | - | drops event | not tested |
| maxmind-geoip | ? | local db | n | - | ip to geolocation ? | not stable |
| modify | - | config | y | - | arbitrary |
| reverse-dns | n | dns | y | 8 | ip to domain | ipv6 implementation missing |
| ripencc-abuse-contact | y | ? | y | 9 | ip to abuse contact |
| taxonomy | - | - | y | - | classification type to taxonomy |
| tor-nodes | n | local db | y | - | if ip is tor node |


### Modify

The modify expert bot allows you to change arbitrary field values of events just using a configuration file. Thus it is possible to adapt certain values or adding new ones only by changing JSON-files without touching the code of many other bots.

The configuration is called `modify.conf` and looks like this:

```json
{
"Spamhaus Cert": {
    "__default": [{
            "feed.name": "^Spamhaus Cert$"
        }, {
            "classification.identifier": "{msg[malware.name]}"
        }],
    "conficker": [{
            "malware.name": "^conficker(ab)?$"
        }, {
            "classification.identifier": "conficker"
        }],
    "urlzone": [{
            "malware.name": "^urlzone2?$"
        }, {
            "classification.identifier": "urlzone"
        }]
	}
}
```

The dictionary in the first level holds sections, here called `Spamhaus Cert` to group the rulessets and for easier navigation. It holds another dictionary of rules, consisting of *conditions* and *actions*. The first matching rule is used. Conditions and actions are again dictionaries holding the field names of harmonization and have regex-expressions to existing values (condition) or new values (action). The rule conditions are merged with the default condition and the default action is applied if no rule matches.

#### Examples

We have an event with `feed.name = Spamhaus Cert` and `malware.name = confickerab`. The expert loops over all sections in the file and enters section `Spamhaus Cert`. First, the default condition is checked, it matches! Ok, going on. Otherwise the expert would have continued to the next section. Now, iteration through the rules, the first is rule `conficker`. We combine the conditions of this rule with the default conditions, and both rules match! So we can apply the action, here `classification.identifier` is set to `conficker`, the trivial name.

Assume we have an event with `feed.name = Spamhaus Cert` and `malware.name = feodo`. The default condition matches, but no others. So the default action is applied. The value for `classification.identifier` is `{msg[malware.name]}`, this is [standard Python string format syntax](https://docs.python.org/3/library/string.html#formatspec). Thus you can use any value from the processed event, which is available as `msg`.
