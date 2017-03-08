# Elasticsearch Output Bot

### Output Bot that sends events to a Elasticsearch


Bot parameters:

* elastic_host       : Name/IP for the elasticsearch server, defaults to 127.0.0.1
* elastic_port       : Port for the elasticsearch server, defaults to 9200
* elastic_index      : Index for the Elasticsearch output, defaults to intelmq
* elastic_doctype    : docname to put the event data, defaults to events
* sanitize_keys      : true/false value to indicate if key names should be changed to remove '.', which is forbidden character in ES, defaults to true
* replacement_char   : if sanitize_keys is true, which character should be used as replacement for '.', defaults to '_'
