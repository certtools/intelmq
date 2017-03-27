# Elasticsearch Output Bot

### Output Bot that sends events to a Elasticsearch


Bot parameters:

* elastic_host       : Name/IP for the elasticsearch server, defaults to 127.0.0.1
* elastic_port       : Port for the elasticsearch server, defaults to 9200
* elastic_index      : Index for the Elasticsearch output, defaults to intelmq
* elastic_doctype    : docname to put the event data, defaults to events
* replacement_char   : ES forbits '.' in field names since v2.0, this parameters specifies which character should be used as replacement for '.', defaults to '_'
* flatten_fields     : In ES, some query and aggrigations work better if the fields are flat and not JSON. Here you can provide a list of fields to convert.
                       Can be a list of strings (fieldnames) or a string with fieldnames separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`
                       Default: ['extra']

The data in ES can be retrieved with the HTTP-Interface:

```bash
> curl -XGET 'http://localhost:9200/intelmq/events/_search?pretty=True'
```
