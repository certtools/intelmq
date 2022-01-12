""" CacheMixin for IntelMQ

SPDX-FileCopyrightText: 2021 Sebastian Waldbauer
SPDX-License-Identifier: AGPL-3.0-or-later

CacheMixin is used for caching/storing data in redis.
"""

from typing import Any, Optional
import redis
import intelmq.lib.utils as utils


class CacheMixin:
    __redis: redis.Redis = None
    redis_cache_host: str = "127.0.0.1"
    redis_cache_port: int = 6379
    redis_cache_db: int = 9
    redis_cache_ttl: int = 15
    redis_cache_password: Optional[str] = None

    def __init__(self, **kwargs):
        if self.redis_cache_host.startswith("/"):
            kwargs = {"unix_socket_path": self.redis_cache_host}
        elif self.redis_cache_host.startswith("unix://"):
            kwargs = {"unix_socket_path": self.redis_cache_host.replace("unix://", "")}
        else:
            kwargs = {
                "host": self.redis_cache_host,
                "port": int(self.redis_cache_port),
                "socket_timeout": 5,
            }

        self.__redis = redis.Redis(db=self.redis_cache_db, password=self.redis_cache_password, **kwargs)
        super().__init__()

    def cache_exists(self, key: str):
        return self.__redis.exists(key)

    def cache_get(self, key: str):
        retval = self.__redis.get(key)
        if isinstance(retval, bytes):
            return utils.decode(retval)
        return retval

    def cache_set(self, key: str, value: Any, ttl: Optional[int] = None):
        if self.redis_cache_ttl is None:
            ttl = self.redis_cache_ttl
        if isinstance(value, str):
            value = utils.encode(value)
        # backward compatibility (Redis v2.2)
        self.__redis.set(key, value)
        if self.redis_cache_ttl:
            self.__redis.expire(key, self.redis_cache_ttl)

    def cache_flush(self):
        """
        Flushes the currently opened database by calling FLUSHDB.
        """
        self.__redis.flushdb()

    def cache_get_redis_instance(self):
        return self.__redis
