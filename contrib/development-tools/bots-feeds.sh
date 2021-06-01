#!/bin/bash

# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

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

