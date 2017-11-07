A bot to filter specific events from the pipeline. See valid fields at https://github.com/certtools/intelmq/blob/master/docs/Harmonization-fields.md

With the filter bot, one should be able to define filters such as:
 - throw away all events for specific ASN or CIDR
 - pass just events with particular CC or Taxonomy
 - or even a combination of multiple like throw away all "Intrusion" events for CIDR 123.34.5.0/24

Processing of the filter configuration is as follows:
1) Logical OR on the level the same attribute
`"CC": [ "DE", "US" ]`
means "DE" OR "US"
2) Logical AND on the level between particular attributes
`"Taxonomy": [ "Malicious Code" ], "CC": [ "DE" ]`
means that in order to match this filter, the event has to have field `CC` with value `DE` (or `US`) and has to have field `Taxonomy` with value `Malicious Code`

Last, but not least, every filter has to be one of the following types:
- "include" - pass events matching the criteria of any include filter if not excluded
- "exclude" - throw away all events matching the criteria, pass all the rest


Sample configuration files
```
filter1.json
{
    "name": "Allow only specific IP",
    "date": "2015-02-04",
    "type": "include",
    "conditions": {        
        "source.ip": [
            "10.0.0.1",
            "10.0.0.2"
        ]
}
```

```
filter2.json
{
    "name": "Exclude specific malware events",
    "date": "2015-02-03",
    "type": "exclude",
    "conditions": {
        "source.abuse_contact": [
            "one@example.com",
            "two@example.com",
        ],    
        "source.ip": [
            "10.0.0.1"
        ]
}
```

As the result, only events with source.ip = `10.0.0.1` OR `10.0.0.2` are passed by the `filter1.json` and only events from `...2` or not having one of the e-mails pass the `filter2.json`.
