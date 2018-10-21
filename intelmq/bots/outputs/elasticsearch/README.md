# Elasticsearch Output Bot

Output Bot that sends events to Elasticsearch

#### Configuration parameters:

* elastic_host       : Name/IP for the Elasticsearch server, defaults to 127.0.0.1
* elastic_port       : Port for the Elasticsearch server, defaults to 9200
* elastic_index      : Index for the Elasticsearch output, defaults to intelmq
* rotate_index       : If set, will index events using the date information associated with the event.
                       Options: 'never', 'daily', 'weekly', 'monthly', 'yearly'. Using 'intelmq' as the elastic_index, the following are examples of the generated index names:
                       'never' --> intelmq
                       'daily' --> intelmq-2018-02-02
                       'weekly' --> intelmq-2018-42
                       'monthly' --> intelmq-2018-02
                       'yearly' --> intelmq-2018
* elastic_doctype    : Elasticsearch document type for the event. Default: events
* http_username      : http_auth basic username
* http_password      : http_auth basic password
* replacement_char   : If set, dots ('.') in field names will be replaced with this character prior to indexing. This is for backward compatibility with ES 2.X. Default: null. Recommended for ES2.X: '_'
* flatten_fields     : In ES, some query and aggregations work better if the fields are flat and not JSON. Here you can provide a list of fields to convert.
                       Can be a list of strings (fieldnames) or a string with field names separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`
                       Default: ['extra']

See contrib/elasticsearch/elasticmapper for a utility for creating Elasticsearch mappings and templates.

If using rotate_index, the resulting index name will be of the form [elastic_index]-[event date].
To query all intelmq indices at once, use an alias (https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html), or a multi-index query.

The data in ES can be retrieved with the HTTP-Interface:

```bash
> curl -XGET 'http://localhost:9200/intelmq/events/_search?pretty=True'
```
