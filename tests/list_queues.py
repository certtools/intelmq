import redis

redis = redis.Redis( host = "127.0.0.1",
                        port = int(6379),
                        db = 2,
                        socket_timeout = 5
                    )

lista = [
    'arbor-collector',
    'arbor-parser',
    'archive',
    'bruteforceblocker-collector',
    'bruteforceblocker-parser',
    'cymru-expert',
    'deduplicator-expert',
    'dragon-research-group-ssh-collector',
    'dragon-research-group-ssh-parser',
    'dragon-research-group-vnc-collector',
    'dragon-research-group-vnc-parser',
    'malware-domain-list-collector',
    'malware-domain-list-parser',
    'malwarepatrol-dans-guardian-collector',
    'malwarepatrol-dans-guardian-parser',
    'openbl-collector',
    'openbl-parser',
    'phishtank-collector',
    'phishtank-parser',
    'postgresql-output',
    'sanitizer-expert',
    'taxonomy-expert',
    'vxvault-collector',
    'vxvault-parser'
    ]

for bot in lista:
    print "%s: %s" % (bot, redis.llen(bot+"-queue"))