#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
© 2019 Sebastian Wagner <wagner@cert.at>

SPDX-License-Identifier: AGPL-3.0

Sets up an intelmq environment after installation or upgrade by
 * creating needed directories
 * set intelmq as owner for those
 * providing example configuration files if not already existing

Reasoning:
Pip does not (and cannot) create `/opt/intelmq`/user-given ROOT_DIR, as described in
https://github.com/certtools/intelmq/issues/819
"""
import argparse
import glob
import os
import shutil
import sys
import pkg_resources

from pwd import getpwuid

from intelmq import (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                     VAR_STATE_PATH)


def intelmqsetup(ownership=True):
    if os.geteuid() != 0 and ownership:
        sys.exit('You need to run this program as root (for setting file ownership)')

    if not ROOT_DIR:
        sys.exit('Not a pip-installation of IntelMQ, nothing to initialize.')

    create_dirs = ('%s/file-output' % VAR_STATE_PATH,
                   VAR_RUN_PATH,
                   DEFAULT_LOGGING_PATH,
                   CONFIG_DIR)
    for create_dir in create_dirs:
        if not os.path.isdir(create_dir):
            os.makedirs(create_dir, mode=0o755,
                        exist_ok=True)
            print('Created directory %r.' % create_dir)

    example_confs = glob.glob(pkg_resources.resource_filename('intelmq', 'etc/*.conf'))
    for example_conf in example_confs:
        fname = os.path.split(example_conf)[-1]
        if os.path.exists(os.path.join(CONFIG_DIR, fname)):
            print('Not overwriting existing %r with example.' % fname)
        else:
            shutil.copy(example_conf, CONFIG_DIR)
            print('Use example %r.' % fname)

    if ownership:
        print('Setting intelmq as owner for it\'s directories.')
        for obj in (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                    VAR_STATE_PATH, VAR_STATE_PATH + 'file-output'):
            if getpwuid(os.stat(obj).st_uid).pw_name != 'intelmq':
                shutil.chown(obj, user='intelmq')


def main():
    parser = argparse.ArgumentParser("Set's up directories and example "
                                     "configurations for IntelMQ.")
    parser.add_argument('--skip-ownership', action='store_true',
                        help='Skip setting file ownership')
    args = parser.parse_args()
    intelmqsetup(ownership=not args.skip_ownership)


if __name__ == '__main__':
    main()
