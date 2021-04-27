#!/bin/bash

echo "Bots:"
bots=$(intelmqctl --type json list bots)
echo $bots | jq '.Collector | keys | length'
echo $bots | jq '.Parser | keys | length'
echo $bots | jq '.Expert | keys | length'
echo $bots | jq '.Output | keys | length'

echo "Feeds:"
grep -Ec '^    [^ ]' intelmq/etc/feeds.yaml
echo "Shadowserver:"
python3 -c "import intelmq.bots.parsers.shadowserver._config; print(len(intelmq.bots.parsers.shadowserver._config.mapping))"

