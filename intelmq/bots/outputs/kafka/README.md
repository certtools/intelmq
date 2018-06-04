# Kafka Output Bot

### Output Bot that sends events to kafka


Bot parameters:

Kafka Producer
* kafka_broker_list : comma seperated list of kafka brokers. defaults to 127.0.0.1

* kafka_topic       : Index for the ElasticSearch output, defaults to intelmq

* flatten_fields    : In ES, some query and aggregations work better if the fields are flat and not JSON. 
                      Here you can provide a list of fields to convert. Can be a list of strings (fieldnames) 
                      or a string with field names separated by a comma (,). eg `extra,field2` or `['extra', 'field2']`
                      Default: ['extra']

AVRO Producer
* avro_topic_schema : a file path, pointing to a file containing a dict object containing expected values, and their destination topics.
                      the keys in this dict should be all expected values in 'avro_topic_field' 

                      IMPORTANT:schema must contain "other" keyword, with either None, or a topic name as the value.
                      If None is declared, other values are dropped.

* avro_topic_field :  The field to be used to map intelligence identy to destination topic

* avro_value_schema_file: The schema file 

* avro_schema_registry:   URL where the schema registry is defined.
