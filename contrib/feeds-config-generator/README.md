# Feeds Configuration Generator

Quickly generate feeds configurations (runtime and pipeline configs).

## Execute

```
./intelmq_gen_feeds_conf -h
usage: intelmq_gen_feeds_conf [-h] --feeds-file <filepath> [--all]
                              [--runtime-output-file <filepath>]
                              [--pipeline-output-file <filepath>]

IntelMQ Feeds Config Generator tool

optional arguments:
  -h, --help            show this help message and exit
  --feeds-file <filepath>
                        feeds.yaml config file
  --all                 iterate through all feeds
  --runtime-output-file <filepath>
                        /tmp/runtime.conf
  --pipeline-output-file <filepath>
                        /tmp/pipeline.conf

```
### Generate a bot configuration
```
./intelmq_gen_feeds_conf --feeds-file=../../intelmq/etc/feeds.yaml 
```

### Generate all bots configurations

```
./intelmq_gen_feeds_conf --feeds-file=../../intelmq/etc/feeds.yaml --all
```

### Generate all bots configurations and send to file

```
./intelmq_gen_feeds_conf --feeds-file=../../intelmq/etc/feeds.yaml --all  --runtime-output-file=/tmp/runtime.conf --pipeline-output-file=/tmp/pipeline.conf
```
