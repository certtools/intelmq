# ElasticMapper Tool

## Requirements

```
pip3 install elasticsearch
```

## Execution

### Options

```
elasticmapper -h
usage: elasticmapper [-h] --harmonization-file <filepath> [--host <ip>]
                     [--index INDEX] [--index-type INDEX_TYPE]
                     [--output <filepath>]

Elastic Mapper tool

optional arguments:
  -h, --help            show this help message and exit
  --harmonization-file <filepath>
                        harmonization file
  --host <ip>           elasticsearch server IP
  --index INDEX         elasticsearch index
  --index-type INDEX_TYPE
                        elasticsearch index type
  --output <filepath>   write a copy of applied mapping to file
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
