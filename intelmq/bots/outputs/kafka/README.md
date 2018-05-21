# Kafka Output Bot

### Output Bot that sends events to kafka


Bot parameters:

* kafka_broker_list       : comma seperated list of kafka brokers. defaults to 127.0.0.1
* kafka_topic      : Index for the ElasticSearch output, defaults to intelmq
* flatten_fields     : In ES, some query and aggregations work better if the fields are flat and not JSON. Here you can provide a list of fields to convert.
                      Can be a list of strings (fieldnames) or a string with field names separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`
                      Default: ['extra']

