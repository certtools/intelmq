<!--
SPDX-FileCopyrightText: 2018 SYNchroACK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# ElasticMapper Tool

## Description

ElasticMapper is a tool to generate the Elasticsearch mapping required to specify the proper fields and field types which will be inserted into the Elasticsearch database.
This tool uses the IntelMQ harmonization file to automatically generate the mapping and provides a quick way to send the mapping directly to Elasticsearch or write the generated mapping to a local file.

## Requirements

```
pip3 install elasticsearch
```

## Execution

### Options

```
usage: elasticmapper [-h] --harmonization-file <filepath>
                     [--harmonization-fallback] [--host <ip>] [--index INDEX]
                     [--output <filepath>]

Elastic Mapper tool

optional arguments:
  -h, --help            show this help message and exit
  --harmonization-file <filepath>
                        harmonization file
  --harmonization-fallback
                        harmonization fallback to `text` type
  --host <ip>           elasticsearch server IP
  --index INDEX         elasticsearch index
  --index-template      save the mapping as a template for newly-created indices
  --output <filepath>   write mapping to file
```

### Examples

#### Send only to Elasticsearch

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --host=127.0.0.1
```

#### Write only to output file

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --output=/tmp/mapping.txt
```

#### Send to Elasticsearch and write to output file
```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --output=/tmp/mapping.txt --host=127.0.0.1
```

#### Send to Elasticsearch as a template (see https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates.html)

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --host=127.0.0.1 --index-template
```

#### Harmonization fallback

Revert to the default 'text' type in the generated mapping for any fields which have unrecognizable field types.

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --output=/tmp/mapping.txt --host=127.0.0.1 --harmonization-fallback
```
