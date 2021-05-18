# -*- coding: utf-8 -*-
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
from subprocess import run, CalledProcessError
from tempfile import NamedTemporaryFile
from typing import Optional

try:
    import intelmq_api
except ImportError:
    intelmq_api = None

try:
    import intelmq_manager
except ImportError:
    intelmq_manager = None

from termstyle import red
from intelmq import (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                     VAR_STATE_PATH, STATE_FILE_PATH)
from intelmq.bin.intelmqctl import IntelMQController


FILE_OUTPUT_PATH = Path(VAR_STATE_PATH) / 'file-output/'
ETC_INTELMQ = Path('/etc/intelmq/')
ETC_INTELMQ_MANAGER = ETC_INTELMQ / 'manager/'
WEBSERVER_CONFIG_DIR = None  # "cache" for the webserver configuration directory
NOTE_WEBSERVER_RELOAD = False  # if the webserver needs to be reloaded


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
    if owner and Path(file).owner() != owner:
        if log:
            print(f'Fixing owner of {file!s}.')
        shutil.chown(file, user=owner)
    if group and Path(file).group() != group:
        if log:
            print(f'Fixing group of {file!s}.')
        shutil.chown(file, group=group)


def find_webserver_user():
    candidates = ('www-data', 'wwwrun', 'httpd', 'apache')
    for candidate in candidates:
        try:
            getpwnam(candidate)
        except KeyError:
            pass
        else:
            print(f'Detected Apache username {candidate!r}.')
            return candidate
    else:
        sys.exit(red("Unable to detect Apache user name. "
                     "Please re-run this program and give the Apache user name with '--webserver-user'."))


def find_webserver_configuration_directory():
    global WEBSERVER_CONFIG_DIR
    if WEBSERVER_CONFIG_DIR:
        return WEBSERVER_CONFIG_DIR
    webserver_configuration_dir_candidates = (Path('/etc/apache2/conf-available/'),
                                              Path('/etc/apache2/conf.d/'),
                                              Path('/etc/httpd/conf.d/'))
    for webserver_configuration_dir_candidate in webserver_configuration_dir_candidates:
        if webserver_configuration_dir_candidate.exists():
            print(f'Detected Apache configuration directory {webserver_configuration_dir_candidate!s}.')
            WEBSERVER_CONFIG_DIR = webserver_configuration_dir_candidate
            webserver_configuration_dir_candidate.as_posix
            return webserver_configuration_dir_candidate
    else:
        sys.exit(red("Unable to detect Apache configuration directory. "
                     "Please re-run this program and give the Apache configuration directory with '--webserver-configuration-directory'."))


def debian_activate_apache_config(config_name: str):
    if 'available' not in WEBSERVER_CONFIG_DIR.as_posix():
        return  # not a Debian system
    available = WEBSERVER_CONFIG_DIR / config_name
    enabled = Path(WEBSERVER_CONFIG_DIR.as_posix().replace('available', 'enabled')) / config_name
    if not enabled.exists():
        enabled.symlink_to(available)
        print(f'Created symbolic link {enabled!s} pointing to {available!s}.')


def intelmqsetup_core(ownership=True, state_file=STATE_FILE_PATH):
    create_directory(FILE_OUTPUT_PATH, 0o40755)
    create_directory(VAR_RUN_PATH, 0o40755)
    create_directory(DEFAULT_LOGGING_PATH, 0o40755)
    create_directory(CONFIG_DIR, 0o40775)

    example_path = Path(pkg_resources.resource_filename('intelmq', 'etc'))
    example_confs = [example_path / 'runtime.yaml', example_path / 'harmonization.conf']
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


def intelmqsetup_api(ownership: bool = True, webserver_user: Optional[str] = None):
    intelmq_group = getgrnam('intelmq')
    webserver_user = webserver_user or find_webserver_user()

    create_directory(ETC_INTELMQ, 0o40775)
    if ownership:
        change_owner(CONFIG_DIR, group='intelmq')
        change_owner(ETC_INTELMQ, owner='intelmq', group='intelmq')

    # Manager configuration directory
    create_directory(ETC_INTELMQ_MANAGER, 0o40775)
    if ownership:
        change_owner(ETC_INTELMQ_MANAGER, group='intelmq')

    base = Path(pkg_resources.resource_filename('intelmq_api', '')).parent
    api_config = base / 'etc/intelmq/api-config.json'
    etc_intelmq_config = ETC_INTELMQ / 'api-config.json'
    api_sudoers = base / 'etc/intelmq/api-sudoers.conf'
    etc_sudoers_api = Path('/etc/sudoers.d/01_intelmq-api')  # same path as used in the packages
    api_manager_positions = base / 'etc/intelmq/manager/positions.conf'
    etc_intelmq_manager_positions = ETC_INTELMQ_MANAGER / 'positions.conf'

    if not base.as_posix().startswith('/usr/'):
        # Paths differ in editable installations
        print(red("Detected an editable (egg-link) pip-installation of 'intelmq-api'. Some feature of this program may not work."))

    if api_config.exists() and not etc_intelmq_config.exists():
        shutil.copy(api_config, etc_intelmq_config)
        print(f'Copied {api_config!s} to {ETC_INTELMQ!s}.')
    elif not api_config.exists() and not etc_intelmq_config.exists():
        print(red(f'Unable to install api-config.json: Neither {api_config!s} nor {etc_intelmq_config!s} exists.'))
    if api_sudoers.exists() and not etc_sudoers_api.exists():
        with open(api_sudoers) as sudoers:
            original_sudoers = sudoers.read()
        sudoers = original_sudoers.replace('www-data', webserver_user)
        with NamedTemporaryFile(mode='w') as tmp_file:
            tmp_file.write(sudoers)
            tmp_file.flush()
            try:
                run(('visudo', '-c', tmp_file.name))
            except CalledProcessError:
                sys.exit(red('Fatal error: Validation of adapted sudoers-file failed. Please report this bug.'))
            change_owner(tmp_file.name, owner='root', group='root', log=False)
            Path(tmp_file.name).chmod(0o440)
            shutil.copy(tmp_file.name, etc_sudoers_api)
        print(f'Copied {api_sudoers!s} to {etc_sudoers_api!s}.')
    elif not api_sudoers.exists() and not etc_sudoers_api.exists():
        print(red(f'Unable to install api-sudoers.conf: Neither {api_sudoers!s} nor {etc_sudoers_api!s} exists.'))
    if api_manager_positions.exists() and not etc_intelmq_manager_positions.exists():
        shutil.copy(api_manager_positions, etc_intelmq_manager_positions)
        print(f'Copied {api_manager_positions!s} to {etc_intelmq_manager_positions!s}.')
        etc_intelmq_manager_positions.chmod(0o664)
        change_owner(etc_intelmq_manager_positions, owner='intelmq', group='intelmq', log=False)
    elif not api_manager_positions.exists() and not etc_intelmq_manager_positions.exists():
        print(red(f'Unable to install positions.conf: Neither {api_manager_positions!s} nor {etc_intelmq_manager_positions!s} exists.'))

    if webserver_user not in intelmq_group.gr_mem:
        sys.exit(red(f"Webserver user {webserver_user} is not a member of the 'intelmq' group. "
                     f"Please add it with: 'usermod -aG intelmq {webserver_user}'."))


def intelmqsetup_api_webserver_configuration(webserver_configuration_directory: Optional[str] = None):
    webserver_configuration_dir = webserver_configuration_directory or find_webserver_configuration_directory()
    api_config = Path(pkg_resources.resource_filename('intelmq_api', '')).parent / 'etc/intelmq/api-apache.conf'
    apache_api_config = webserver_configuration_dir / 'api-apache.conf'
    if api_config.exists() and not apache_api_config.exists():
        shutil.copy(api_config, apache_api_config)
        print(f'Copied {api_config!s} to {ETC_INTELMQ!s}.')
        debian_activate_apache_config('api-apache.conf')

        global NOTE_WEBSERVER_RELOAD
        NOTE_WEBSERVER_RELOAD = True
    elif not api_config.exists() and not apache_api_config.exists():
        print(red(f'Unable to install webserver configuration api-config.conf: Neither {api_config!s} nor {apache_api_config!s} exists.'))

    print('Setup of intelmq-api successful.')


def intelmqsetup_manager_webserver_configuration(webserver_configuration_directory: Optional[str] = None):
    html_dir = Path(pkg_resources.resource_filename('intelmq_manager', '')).parent / '/usr/share/intelmq-manager/html'
    html_dir_destination = Path('/usr/share/intelmq-manager/html')

    if not html_dir_destination.as_posix().startswith('/usr/'):
        # Paths differ in editable installations
        print(red("Detected an editable (egg-link) pip-installation of intelmq-manager. Some feature of this program may not work."))

    webserver_configuration_dir = webserver_configuration_directory or find_webserver_configuration_directory()
    manager_config = Path(pkg_resources.resource_filename('intelmq_manager', '')).parent / 'etc/intelmq/manager-apache.conf'
    apache_manager_config = webserver_configuration_dir / 'manager-apache.conf'
    if manager_config.exists() and not apache_manager_config.exists():
        shutil.copy(manager_config, apache_manager_config)
        print(f'Copied {manager_config!s} to {apache_manager_config!s}.')
        debian_activate_apache_config('manager-apache.conf')

        global NOTE_WEBSERVER_RELOAD
        NOTE_WEBSERVER_RELOAD = True
    elif not manager_config.exists() and not apache_manager_config.exists():
        print(red(f'Unable to install webserver configuration manager-config.conf: Neither {manager_config!s} nor {apache_manager_config!s} exists.'))

    if html_dir.exists():
        try:
            shutil.copy(html_dir, '/')
        except Exception as exc:
            print(red(f"Unable to copy {html_dir} to {html_dir_destination}: {exc!s}"))
        else:
            print(f'Copied {html_dir!s} to {html_dir_destination!s}.')


def main():
    parser = argparse.ArgumentParser("Set's up directories and example "
                                     "configurations for IntelMQ.")
    parser.add_argument('--skip-ownership', action='store_true',
                        help='Skip setting file ownership')
    parser.add_argument('--state-file',
                        help='The state file location to use.',
                        default=STATE_FILE_PATH)
    parser.add_argument('--webserver-user',
                        help='The webserver to use instead of auto-detection.')
    parser.add_argument('--webserver-configuration-directory',
                        help='The webserver configuration directory to use instead of auto-detection.')
    parser.add_argument('--skip-api',
                        help='Skip set-up of intelmq-api.',
                        action='store_true')
    args = parser.parse_args()

    basic_checks(skip_ownership=args.skip_ownership)
    intelmqsetup_core(ownership=not args.skip_ownership,
                      state_file=args.state_file)
    if intelmq_api and not args.skip_api:
        print('Running setup for intelmq-api.')
        intelmqsetup_api(ownership=not args.skip_ownership,
                         webserver_user=args.webserver_user)
        print('Running webserver setup for intelmq-api.')
        intelmqsetup_api_webserver_configuration(webserver_configuration_directory=args.webserver_configuration_directory)
    else:
        print('Skipping set-up of intelmq-api.')
    if intelmq_manager and not args.skip_api:
        print('Running webserver setup for intelmq-manager.')
        intelmqsetup_manager_webserver_configuration(webserver_configuration_directory=args.webserver_configuration_directory)
    else:
        print('Skipping set-up of intelmq-manager.')

    if NOTE_WEBSERVER_RELOAD:
        print('Reload the webserver to make the changes effective.')

    print("'intelmqsetup' completed.")


if __name__ == '__main__':
    main()
