# SPDX-FileCopyrightText: 2022 CERT.at GmbH <intelmq-team@cert.at>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

from intelmq.lib.packers.packer import Packer
import json


class JSON(Packer):
    def __init__(self) -> None:
        super().__init__()

    def serialize(self, data, **kwargs) -> bytes:
        return json.dumps(data, **kwargs)

    def deserialize(self, data, **kwargs) -> object:
        return json.loads(data, **kwargs)
