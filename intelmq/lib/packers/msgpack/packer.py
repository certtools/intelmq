# SPDX-FileCopyrightText: 2022 CERT.at GmbH <intelmq-team@cert.at>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from intelmq.lib.packers.packer import Packer
from intelmq.lib import exceptions


try:
    import msgpack
except:
    msgpack = None


class MsgPack(Packer):
    def __init__(self) -> None:
        if msgpack is None:
            raise exceptions.MissingDependencyError("msgpack")
        super().__init__()

    def serialize(self, data, **kwargs) -> bytes:
        return msgpack.packb(data, **kwargs)

    def deserialize(self, data, **kwargs) -> object:
        return msgpack.unpackb(data, raw=False, **kwargs)
