# MISP collector

[MISP](https://github.com/MISP) is a malware information sharing platform.

This collector will search for events on a MISP server that have a
'to_process' tag attached to them (see the 'misp_tag_to_process' parameter)
and collect them for processing by IntelMQ. Once the MISP event has been
processed the 'to_process' tag is removed from the MISP event and a
'processed' tag is then attached (see the 'misp_tag_processed' parameter).

**NB.** The MISP tags must be configured to be 'exportable' otherwise they will
not be retrieved by the collector.

A sample configuration for this bot is as follows (see also the BOTS file):
```
"MISP Generic": {
    "description": "Collect events from a MISP server.",
    "module": "intelmq.bots.collectors.misp.collector",
    "parameters": {
        "feed": "misp_generic",
        "misp_url": "<URL of MISP server (with trailing '/')>",
        "misp_key": "<MISP Authkey>",
        "misp_tag_to_process": "<MISP tag for events to be processed>",
        "misp_tag_processed": "<MISP tag for processed events>",
        "rate_limit": 3600
    }
},
```
