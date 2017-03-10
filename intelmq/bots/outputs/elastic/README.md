# Elasticsearch Output Bot

### Output Bot that sends events to a Elasticsearch


Bot parameters:

* elastic_host       : Name/IP for the elasticsearch server, defaults to 127.0.0.1
* elastic_port       : Port for the elasticsearch server, defaults to 9200
* elastic_index      : Index for the Elasticsearch output, defaults to intelmq
* elastic_doctype    : docname to put the event data, defaults to events
* sanitize_keys      : true/false value to indicate if key names should be changed to remove '.', which is forbidden character in ES, defaults to true
* replacement_char   : if sanitize_keys is true, which character should be used as replacement for '.', defaults to '_'
* flatten_fields     : In ES, some query and aggrigations work better if the fields are flat and not nested. Here you can provide a list of fields to flatten out.
                       List of fields is seprated by comma (,) eg extra,field2
