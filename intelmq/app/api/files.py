"""Direct access to IntelMQ files and directories

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>

This module implements the part of the IntelMQ-Manager backend that
allows direct read and write access to some of the files used by
IntelMQ.
"""

from pathlib import PurePath, Path
from typing import Optional, Tuple, Union, Dict, Any, Iterable, BinaryIO

from intelmq_api.config import Config


def path_starts_with(path: PurePath, prefix: PurePath) -> bool:
    """Return whether the path starts with prefix.

    Both arguments must be absolute paths. If not, this function raises
    a ValueError.

    This function compares the path components, so it's not a simple
    string prefix test.
    """
    if not path.is_absolute():
        raise ValueError("{!r} is not absolute".format(path))
    if not prefix.is_absolute():
        raise ValueError("{!r} is not absolute".format(prefix))
    return path.parts[:len(prefix.parts)] == prefix.parts


class FileAccess:

    def __init__(self, config: Config):
        self.allowed_path = config.allowed_path

    def file_name_allowed(self, filename: str) -> Optional[Tuple[bool, Path]]:
        """Determine wether the API should allow access to a file."""
        resolved = Path(filename).resolve()
        if not path_starts_with(resolved, self.allowed_path):
            return None

        return (False, resolved)

    def load_file_or_directory(self, unvalidated_filename: str, fetch: bool) \
            -> Union[Tuple[str, Union[BinaryIO, Dict[str, Any]]], None]:
        allowed = self.file_name_allowed(unvalidated_filename)
        if allowed is None:
            return None

        content_type = "application/json"
        predefined, normalized = allowed

        if predefined or fetch:
            if fetch:
                content_type = "text/html"
            return (content_type, open(normalized, "rb"))

        result = {"files": {}}  # type: Dict[str, Any]
        if normalized.is_dir():
            result["directory"] = str(normalized)
            files = normalized.iterdir()  # type: Iterable[Path]
        else:
            files = [normalized]

        for path in files:
            stat = path.stat()
            if stat.st_size < 2000:
                # FIXME: don't hardwire this size
                obj = {"contents": path.read_text()}  # type: Dict[str, Any]
            else:
                obj = {"size": stat.st_size, "path": str(path.resolve())}
            result["files"][path.name] = obj
        return (content_type, result)
