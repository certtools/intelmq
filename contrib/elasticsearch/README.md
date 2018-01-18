# ElasticMapper Tool

## Description

ElasticMapper is a tool to generate the ElasticSearch mapping required to specify the proper fields and field types which will be insert on ElasticSearch database. This tool uses the IntelMQ harmonization file to automatically generate the mapping and provides a quick way to send directly the mapping to ElasticSearch or write in a local file the generated mapping.

## Requirements

```
pip3 install elasticsearch
```

## Execution

### Options

```
usage: elasticmapper [-h] --harmonization-file <filepath>
                     [--harmonization-fallback] [--host <ip>] [--index INDEX]
                     [--index-type INDEX_TYPE] [--output <filepath>]

Elastic Mapper tool

optional arguments:
  -h, --help            show this help message and exit
  --harmonization-file <filepath>
                        harmonization file
  --harmonization-fallback
                        harmonization fallback to `text` type
  --host <ip>           elasticsearch server IP
  --index INDEX         elasticsearch index
  --index-type INDEX_TYPE
                        elasticsearch index type
  --output <filepath>   write mapping to file
```

### Examples

#### Send-only to ElasticSearch

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --index-type=events --host=127.0.0.1
```

#### Write-only to output file

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --index-type=events --output=/tmp/mapping.txt
```

#### Send to ElasticSearch and write to output file
```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --index-type=events --output=/tmp/mapping.txt --host=127.0.0.1
```

#### Harmonization fallback

In case elasticmapper returned an error related to harmonization field type unrecognizable, specify an additional parameter to fallback to `text` type any unrecognizable field types.

```
elasticmapper --harmonization-file=intelmq/intelmq/etc/harmonization.conf --index=intelmq --index-type=events --output=/tmp/mapping.txt --host=127.0.0.1 --harmonization-fallback
```
