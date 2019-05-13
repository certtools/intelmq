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
Pip does not (and cannot) create `/opt/intelmq`, as described in
https://github.com/certtools/intelmq/issues/819
"""
import glob
import os
import shutil
import site
import sys

from intelmq import (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                     VAR_STATE_PATH)


def main():
    if os.geteuid() != 0:
        sys.exit('You need to run this program as root.')

    if not ROOT_DIR.startswith('/opt/'):
        print('Not a pip-installation of IntelMQ.')

    intelmq_path = os.path.join(site.getsitepackages()[0], 'opt/intelmq/')
    opt_path = os.path.join(site.getsitepackages()[0], 'opt/')
    if os.path.isdir(intelmq_path) and os.path.isdir(ROOT_DIR):
        print('%r already exists, not moving %r there.' % (ROOT_DIR,
                                                           intelmq_path))
    elif os.path.isdir(intelmq_path):
        shutil.move(intelmq_path, '/opt/')
        print('Moved %r to %r.' % (intelmq_path, '/opt/'))
        try:
            os.rmdir(opt_path)
        except OSError:
            print('Directory %r is not empty, did not remove it.' % opt_path)
    create_dirs = ('/opt/intelmq/var/lib/bots/file-output',
                   '/opt/intelmq/var/run',
                   '/opt/intelmq/var/log')
    for create_dir in create_dirs:
        if not os.path.isdir(create_dir):
            os.makedirs(create_dir, mode=0o755,
                        exist_ok=True)
            print('Created directory %r.' % create_dir)

    example_confs = glob.glob(os.path.join(CONFIG_DIR, 'examples/*.conf'))
    for example_conf in example_confs:
        fname = os.path.split(example_conf)[-1]
        if os.path.exists(os.path.join(CONFIG_DIR, fname)):
            print('Not overwriting existing %r with example.' % fname)
        else:
            shutil.copy(example_conf, CONFIG_DIR)
            print('Use example %r.' % fname)

    print('Setting intelmq as owner for it\'s directories.')
    for obj in (CONFIG_DIR, DEFAULT_LOGGING_PATH, ROOT_DIR, VAR_RUN_PATH,
                VAR_STATE_PATH, VAR_STATE_PATH + 'file-output'):
        shutil.chown(obj, user='intelmq')


if __name__ == '__main__':
    main()
