# SPDX-FileCopyrightText: 2022 CERT.at GmbH <intelmq-team@cert.at>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

class Packer():
    def __init__(self) -> None:
        pass

    def serialize(self, data: bytes, **kwargs) -> bytes:
        raise NotImplementedError()

    def deserialize(self, data: bytes, **kwargs) -> object:
        raise NotImplementedError()
