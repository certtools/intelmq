A bot to filter specific events from the pipeline. This version of the bot, the filter parameters include:
- Taxonomy - values describeb here https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md#typetaxonomy-mapping
- Type - values described here https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md#typetaxonomy-mapping
- ASN - string with autonomous system number, e.g. "12345"
- CIDR - notation of particular subnet, e.g. "192.168.100.0/24" (yet to be finished)
- AbuseEmail - email address including wildcards, e.g. "*@isp.cz"
- CC - country code, e.g. "CN" or "US"

With the filter bot, one should be able to define filters such as:
 - throw away all events for specific ASN or CIDR
 - pass just events with particular CC or Taxonomy
 - or even a combination of multiple like throw away all "Intrusion" events for CIDR 123.34.5.0/24

Processing of the filter configuration is as follows:
1) Logical OR on the level the same attribute
"CC": [ "DE", "US" ]
means "DE" OR "US"
2) Logical AND on the level between particular attributes
"Taxonomy": [ "Malicious Code" ], "CC": [ "DE" ]
means that in order to match this filter, the event has to have country code "DE" and has to be under taxonomy "Malicious Code"

Last, but not least, every filter has to be one of the following types:
- "include" - pass events matching the criteria of any include filter
- "exclude" - throw away all events matching the criteria, pass all the rest


Sample configuration file
```
{
    "name": "Exclude specific malware events",
    "date": "2015-02-03",
    "type": "exclude",
    "filter": {
        "Taxonomy": [
            "Malicious Code",
            "Intrusion Attempts"
        ],
        "Type": [
            "botnet drone",
            "c&c"
        ],
        "ASN": [
            "25761",
            "54600"
        ],
        "CIDR": [
            "192.168.100.0/24",
            "10.10.25.38/32"
        ],
        "Recipient": [
            "info@abuse.com",
            "*@isp.cz"
        ],
        "CC": [
            "US"
        ]
    }
}
```
