#!/bin/bash

echo "Bots:"
jq '.Collector | keys | length' intelmq/bots/BOTS
jq '.Parser | keys | length' intelmq/bots/BOTS
jq '.Expert | keys | length' intelmq/bots/BOTS
jq '.Output | keys | length' intelmq/bots/BOTS

echo "Feeds:"
grep -Ec '^    [^ ]' intelmq/etc/feeds.yaml
echo "Shadowserver:"
python3 -c "import intelmq.bots.parsers.shadowserver.config; print(len(intelmq.bots.parsers.shadowserver.config.mapping))"

