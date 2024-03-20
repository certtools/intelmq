"""Helper functions for the API

SPDX-FileCopyrightText: 2020 Intevation GmbH <https://intevation.de>
SPDX-License-Identifier: AGPL-3.0-or-later

Funding: of initial version by SUNET
Author(s):
  * Bernhard Herzog <bernhard.herzog@intevation.de>
"""

import os
import pwd
import shlex
from typing import List


def effective_user_name() -> str:
    """Return the name of the effective user"""
    return pwd.getpwuid(os.geteuid()).pw_name


def format_shell_command(words: List[str]) -> str:
    """Format a shell command as a string for use with a shell.

    This function turns a command given as a list of strings as a single
    string that could be interpreted by the shell.

    When invoking subprocesses it's usually best to use a list of
    strings as the command so that no shell is involved so that one
    doesn't have to care about quoting. However, for error messages it's
    convenient for the user to see the command as it would be written
    for the shell so that it's easy to e.g. test it in an interactive
    shell.

    This function is basically identical to shlex.join function that was
    added in Python 3.8.
    """
    return " ".join(shlex.quote(word) for word in words)


def shell_command_for_errors(words: List[str]) -> str:
    """Return a formatted shell command for error messages.

    The return value contains the command formatted for use in a shell
    with a prefix that uses sudo to execute the command as the users
    this API is running as. This is intended primarily for error
    messages so that users of the web interface can use the command to
    replicate the problems that may be encountered.

    This is particularly interesting for the usual case where we do not
    invoke intelmqctl directly but run it via sudo from code executed by
    special users like www-data.
    """
    return format_shell_command(["sudo", "-u", effective_user_name()] + words)
