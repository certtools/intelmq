```
$ ./intelmq-conf-validator -h
usage: intelmq-conf-validator [-h] --config-file <filepath> --validation-file
                              <filepath>

IntelMQ Config Validator tool

optional arguments:
  -h, --help            show this help message and exit
  --config-file <filepath>
                        config file (JSON or YAML)
  --validation-file <filepath>
                        validation file
```

```
cd intelmq/intelmq/bin/validators

./intelmq-conf-validator --config-file=../../etc/feeds.yaml --validation-file=feeds.schema.json

./intelmq-conf-validator --config-file=../../bots/BOTS --validation-file=bots.schema.json
```
