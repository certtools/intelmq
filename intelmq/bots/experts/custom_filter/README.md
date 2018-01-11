# Custom filter bot

A bot to filter specific events from the pipeline. See valid fields at https://github.com/certtools/intelmq/blob/master/docs/Harmonization-fields.md

With the filter bot, one should be able to define filters such as:
 - throw away all events for specific ASN or CIDR
 - pass just events with particular CC or Taxonomy
 - or even a combination of multiple like throw away all "Intrusion" events for CIDR 123.34.5.0/24

## Description

In the `runtime.conf` / parameters we define `rules_dir` with a directory where filter configuration files are stored. Such file contains a JSON with following fields:
* `name` (optional) – name of the filter
* `description` (optional) – any additional text
* `date` (optional) – when the filter was added
* `type` – one of the following:
	- "**include**" - pass events matching the criteria of any include filter if not excluded
	- "**exclude**" - throw away all events matching the criteria, pass all the rest
* `conditions` – dict of keys from intelmq-event-fields
	* each of the fields are mapped to a `value` or `list` of values
	* processing of the filter configuration is as follows:
		1) Logical OR on the level the same attribute
`"country": [ "DE", "US" ]`
means "DE" OR "US"
		2) Logical AND on the level between particular attributes
`"taxonomy": [ "malware" ], "country": [ "DE" ]`
means that in order to match this filter, the event has to have field `country` with value `DE` (or `US`) and has to have field `taxonomy` with value `malware`
	* if the field is "**source.ip**", it may contain either the IP address or IPv4 network mask in the format "1.2.3.4/XY"


## Sample configuration files
```
filter1.json
{
    "name": "Allow only specific IP",
    "date": "2015-02-04",
    "type": "include",
    "conditions": {        
        "source.ip": [
            "10.0.0.0/24"            
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

As the result, only events with source.ip in `"10.0.0.0/24"` are passed (`filter1.json`) and then, events from `"10.0.0.1"` having one of the e-mails are dropped (`filter2.json`).  
So `"10.0.0.2"` passes every time but `"10.0.0.1"` passes only if not having `"one@example.com"` abuse mail.
