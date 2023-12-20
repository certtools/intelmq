"""Python __init__ file that provides the path to the module

SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later

"""
import pathlib
from .version import __version__, __version_info__  # noqa

path = pathlib.Path(__file__).parent
