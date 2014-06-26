#/usr/bin/env bash
python -m bots.inputs.arbor.feed arbor-feed &
python -m bots.inputs.arbor.parser arbor-parser &
python -m bots.inputs.arbor.harmonizer arbor-harmonizer &
python -m bots.inputs.vxvault.feed vxvault-feed &
python -m bots.inputs.vxvault.parser vxvault-parser &
python -m bots.inputs.vxvault.harmonizer vxvault-harmonizer &
python -m bots.inputs.malwaredomainlist.feed malwaredomainlist-feed &
python -m bots.inputs.malwaredomainlist.parser malwaredomainlist-parser &
python -m bots.inputs.malwaredomainlist.harmonizer malwaredomainlist-harmonizer &
python -m bots.experts.deduplicator.deduplicator deduplicator &
python -m bots.experts.sanitizer.sanitizer sanitizer &
python -m bots.experts.taxonomy.taxonomy taxonomy-expert &
#python -m bots.experts.geoip.geoip geoip-expert &
python -m bots.experts.cymru.cymru cymru-expert &
python -m bots.outputs.file.file file-output &
#python -m bots.outputs.mongodb.mongodb mongodb &

echo -en "\ec"
echo ""
echo ""
echo "Check /tmp/events.txt with following command:"
echo ""
echo "tail -f /tmp/events.txt"
echo ""
