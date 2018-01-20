# Feeds Configuration Generator

Quickly generate feeds configurations (runtime and pipeline configs).

## Execute

```
./intelmq_gen_feeds_conf -h
usage: intelmq_gen_feeds_conf [-h] --feeds-file <filepath> [--all]

IntelMQ Feeds Config Generator tool

optional arguments:
  -h, --help            show this help message and exit
  --feeds-file <filepath>
                        feeds.yaml config file
  --all                 iterate through all feeds

```

```
./intelmq_gen_feeds_conf --feeds-file=../../intelmq/etc/feeds.yaml 

./intelmq_gen_feeds_conf --feeds-file=../../intelmq/etc/feeds.yaml --all
```
