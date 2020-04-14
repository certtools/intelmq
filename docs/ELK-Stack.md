# ELK Stack

If you wish to run IntelMQ with ELK (Elasticsearch, Logstash, Kibana) it is entirely possible. This guide assumes the reader is familiar with basic configuration of ELK and does not aim to cover using ELK in general. It is based on the version 6.8.0 (ELK is a fast moving train therefore things might change). Assuming you have IntelMQ (and Redis) installation in place, lets dive in.

## Configuring IntelMQ for Logstash

In order to pass IntelMQ events to Logstash we are going to need an output queue, particulary orphaned queue (which simply means there is no IntelMQ bot processing events from this queue). However because IntelMQ system does not like to have an orphaned queue (and the IntelMQ Manager does not allow to create one), we will simply add a new bot at the end of the pipeline (or wherever you see fit) and set it's configuration `enabled` to `false`. The bot type does not matter as it's only a forever disabled dummy bot (it's recommended to choose an output bot, e.g. Rest API Output Bot).

## Configuring Logstash

Logstash defines pipeline as well. In the pipeline configuration of Logstash you need to specify where it should look for IntelMQ events, what to do with them and where to pass them.

### Input

This part describes how to receive data from Redis queue.
See the example configuration and comments below:

```
input {
  redis {
    host => "10.10.10.10"
    port => 6379
    db => 2 
    data_type => "list"
    key => "restapi-output-queue"
  }
}
```
* `host` - Redis hostname or IP
* `port` - Redis port
* `db` - Redis db used (same value as `source_pipeline_db` from defaults.conf of IntelMQ)
* `data_type` - data type is usually `list`
* `key` - name of the queue (found in pipeline.conf of IntelMQ as source queue for our dummy bot)

**Extra**

You can also use syntax like this: `host => "${REDIS_HOST:10.10.10.10}"`

The value will then be taken from environment variable `$REDIS_HOST`. If the environment variable is not defined then the default value of `10.10.10.10` will be used instead.

### Filter (optional)

Before passing the data to the database you can apply certain changes. This is done with filters. See an example: 
```
filter {
  mutate {
    lowercase => ["source.geolocation.city", "classification.identifier"]
    remove_field => ["__type", "@version"]
  }
  date {
    match => ["time.observation", "ISO8601"]
  }
}
```
I recommend using the `date` filter: generally we have two timestamp fields - `time.source` (provided by feed source this can be understood as when the event happend; however it is not always present) and `time.observation` (when IntelMQ collected this event). Logstash also adds another field `@timestamp` with time of processing by Logstash. While it can be useful for debugging, I recommend to set the `@timestamp` to the same value as `time.observation`.

### Output 

The pipeline also needs output, where we define our database (Elasticsearch). The simplest way of doing so is defining an output like this:
```
output {
  elasticsearch {
    hosts => ["http://10.10.10.11:9200", "http://10.10.10.12:9200"]
    index => "intelmq-%{+YYYY.MM}"
  }
}
```
* `hosts` - Elasticsearch host (or more) with the correct port (9200 by default)
* `index` - name of the index where to insert data

Our experience, hardware equipment and the amount of events collected led us to having a separate index for each month. This might not necessarily suit your needs.

## Configuring Elasticsearch

Configuring Elasticsearch is entirely up to you and should be consulted with the [official documentation](https://www.elastic.co/guide/en/elasticsearch/reference/index.html). What you will most likely need is something called [index template](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html) mappings which I can provide. Again it might not suit your needs so feel free to adjust it for your use case, it is only included as an inspiration.

```
{
    "mappings" : {
      "event" : {
        "numeric_detection" : true,
        "dynamic_templates" : [
          {
            "string_fields" : {
              "mapping" : {
                "norms" : false,
                "type" : "text"
              },
              "match_mapping_type" : "string",
              "match" : "*"
            }
          }
        ],
        "date_detection" : true,
        "properties" : {
          "malware" : {
            "properties" : {
              "name" : {
                "type" : "text"
              },
              "version" : {
                "type" : "keyword"
              },
              "hash" : {
                "properties" : {
                  "sha1" : {
                    "type" : "keyword"
                  },
                  "sha256" : {
                    "type" : "keyword"
                  },
                  "md5" : {
                    "type" : "keyword"
                  }
                }
              }
            }
          },
          "destination" : {
            "properties" : {
              "registry" : {
                "type" : "keyword"
              },
              "fqdn" : {
                "type" : "keyword"
              },
              "domain_suffix" : {
                "type" : "keyword"
              },
              "ip" : {
                "type" : "ip"
              },
              "url" : {
                "type" : "text"
              },
              "network" : {
                "type" : "keyword"
              },
              "local_ip" : {
                "type" : "ip"
              },
              "port" : {
                "type" : "long"
              },
              "abuse_contact" : {
                "type" : "keyword"
              },
              "tor_node" : {
                "type" : "boolean"
              },
              "local_hostname" : {
                "type" : "text"
              },
              "asn" : {
                "type" : "keyword"
              },
              "account" : {
                "type" : "text"
              },
              "reverse_dns" : {
                "type" : "keyword"
              },
              "allocated" : {
                "type" : "date"
              },
              "as_name" : {
                "type" : "keyword"
              },
              "geolocation" : {
                "properties" : {
                  "cc" : {
                    "type" : "keyword"
                  },
                  "city" : {
                    "type" : "keyword"
                  },
                  "latitude" : {
                    "type" : "float"
                  },
                  "state" : {
                    "type" : "keyword"
                  },
                  "region" : {
                    "type" : "keyword"
                  },
                  "longitude" : {
                    "type" : "float"
                  }
                }
              }
            }
          },
          "event_description" : {
            "properties" : {
              "text" : {
                "type" : "text"
              },
              "url" : {
                "type" : "text"
              },
              "target" : {
                "type" : "text"
              }
            }
          },
          "raw" : {
            "type" : "keyword"
          },
          "misp" : {
            "properties" : {
              "attribute_uuid" : {
                "type" : "keyword"
              },
              "event_uuid" : {
                "type" : "keyword"
              }
            }
          },
          "source" : {
            "properties" : {
              "registry" : {
                "type" : "keyword"
              },
              "fqdn" : {
                "type" : "keyword"
              },
              "domain_suffix" : {
                "type" : "keyword"
              },
              "ip" : {
                "type" : "ip"
              },
              "url" : {
                "type" : "text"
              },
              "network" : {
                "type" : "keyword"
              },
              "local_ip" : {
                "type" : "ip"
              },
              "urlpath" : {
                "type" : "text"
              },
              "port" : {
                "type" : "long"
              },
              "abuse_contact" : {
                "type" : "keyword"
              },
              "tor_node" : {
                "type" : "boolean"
              },
              "local_hostname" : {
                "type" : "text"
              },
              "asn" : {
                "type" : "keyword"
              },
              "account" : {
                "type" : "text"
              },
              "reverse_dns" : {
                "type" : "keyword"
              },
              "allocated" : {
                "type" : "date"
              },
              "as_name" : {
                "type" : "keyword"
              },
              "geolocation" : {
                "properties" : {
                  "cc" : {
                    "type" : "keyword"
                  },
                  "city" : {
                    "type" : "keyword"
                  },
                  "latitude" : {
                    "type" : "float"
                  },
                  "state" : {
                    "type" : "keyword"
                  },
                  "region" : {
                    "type" : "keyword"
                  },
                  "longitude" : {
                    "type" : "float"
                  }
                }
              }
            }
          },
          "classification" : {
            "properties" : {
              "identifier" : {
                "type" : "keyword"
              },
              "taxonomy" : {
                "type" : "keyword"
              },
              "type" : {
                "type" : "keyword"
              }
            }
          },
          "feed" : {
            "properties" : {
              "code" : {
                "type" : "keyword"
              },
              "provider" : {
                "type" : "keyword"
              },
              "documentation" : {
                "type" : "keyword"
              },
              "name" : {
                "type" : "keyword"
              },
              "accuracy" : {
                "type" : "float"
              },
              "url" : {
                "type" : "text"
              }
            }
          },
          "protocol" : {
            "properties" : {
              "application" : {
                "type" : "keyword"
              },
              "transport" : {
                "type" : "keyword"
              }
            }
          },
          "event_hash" : {
            "type" : "keyword"
          },
          "tlp" : {
            "type" : "keyword"
          },
          "comment" : {
            "type" : "text"
          },
          "time" : {
            "properties" : {
              "observation" : {
                "type" : "date"
              },
              "source" : {
                "type" : "date"
              }
            }
          },
          "status" : {
            "type" : "keyword"
          }
        }
      }
    }
}
```

