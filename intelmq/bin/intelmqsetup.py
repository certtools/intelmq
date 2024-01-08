"""
© 2019-2021 nic.at GmbH <intelmq-team@cert.at>

SPDX-License-Identifier: AGPL-3.0-or-later

Sets up an intelmq environment after installation or upgrade by
 * creating needed directories
 * set intelmq as owner for those
 * providing example configuration files if not already existing

If intelmq-api is installed, the similar steps are performed:
 * creates needed directories
 * sets the webserver as group for them
 * sets group write permissions

Reasoning:
Pip does not (and cannot) create `/opt/intelmq`/user-given ROOT_DIR, as described in
https://github.com/certtools/intelmq/issues/819
"""
import argparse
import os
import shutil
import stat
import sys
import pkg_resources

from grp import getgrnam
from pathlib import Path
from pwd import getpwnam
from typing import Optional

from termstyle import red
from intelmq import (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                     VAR_STATE_PATH, STATE_FILE_PATH, VAR_SERVER_PATH)
from intelmq.bin.intelmqctl import IntelMQController

FILE_OUTPUT_PATH = Path(VAR_STATE_PATH) / 'file-output/'
ETC_INTELMQ = Path('/etc/intelmq/')
ETC_INTELMQ_MANAGER = ETC_INTELMQ / 'manager/'


def basic_checks(skip_ownership):
    if os.geteuid() != 0 and not skip_ownership:
        sys.exit(red('You need to run this program as root for setting file ownership!'))
    if not ROOT_DIR:
        sys.exit(red('Not a pip-installation of IntelMQ, nothing to initialize.'))

    if skip_ownership:
        return
    try:
        getpwnam('intelmq')
    except KeyError:
        sys.exit(red("User 'intelmq' does not exist. Please create it and then re-run this program."))
    try:
        getgrnam('intelmq')
    except KeyError:
        sys.exit(red("Group 'intelmq' does not exist. Please create it and then re-run this program."))


def create_directory(directory: str, octal_mode: int):
    directory = Path(directory)
    readable_mode = stat.filemode(octal_mode)
    if not directory.is_dir():
        directory.mkdir(mode=octal_mode, exist_ok=True, parents=True)
        print(f'Created directory {directory!s} with permissions {readable_mode}.')
    else:
        current_mode = directory.stat().st_mode
        if current_mode != octal_mode:
            current_mode_readable = stat.filemode(current_mode)
            print(f'Fixed wrong permissions of {directory!s}: {current_mode_readable!r} -> {readable_mode!r}.')
            directory.chmod(octal_mode)


def change_owner(file: str, owner: Optional[str] = None, group: Optional[str] = None, log: bool = True):
    if Path(file).as_posix() in ['/', '//']:
        # Skip taking ownership over system root path
        return
    if owner and Path(file).owner() != owner:
        if log:
            print(f'Fixing owner of {file!s}.')
        shutil.chown(file, user=owner)
    if group and Path(file).group() != group:
        if log:
            print(f'Fixing group of {file!s}.')
        shutil.chown(file, group=group)


def intelmqsetup_core(ownership=True, state_file=STATE_FILE_PATH):
    create_directory(FILE_OUTPUT_PATH, 0o40755)
    create_directory(VAR_RUN_PATH, 0o40755)
    create_directory(DEFAULT_LOGGING_PATH, 0o40755)
    create_directory(CONFIG_DIR, 0o40775)
    create_directory(VAR_SERVER_PATH, 0o40775)

    example_path = Path(pkg_resources.resource_filename('intelmq', 'etc'))
    example_confs = [
        example_path / 'runtime.yaml',
        example_path / 'harmonization.conf',
        example_path / 'intelmq.yaml',
    ]
    for example_conf in example_confs:
        fname = Path(example_conf).name
        destination_file = Path(CONFIG_DIR) / fname
        if destination_file.exists():
            print(f'Not overwriting existing {fname!r} with example.')
            log_ownership_change = True
        else:
            shutil.copy(example_conf, CONFIG_DIR)
            print(f'Installing example {fname!r} to {CONFIG_DIR}.')
            log_ownership_change = False  # For installing the new files, we don't need to inform the admin that the permissions have been "fixed"
        if ownership:
            change_owner(destination_file, owner='intelmq', group='intelmq', log=log_ownership_change)

    if ownership:
        print('Setting intelmq as owner for it\'s directories.')
        for obj in (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                    VAR_STATE_PATH, FILE_OUTPUT_PATH, Path(STATE_FILE_PATH).parent):
            change_owner(obj, owner='intelmq')

    print('Calling `intelmqctl upgrade-config` to update/create state file.')
    controller = IntelMQController(interactive=False, no_file_logging=True,
                                   drop_privileges=False)
    controller.upgrade_conf(state_file=state_file, no_backup=True)
    if ownership:
        change_owner(STATE_FILE_PATH, owner='intelmq', group='intelmq')


def main():
    parser = argparse.ArgumentParser("Set's up directories and example "
                                     "configurations for IntelMQ.")
    parser.add_argument('--skip-ownership', action='store_true',
                        help='Skip setting file ownership')
    parser.add_argument('--state-file',
                        help='The state file location to use.',
                        default=STATE_FILE_PATH)
    parser.add_argument('--webserver-user',
                        help='(DEPRECATED) The webserver to use instead of auto-detection.')
    parser.add_argument('--webserver-configuration-directory',
                        help='(DEPRECATED) The webserver configuration directory to use instead of auto-detection.')
    parser.add_argument('--skip-api',
                        help='(DEPRECATED) Skip set-up of intelmq-api.',
                        action='store_true')
    parser.add_argument('--skip-webserver',
                        help='(DEPRECATED) Skip all operations on the webserver configuration, affects the API and Manager.',
                        action='store_true')
    parser.add_argument('--skip-manager',
                        help='(DEPRECATED) Skip set-up of intelmq-manager.',
                        action='store_true')
    args = parser.parse_args()

    basic_checks(skip_ownership=args.skip_ownership)
    intelmqsetup_core(ownership=not args.skip_ownership,
                      state_file=args.state_file)

    print("'intelmqsetup' completed.")


if __name__ == '__main__':
    main()
