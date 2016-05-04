# -*- coding: utf-8 -*-
"""
Cache is a set with information already seen by the system.
This provides a way, for example, to remove duplicated events
and reports in system or cache some results from experts like
Cymru Whois. It's possible to define a TTL value in each information
inserted in cache. This TTL means how much time the system will keep an
information in the cache.
"""
import redis

import intelmq.lib.utils as utils

__all__ = ['Cache']


class Cache():

    def __init__(self, host, port, db, ttl):
        self.redis = redis.Redis(host=host,
                                 port=int(port),
                                 db=db,
                                 socket_timeout=5)

        self.ttl = ttl

    def exists(self, key):
        return self.redis.exists(key)

    def get(self, key):
        retval = self.redis.get(key)
        if isinstance(retval, bytes):
            return utils.decode(retval)
        return retval

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl
        if isinstance(value, str):
            value = utils.encode(value)
        # backward compatibility (Redis v2.2)
        self.redis.setnx(key, value)
        self.redis.expire(key, ttl)

    def flush(self):
        """
        Flushes the currently opened database by calling FLUSHDB.
        """
        self.redis.flushdb()
